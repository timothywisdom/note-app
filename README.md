# NoteApp - AI-Powered Note Taking

A modern note-taking application built with FastAPI backend and Next.js frontend, featuring AI-powered note enrichment.

## Features

- **Create Notes**: Add new notes with content
- **View Notes**: Browse all your notes in a clean, card-based interface
- **AI Enrichment**: Automatically generate summaries, topics, tags, and sentiment analysis
- **User Management**: Switch between different user accounts
- **Real-time Updates**: See changes immediately across the interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

### Backend

- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11+**: Core runtime environment
- **Pydantic**: Data validation and serialization
- **Gemini API**: Real AI enrichment using Google's Gemini model

### Frontend

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful, customizable icons
- **Axios**: HTTP client for API communication

## Project Structure

```
note-app/
├── .env                   # Environment variables (create this file)
├── server/                # FastAPI backend
│   ├── main.py           # Main application entry point
│   ├── notes/            # Notes module
│   │   ├── models/       # Pydantic models organized by type
│   │   ├── services/     # Business logic services
│   │   ├── interfaces/   # Service interface protocols
│   │   ├── router.py     # API endpoints
│   │   ├── dependencies.py # Dependency injection
│   │   └── tests/        # Comprehensive test suite
│   └── requirements.txt  # Python dependencies
├── client/                # Next.js frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Utility libraries
│   │   ├── types/        # TypeScript type definitions
│   │   └── contexts/     # React contexts
│   └── package.json      # Node.js dependencies
├── run-server.sh         # Server startup script
└── run-client.sh         # Client startup script
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd note-app
   ```

2. **Install dependencies (one-time setup)**

   ```bash
   # Backend dependencies
   cd server
   python3.11 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cd ..

   # Frontend dependencies
   cd client
   npm install
   cd ..
   ```

3. **Set up environment variables**

   ```bash
   # Create .env file in the root directory
   touch .env

   # Add your Gemini API key to .env
   echo "GEMINI_API_KEY=your_actual_api_key_here" >> .env
   ```

### Running the Application

**Option 1: Run Both (Recommended)**
Open two terminal windows and run:

```bash
# Terminal 1 - Backend
./run-server.sh

# Terminal 2 - Frontend
./run-client.sh
```

**Option 2: Run Separately**

```bash
# Backend only
./run-server.sh

# Frontend only
./run-client.sh
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Notes

- `POST /notes` - Create a new note
- `GET /notes` - Get all notes for a user
- `GET /notes/{id}` - Get a specific note
- `PATCH /notes/{id}/enrich` - Enrich note with AI
- `PATCH /notes/{id}` - Update note content
- `DELETE /notes/{id}` - Delete a note

## Usage

1. **Create Notes**: Click "New Note" to add a note with content
2. **View Notes**: All your notes are displayed in a responsive grid layout
3. **AI Enrichment**: Click "Enrich with AI" to generate metadata for any note
4. **Switch Users**: Use the user selector to switch between different accounts
5. **Edit Notes**: Click on note content to modify it directly
6. **Delete Notes**: Remove unwanted notes with the delete button

## Development

### Backend Development

- The FastAPI server includes comprehensive integration test coverage
- Run tests: `cd server && pytest notes/tests/ -v`
- Tests cover the entire system through the router endpoints

### Frontend Development

- Built with Next.js App Router for modern React patterns
- TypeScript ensures type safety
- Tailwind CSS provides consistent styling
- Components are modular and reusable

### Testing

- **Backend**: Comprehensive integration tests using pytest that test the entire system through the router
- **Frontend**: Built-in Next.js testing capabilities

## Configuration

### Environment Variables

The application uses environment variables for configuration. Create a `.env` file in the root directory and add your values:

```bash
# In the root directory
touch .env
```

**Required Variables:**

- `GEMINI_API_KEY`: Google Gemini API key for AI enrichment (required for production)
  - Get your API key from: https://makersuite.google.com/app/apikey

**Optional Variables:**

- `NEXT_PUBLIC_API_URL`: Backend API URL (defaults to http://localhost:8000)
- `DEBUG_MODE`: Enable debug mode for the server (default: false)
- `DEBUG_PORT`: Debug port for the server (default: 5678)

### Customization

- **LLM Service**: The Gemini service is already integrated with real AI APIs
- **Styling**: Modify Tailwind classes or add custom CSS
- **Features**: Extend the API endpoints and frontend components

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000 and 3000 are available
2. **Python version**: Use Python 3.11+ for optimal compatibility
3. **Virtual environment**: Always activate the virtual environment before running the server
4. **Dependencies**: Run `npm install` in the client directory

### Debug Mode

Enable debug mode to attach a debugger:

```bash
./run-server.sh --debug
# or
./run-server.sh --debug-port 5679
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add integration tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details
