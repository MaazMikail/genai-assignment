# this file builds the order_status API to get order status. 

from agents import function_tool, RunContextWrapper
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import pandas as pd
import os

# The customer context to be fed to the API through the agent. 
class CustomerContext(BaseModel):
    customer_id: str 
    customer_name: str | None = None
    

app = FastAPI()

script_dir = os.path.dirname(os.path.abspath(__file__))
orders = pd.read_json(os.path.join(script_dir, "../data/dummy_orders.json"))

@function_tool
@app.get("/order_status")
async def get_order_status(context: RunContextWrapper[CustomerContext]):
    
    result = orders[orders["customer_id"] == context.context.customer_id]
    if result.empty:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    return result.to_dict(orient="records")[0]




    
    