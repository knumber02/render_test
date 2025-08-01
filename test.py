from fastapi import FastAPI, Request
import hashlib

app = FastAPI()

@app.put("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    token = hashlib.sha1((username + password).encode()).hexdigest()
    return {"token": token}

@app.put(("/flag"))
async def flag(request: Request):
    data = await request.json()
    print(data["flag"])
    return {"ok": True}
