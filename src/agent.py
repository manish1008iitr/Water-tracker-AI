import os 
from langchain_groq import ChatGroq
from dotenv import load_dotenv 
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

#Initialise LLM
llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    temperature=0.7, 
    api_key=GROQ_KEY
)

class WaterIntakeAgent():
    def __init__(self):
        self.history = []

    def analyse_intake(self,intake_ml):
        prompt = f"""
        You are a hydration assiastant. 
        The user has consumed {intake_ml} ml of water today. 
        Provide hydration status and suggest if they need to drink more water
        Provide answer in small statements with clearly highlighting how water should be drunk 
        and highlighting important recommendations (according to water consumed)
"""
        response = llm.invoke([HumanMessage(content = prompt)])
        return response.content

if __name__ == "__main__":
        agent = WaterIntakeAgent()
        intake = 1500
        feedback = agent.analyse_intake(intake)
        print(feedback)