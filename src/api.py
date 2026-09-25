from fastapi import FastAPI
from pydantic import BaseModel

from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history
from src.logger import log_message, log_error

app = FastAPI()
agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml : int

@app.post("/log-intake")
async def log_water_intake(request:WaterIntakeRequest):
    log_intake(request.user_id, request.intake_ml)
    analyse = agent.analyse_intake(request.intake_ml)
    log_message(f"user {request.user_id} logged request {request.intake_ml}")
    return {"message":"water intake logged succesfully", "analyse":analyse}

@app.get("/history{user_id}")
async def get_water_history(user_id):
    history = get_intake_history(user_id)
    return {"user_id" :user_id, "history":history}

