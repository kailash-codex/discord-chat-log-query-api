from fastapi import FastAPI
from api import chats
app = FastAPI()

@app.get("/")
def healthCheck():
    return {"status": "Application Health - Green"}


app.include_router(chats.api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)