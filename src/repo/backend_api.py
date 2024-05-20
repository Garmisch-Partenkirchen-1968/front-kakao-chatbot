import httpx
from typing import List
from src.models.project import Project

API_ROOT = "https://garmissue.newpotatoes.org/backend/"

async def get_backend_projects(username: str, password: str) -> List[Project]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_ROOT}projects", auth=(username, password))
        if response.status_code != 200:
            raise Exception("Failed to fetch projects")
        projects_data = response.json()
        return [Project(**proj) for proj in projects_data]

async def verify_login(username: str, password: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_ROOT}login", json={"username": username, "password": password})
        if response.status_code != 200:
            raise Exception("Invalid username or password")
        user_data = response.json()
        return user_data['user_id']  # Assuming backend returns a user_id

