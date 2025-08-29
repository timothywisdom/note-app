import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from middleware import ExceptionHandlerMiddleware
from main_router import router as main_router
from notes import router as notes_router

# Load environment variables from .env file (look in parent directory as well)
load_dotenv(dotenv_path='../.env')

# Check if debug mode is enabled
DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"
DEBUG_PORT = int(os.environ.get("DEBUG_PORT", "5678"))

if DEBUG_MODE:
    try:
        import debugpy
        print(f"🐛 Debug mode enabled. Listening for debugger on port {DEBUG_PORT}...")
        print("🔗 Connect your debugger to continue...")
        debugpy.listen(("0.0.0.0", DEBUG_PORT))
        debugpy.wait_for_client()
        print("✅ Debugger connected! Continuing...")
    except ImportError:
        print("⚠️  debugpy not available. Debug mode disabled.")
        DEBUG_MODE = False
    except Exception as e:
        print(f"⚠️  Error in debug mode: {e}. Debug mode disabled.")
        DEBUG_MODE = False

app = FastAPI(
    title="NoteApp FastAPI",
    description="A modern FastAPI server application for note-taking with AI enrichment",
    version="1.0.0"
)

# Add custom exception handler middleware (must be first)
app.add_middleware(ExceptionHandlerMiddleware)

# Configure CORS to allow requests from the Next.js client
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js client (development)
        "http://127.0.0.1:3000",  # Alternative localhost format
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the main application router
app.include_router(main_router)

# Include the notes module router
app.include_router(notes_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
