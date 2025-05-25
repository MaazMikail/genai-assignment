from agents import Agent, Runner
from tools.order_api import get_order_status, CustomerContext

# The tracking agent uses the get_order_status API tool to fetch the order status
# Whenever the coordinator/triage delegates to the tracker, it calls the tool to answer the user query. 

tracking_agent = Agent(
    name="Tracking Agent",
    model="gpt-4o-mini",
    instructions="You are a tracking agent and your job is to track the order status, you can use the tools provided to get the order status.",
    tools=[
        get_order_status
    ]
)



