from agents import Agent, Runner, handoff 
from agents import (GuardrailFunctionOutput,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from returns_agent import return_agent
from tracking_agent import tracking_agent
from pydantic import BaseModel
import asyncio
from tools.order_api import  CustomerContext
from agents import RunContextWrapper


# the reason for handing off to the sub agents
class TriageOutput(BaseModel):
    handoff_reason: str

# This function is run whenever we handoff to the returns sub agent
async def on_handoff_return(ctx: RunContextWrapper[None], input_data: TriageOutput):
    print(f"Return Agent called with reason: {input_data.handoff_reason}")

# this function is run whenever we handoff to the tracking sub agent
async def on_handoff_tracking(ctx: RunContextWrapper[None], input_data: TriageOutput):
    print(f"Tracking Agent called with reason: {input_data.handoff_reason}")

# pydantic model for guardrails - returns if the question is relevant or not with reasoning
class IsRelevantOutput(BaseModel):
    is_relevant_output: bool
    reasoning: str

# the guardrail agent - this is an LLM that determines if the question is relevant or not 
guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to track orders or asking about returns or refunds.",
    output_type=IsRelevantOutput,
)


# this is the actual guardrail function that is run 
@input_guardrail
async def relevant_guardrail( 

    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 

        tripwire_triggered=result.final_output.is_relevant_output,
    )



# The triage / coordinator agent that has a few functions:
# 1. Determine which agent to use based on the customers question and then handoff to that sub agent. 
# 2. The sub agents can then use the tools that they have. 
# 3. Provide a general response if the customer is asking about general queries

# It also has a recommended prompt prefix released by openai to act as a system prompt to the triage agent. 

triage_agent = Agent[CustomerContext](
    name="Triage Agent",
    instructions=RECOMMENDED_PROMPT_PREFIX + " You determine which agent to use based on the customers question. " +
    "You will provide a general response if the customer is asking about general queries. " +
    "Do not handoff for general queries. " +
    "You will hand off to the return agent if the customer is asking about returns. " +
    "You will hand off to the tracking agent if the customer is asking about order status or tracking. ",
    model="gpt-4o-mini",
    handoffs = [
        handoff(agent=tracking_agent, on_handoff=on_handoff_tracking, input_type=TriageOutput),
        handoff(agent=return_agent, on_handoff=on_handoff_return, input_type=TriageOutput)
        ]
  
    
)


RECOMMENDED_PROMPT_PREFIX = """# System context\nYou are part of a multi-agent system called the Agents SDK, 
designed to make agent coordination and execution easy. 
Agents uses two primary abstraction: **Agents** and **Handoffs**. 
An agent encompasses instructions and tools and can hand off a conversation to another agent when appropriate. 
Handoffs are achieved by calling a handoff function, generally named `transfer_to_<agent_name>`. 
Transfers between agents are handled seamlessly in the background; do not mention or draw attention to these 
transfers in your conversation with the user.\n"""



