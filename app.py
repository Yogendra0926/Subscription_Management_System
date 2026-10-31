"""Run the BrightLoop FastAPI backend from the repository root."""

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "MongoDB.connectionTable.mongoDB_fastapi.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
