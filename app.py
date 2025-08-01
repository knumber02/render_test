from fastapi import FastAPI, Request
import hashlib

app = FastAPI()

@app.put("/login")
async def login(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]
    token = hashlib.sha1((username + password).encode()).hexdigest()
    return {"token": token}

@app.put("/flag")
async def flag(request: Request):
    data = await request.json()
    print("✅ FLAG:", data["flag"])
    return {"ok": True}
