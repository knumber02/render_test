from fastapi import FastAPI, Request, status
import hashlib
import pandas as pd
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()
class FlagRequest(BaseModel):
    flag: str

@app.put("/login")
async def login(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]
    token = hashlib.sha1((username + password).encode()).hexdigest()
    return {"token": token}



@app.put("/flag")
async def receive_flag(req: FlagRequest):
    flag = req.flag
    print(f"🎉 Received flag: {flag}")
    return {"message": "Flag received!"}


df = pd.read_csv("order_books.csv")
df["time"] = pd.to_datetime(df["time"].str.replace(" JST", "", regex=False), format="%Y-%m-%d %H:%M:%S %z")
df["rounded_time"] = df["time"].dt.floor("h")

ohlc = df.groupby(["code", "rounded_time"]).agg(
    open=("price", lambda x: x.iloc[0]),
    high=("price", "max"),
    low=("price", "min"),
    close=("price", lambda x: x.iloc[-1])
).reset_index()

@app.get("/candle")
async def get_candle(code: str, year: int, month: int, day: int, hour: int):
    try:
        dt = datetime(year, month, day, hour, tzinfo=df["rounded_time"].dt.tz)
        row = ohlc[(ohlc["code"] == code) & (ohlc["rounded_time"] == dt)]

        if row.empty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

        data = row.iloc[0][["open", "high", "low", "close"]].to_dict()
        return JSONResponse(content=data)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
