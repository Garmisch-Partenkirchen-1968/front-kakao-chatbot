import sys
from fastapi import FastAPI
from src.main import router as main_router

# src 디렉터리를 Python 경로에 추가
sys.path.append("./src")

app = FastAPI()

# Include the main router with prefix "/kakao"
app.include_router(main_router, prefix="/kakao")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8090)

