from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["main"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint that returns a simple HTML welcome page."""
    
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>NoteApp FastAPI</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                    margin-bottom: 20px;
                    font-size: 2.5em;
                }
                .endpoints {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }
                .endpoint {
                    margin: 10px 0;
                    padding: 10px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 5px;
                }
                code {
                    background: rgba(0, 0, 0, 0.3);
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: monospace;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Note App FastAPI!</h1>
                <p>Welcome to your FastAPI server application. This is a simple note-taking server.</p>
                <p><strong>Debug Mode:</strong> {'🐛 Enabled' if DEBUG_MODE else '❌ Disabled'}</p>
                
                <div class="endpoints">
                    <h3>Available Endpoints:</h3>
                    <div class="endpoint">
                        <strong>GET</strong> <code>/</code> - This welcome page
                    </div>
                    <div class="endpoint">
                        <strong>POST</strong> <code>/notes</code> - Create a new note
                    </div>
                    <div class="endpoint">
                        <strong>GET</strong> <code>/notes</code> - Get all notes for a user
                    </div>
                    <div class="endpoint">
                        <strong>GET</strong> <code>/notes/{id}</code> - Get a specific note
                    </div>
                    <div class="endpoint">
                        <strong>PATCH</strong> <code>/notes/{id}/enrich</code> - Enrich note with LLM
                    </div>
                    <div class="endpoint">
                        <strong>PATCH</strong> <code>/notes/{id}</code> - Update a note
                    </div>
                    <div class="endpoint">
                        <strong>DELETE</strong> <code>/notes/{id}</code> - Delete a note
                    </div>
                    <div class="endpoint">
                        <strong>GET</strong> <code>/notes/stats/info</code> - Get service statistics
                    </div>
                    <div class="endpoint">
                        <strong>GET</strong> <code>/docs</code> - Interactive API documentation
                    </div>
                </div>
                
                <p>To explore the API interactively, visit <code>/docs</code> for the Swagger UI documentation.</p>
            </div>
        </body>
    </html>
    """
