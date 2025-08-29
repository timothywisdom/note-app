import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
from uuid import uuid4, UUID
from typing import Dict, Any

from ..router import router
from ..dependencies import get_notes_service
from ..models import Note, NoteCreate, NoteUpdate, LLMEnrichment, Sentiment
from ..services.notes_service import NotesService


class TestNotesRouterIntegration:
    """Integration tests for the notes router endpoints."""

    @pytest.fixture
    def app(self):
        """Create a FastAPI app with the notes router for testing."""
        app = FastAPI(
            title="NoteApp FastAPI Test",
            description="Test FastAPI application for notes router",
            version="1.0.0"
        )
        
        # Add the same middleware as the real app
        from middleware.exception_handler import ExceptionHandlerMiddleware
        app.add_middleware(ExceptionHandlerMiddleware)
        
        app.include_router(router)
        return app

    @pytest.fixture
    def mock_gemini_model(self):
        """Create a mock Gemini model with all required methods."""
        mock_model = Mock()
        mock_model.model_name = "gemini-2.5-flash"
        
        # Mock the generate_content_async method that GeminiService calls
        mock_response = Mock()
        mock_response.text = '{"summary": "Test summary", "topics": ["test"], "sentiment": "positive", "key_entities": ["test"], "suggested_tags": ["test"], "complexity_score": 0.7}'
        mock_model.generate_content_async = AsyncMock(return_value=mock_response)
        
        return mock_model

    @pytest.fixture
    def notes_service(self, mock_gemini_model):
        """Create a NotesService instance with real GeminiService and mocked model."""
        # Clear any existing singleton instance
        NotesService._instance = None
        
        # Create a real GeminiService with mocked model
        from ..services.gemini_service import GeminiService
        gemini_service = GeminiService(gemini_model=mock_gemini_model)
        
        service = NotesService(gemini_service)
        # Clear notes for clean test state
        service._notes.clear()
        return service

    @pytest.fixture
    def client(self, app, notes_service):
        """Create a test client with mocked dependencies."""
        # Override the dependencies
        app.dependency_overrides[get_notes_service] = lambda: notes_service
        
        with TestClient(app) as test_client:
            yield test_client
        
        # Clean up
        app.dependency_overrides.clear()

    @pytest.fixture
    def sample_note_data(self):
        """Sample note creation data."""
        return {
            "content": "Test note content for integration testing",
            "user_id": "test_user_123"
        }

    @pytest.fixture
    def sample_note(self, sample_note_data, notes_service):
        """Create and store a sample note for testing."""
        note = Note(
            id=uuid4(),
            content=sample_note_data["content"],
            user_id=sample_note_data["user_id"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            metadata={}
        )
        notes_service._notes[note.id] = note
        return note



    class TestCreateNote:
        """Test POST /notes endpoint."""

        @pytest.mark.parametrize("note_data,expected_status,expected_response", [
            # Valid note creation
            (
                {"content": "Simple test note", "user_id": "user123"},
                201,
                {"content": "Simple test note", "user_id": "user123"}
            ),
            # Empty content (should still work)
            (
                {"content": "", "user_id": "user123"},
                201,
                {"content": "", "user_id": "user123"}
            ),
            # Very long content
            (
                {"content": "A" * 1000, "user_id": "user123"},
                201,
                {"content": "A" * 1000, "user_id": "user123"}
            ),
            # Content with special characters
            (
                {"content": "Note with @#$%^&*() chars", "user_id": "user123"},
                201,
                {"content": "Note with @#$%^&*() chars", "user_id": "user123"}
            ),
            # Content with unicode
            (
                {"content": "Note with unicode: café résumé 🚀", "user_id": "user123"},
                201,
                {"content": "Note with unicode: café résumé 🚀", "user_id": "user123"}
            ),
        ])
        def test_create_note_success(self, client, note_data, expected_status, expected_response):
            """Test successful note creation with various content types."""
            response = client.post("/notes/", json=note_data)
            
            assert response.status_code == expected_status
            response_data = response.json()
            
            # Check that required fields are present
            assert "id" in response_data
            assert "created_at" in response_data
            assert "updated_at" in response_data
            assert "metadata" in response_data
            
            # Check that content and user_id match
            assert response_data["content"] == expected_response["content"]
            assert response_data["user_id"] == expected_response["user_id"]
            
            # Check that timestamps are valid
            assert response_data["created_at"] == response_data["updated_at"]

        @pytest.mark.parametrize("invalid_data,expected_status", [
            # Missing content
            (
                {"user_id": "user123"},
                422
            ),
            # Missing user_id
            (
                {"content": "Test content"},
                422
            ),
            # Invalid content type
            (
                {"content": 123, "user_id": "user123"},
                422
            ),
            # Invalid user_id type
            (
                {"content": "Test content", "user_id": 123},
                422
            ),
            # Empty JSON
            (
                {},
                422
            ),
        ])
        def test_create_note_validation_errors(self, client, invalid_data, expected_status):
            """Test note creation with invalid data."""
            response = client.post("/notes/", json=invalid_data)
        
            assert response.status_code == expected_status

    class TestGetNotes:
        """Test GET /notes endpoint."""

        def test_get_notes_success(self, client, notes_service, sample_note):
            """Test successful retrieval of user notes."""
            # Create additional notes for the same user
            note2 = Note(
                id=uuid4(),
                content="Second test note",
                user_id=sample_note.user_id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                metadata={}
            )
            notes_service._notes[note2.id] = note2
            
            # Create a note for a different user
            other_user_note = Note(
                id=uuid4(),
                content="Other user's note",
                user_id="other_user",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                metadata={}
            )
            notes_service._notes[other_user_note.id] = other_user_note
            
            response = client.get(f"/notes/?user_id={sample_note.user_id}")
            
            assert response.status_code == 200
            notes = response.json()
            
            # Should return only notes for the specified user
            assert len(notes) == 2
            user_ids = [note["user_id"] for note in notes]
            assert all(uid == sample_note.user_id for uid in user_ids)

        def test_get_notes_empty_user(self, client):
            """Test getting notes for a user with no notes."""
            response = client.get("/notes/?user_id=empty_user")
            
            assert response.status_code == 200
            notes = response.json()
            assert notes == []

        @pytest.mark.parametrize("invalid_user_id,expected_status", [
            ("", 200),  # Empty user_id returns empty results
            (None, 422),  # Missing user_id triggers validation error
        ])
        def test_get_notes_validation_errors(self, client, invalid_user_id, expected_status):
            """Test getting notes with invalid user_id."""
            if invalid_user_id is None:
                response = client.get("/notes/")
            else:
                response = client.get(f"/notes/?user_id={invalid_user_id}")
            
            assert response.status_code == expected_status
            
            # For empty user_id, verify we get an empty array
            if invalid_user_id == "":
                notes = response.json()
                assert notes == []

    class TestGetNote:
        """Test GET /notes/{note_id} endpoint."""

        def test_get_note_success(self, client, sample_note):
            """Test successful retrieval of a single note."""
            response = client.get(f"/notes/{sample_note.id}?user_id={sample_note.user_id}")
            
            assert response.status_code == 200
            note = response.json()
            
            assert note["id"] == str(sample_note.id)
            assert note["content"] == sample_note.content
            assert note["user_id"] == sample_note.user_id

        def test_get_note_not_found(self, client):
            """Test getting a note that doesn't exist."""
            note_id = uuid4()
            response = client.get(f"/notes/{note_id}?user_id=test_user")
            
            assert response.status_code == 404
            assert "note not found" in response.text.lower()

        def test_get_note_unauthorized_user(self, client, sample_note):
            """Test getting a note with unauthorized user."""
            response = client.get(f"/notes/{sample_note.id}?user_id=unauthorized_user")
            
            assert response.status_code == 403
            assert "access denied" in response.text.lower()

        @pytest.mark.parametrize("invalid_note_id,expected_status", [
            ("invalid-uuid", 422),  # Invalid UUID format
            ("123", 422),  # Numeric string
        ])
        def test_get_note_invalid_id(self, client, invalid_note_id, expected_status):
            """Test getting a note with invalid note_id."""
            response = client.get(f"/notes/{invalid_note_id}?user_id=test_user")
            
            assert response.status_code == expected_status

    class TestEnrichNote:
        """Test PATCH /notes/{note_id}/enrich endpoint."""

        def test_enrich_note_success(self, client, sample_note, notes_service):
            """Test successful note enrichment."""
            response = client.patch(f"/notes/{sample_note.id}/enrich?user_id={sample_note.user_id}")
            
            assert response.status_code == 200
            note = response.json()
            
            # Check that metadata was updated
            assert "metadata" in note
            assert note["metadata"]["summary"] == "Test summary"
            assert note["metadata"]["topics"] == ["test"]
            assert note["metadata"]["sentiment"] == "positive"

        def test_enrich_note_not_found(self, client):
            """Test enriching a note that doesn't exist."""
            note_id = uuid4()
            response = client.patch(f"/notes/{note_id}/enrich?user_id=test_user")
            
            assert response.status_code == 404
            assert "note not found" in response.text.lower()

        def test_enrich_note_unauthorized_user(self, client, sample_note):
            """Test enriching a note with unauthorized user."""
            response = client.patch(f"/notes/{sample_note.id}/enrich?user_id=unauthorized_user")
            
            assert response.status_code == 403
            assert "access denied" in response.text.lower()

        def test_enrich_note_llm_service_error(self, client, sample_note, notes_service):
            """Test enrichment when LLM service fails."""
            # Mock the Gemini model to raise an exception
            mock_model = notes_service.llm_service.model
            mock_model.generate_content_async.side_effect = Exception("Gemini API error")
            
            response = client.patch(f"/notes/{sample_note.id}/enrich?user_id={sample_note.user_id}")
            
            # Should return 500 error due to LLM service failure
            assert response.status_code == 500

    class TestUpdateNote:
        """Test PATCH /notes/{note_id} endpoint."""

        @pytest.mark.parametrize("note_update,expected_status,expected_content", [
            # Update content only
            (
                {"content": "Updated content"},
                200,
                "Updated content"
            ),
            # Update metadata only
            (
                {"metadata": {"custom_key": "custom_value"}},
                200,
                "Test note content for integration testing"  # Content should remain unchanged
            ),
            # Update both content and metadata
            (
                {
                    "content": "Updated content and metadata",
                    "metadata": {"key": "value", "nested": {"deep": "value"}}
                },
                200,
                "Updated content and metadata"
            ),
            # Empty content update
            (
                {"content": ""},
                200,
                ""
            ),
            # Very long content update
            (
                {"content": "A" * 1000},
                200,
                "A" * 1000
            ),
        ])
        def test_update_note_success(self, client, sample_note, note_update, expected_status, expected_content):
            """Test successful note updates with various data types."""
            response = client.patch(
                f"/notes/{sample_note.id}?user_id={sample_note.user_id}",
                json=note_update
            )
            
            assert response.status_code == expected_status
            note = response.json()
            
            # Check that content was updated if provided
            if "content" in note_update:
                assert note["content"] == expected_content
            
            # Check that metadata was updated if provided
            if "metadata" in note_update:
                for key, value in note_update["metadata"].items():
                    assert note["metadata"][key] == value

        def test_update_note_not_found(self, client):
            """Test updating a note that doesn't exist."""
            note_id = uuid4()
            note_update = {"content": "Updated content"}
            
            response = client.patch(
                f"/notes/{note_id}?user_id=test_user",
                json=note_update
            )
            
            assert response.status_code == 404
            assert "note not found" in response.text.lower()

        def test_update_note_unauthorized_user(self, client, sample_note):
            """Test updating a note with unauthorized user."""
            note_update = {"content": "Updated content"}
            
            response = client.patch(
                f"/notes/{sample_note.id}?user_id=unauthorized_user",
                json=note_update
            )
            
            assert response.status_code == 403
            assert "access denied" in response.text.lower()

        @pytest.mark.parametrize("invalid_update,expected_status", [
            # Invalid content type
            ({"content": 123}, 422),
            # Invalid metadata type
            ({"metadata": "not_a_dict"}, 422),
            # Invalid UUID in path
            ("invalid-uuid", 422),
        ])
        def test_update_note_validation_errors(self, client, sample_note, invalid_update, expected_status):
            """Test note updates with invalid data."""
            if isinstance(invalid_update, str):
                # Test invalid UUID in path
                response = client.patch(
                    f"/notes/{invalid_update}?user_id={sample_note.user_id}",
                    json={"content": "Updated content"}
                )
            else:
                response = client.patch(
                    f"/notes/{sample_note.id}?user_id={sample_note.user_id}",
                    json=invalid_update
                )
            
            assert response.status_code == expected_status

    class TestDeleteNote:
        """Test DELETE /notes/{note_id} endpoint."""

        def test_delete_note_success(self, client, sample_note):
            """Test successful note deletion."""
            response = client.delete(f"/notes/{sample_note.id}?user_id={sample_note.user_id}")
            
            assert response.status_code == 204
            
            # Verify note was actually deleted
            get_response = client.get(f"/notes/{sample_note.id}?user_id={sample_note.user_id}")
            assert get_response.status_code == 404

        def test_delete_note_not_found(self, client):
            """Test deleting a note that doesn't exist."""
            note_id = uuid4()
            response = client.delete(f"/notes/{note_id}?user_id=test_user")
            
            assert response.status_code == 404
            assert "note not found" in response.text.lower()

        def test_delete_note_unauthorized_user(self, client, sample_note):
            """Test deleting a note with unauthorized user."""
            response = client.delete(f"/notes/{sample_note.id}?user_id=unauthorized_user")
            
            assert response.status_code == 403
            assert "access denied" in response.text.lower()

        @pytest.mark.parametrize("invalid_note_id,expected_status", [
            ("invalid-uuid", 422),  # Invalid UUID format
            ("123", 422),  # Numeric string
            ("", 405),  # Empty string (405 Method Not Allowed when endpoint is on root /notes endpoint)
        ])
        def test_delete_note_invalid_id(self, client, invalid_note_id, expected_status):
            """Test deleting a note with invalid note_id."""
            response = client.delete(f"/notes/{invalid_note_id}?user_id=test_user")
            
            assert response.status_code == expected_status

    class TestGetServiceStats:
        """Test GET /notes/stats/info endpoint."""

        def test_get_service_stats_success(self, client, notes_service, sample_note):
            """Test successful retrieval of service statistics."""
            # Create additional notes to test stats
            note2 = Note(
                id=uuid4(),
                content="Second test note",
                user_id="user456",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                metadata={}
            )
            notes_service._notes[note2.id] = note2
            
            response = client.get("/notes/stats/info")
            
            assert response.status_code == 200
            stats = response.json()
            
            # Check that expected fields are present
            assert "total_notes" in stats
            assert "unique_users" in stats
            assert "storage_type" in stats
            
            # Check that values are correct
            assert stats["total_notes"] == 2
            assert stats["unique_users"] == 2
            assert stats["storage_type"] == "in_memory"

        def test_get_service_stats_empty(self, client, notes_service):
            """Test service stats when no notes exist."""
            # Ensure no notes exist
            notes_service._notes.clear()
            
            response = client.get("/notes/stats/info")
            
            assert response.status_code == 200
            stats = response.json()
            
            assert stats["total_notes"] == 0
            assert stats["unique_users"] == 0
            assert stats["storage_type"] == "in_memory"

    class TestRouterErrorHandling:
        """Test router-level error handling."""

        def test_router_handles_service_exceptions(self, client, sample_note, notes_service):
            """Test that router properly handles service exceptions."""
            # Mock the Gemini model to raise an exception
            mock_model = notes_service.llm_service.model
            mock_model.generate_content_async.side_effect = Exception("Service error")
            
            response = client.patch(f"/notes/{sample_note.id}/enrich?user_id={sample_note.user_id}")
            
            # Should return 500 error due to unhandled service exception
            assert response.status_code == 500

        def test_router_handles_validation_errors(self, client):
            """Test that router properly handles validation errors."""
            # Test with invalid JSON
            response = client.post(
                "/notes/",
                data="invalid json",
                headers={"Content-Type": "application/json"}
            )
            
            assert response.status_code == 422

        def test_router_handles_malformed_requests(self, client):
            """Test that router properly handles malformed requests."""
            # Test with missing required query parameters
            response = client.get("/notes/")
            
            assert response.status_code == 422

    class TestRouterIntegrationScenarios:
        """Test complex integration scenarios."""

        def test_full_note_lifecycle(self, client, notes_service):
            """Test complete note lifecycle: create, read, update, enrich, delete."""
            # 1. Create note
            note_data = {"content": "Lifecycle test note", "user_id": "lifecycle_user"}
            create_response = client.post("/notes/", json=note_data)
            assert create_response.status_code == 201
            
            note = create_response.json()
            note_id = note["id"]
            user_id = note["user_id"]
            
            # 2. Read note
            read_response = client.get(f"/notes/{note_id}?user_id={user_id}")
            assert read_response.status_code == 200
            assert read_response.json()["content"] == note_data["content"]
            
            # 3. Update note
            update_data = {"content": "Updated lifecycle note"}
            update_response = client.patch(f"/notes/{note_id}?user_id={user_id}", json=update_data)
            assert update_response.status_code == 200
            assert update_response.json()["content"] == update_data["content"]
            
            # 4. Enrich note (mock Gemini model)
            # Set up the mock to return a valid enrichment response
            mock_response = Mock()
            mock_response.text = '{"summary": "Lifecycle test summary", "topics": ["test", "lifecycle"], "sentiment": "positive", "key_entities": ["test"], "suggested_tags": ["test"], "complexity_score": 0.8}'
            
            # Configure the mock model to return our test response
            mock_model = notes_service.llm_service.model
            mock_model.generate_content_async.return_value = mock_response
            
            enrich_response = client.patch(f"/notes/{note_id}/enrich?user_id={user_id}")
            assert enrich_response.status_code == 200
            
            enriched_note = enrich_response.json()
            assert "metadata" in enriched_note
            assert enriched_note["metadata"]["summary"] == "Lifecycle test summary"
            
            # 5. Delete note
            delete_response = client.delete(f"/notes/{note_id}?user_id={user_id}")
            assert delete_response.status_code == 204
            
            # 6. Verify deletion
            verify_response = client.get(f"/notes/{note_id}?user_id={user_id}")
            assert verify_response.status_code == 404

        def test_concurrent_operations(self, client, notes_service):
            """Test concurrent operations on the same note."""
            # Create a note
            note_data = {"content": "Concurrent test note", "user_id": "concurrent_user"}
            create_response = client.post("/notes/", json=note_data)
            assert create_response.status_code == 201
            
            note = create_response.json()
            note_id = note["id"]
            user_id = note["user_id"]
            
            # Simulate concurrent updates
            async def concurrent_update():
                update_data = {"content": f"Concurrent update {uuid4()}"}
                response = client.patch(f"/notes/{note_id}?user_id={user_id}", json=update_data)
                return response.status_code
            
            # Run multiple concurrent updates
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                tasks = [concurrent_update() for _ in range(5)]
                results = loop.run_until_complete(asyncio.gather(*tasks))
                
                # All updates should succeed
                assert all(status == 200 for status in results)
            finally:
                loop.close()
            
            # Verify final state
            final_response = client.get(f"/notes/{note_id}?user_id={user_id}")
            assert final_response.status_code == 200
            assert "Concurrent update" in final_response.json()["content"]
