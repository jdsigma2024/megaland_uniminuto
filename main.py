import uvicorn
from infrastructure.api_fastapi import app

# Esto permite que uvicorn main:app --reload funcione perfectamente
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)