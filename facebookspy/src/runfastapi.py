def run_fastapi():
    """Run FastAPI server"""

    import uvicorn
    from .server.backend.app import app as fastapi_app

    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)
