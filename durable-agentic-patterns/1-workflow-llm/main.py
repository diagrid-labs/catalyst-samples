import json
import logging
import uuid
from time import sleep

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import dapr.ext.workflow as wf
from dapr.ext.workflow import DaprWorkflowContext, WorkflowRuntime

from dapr_agents.llm.dapr import DaprChatClient


class SupportRequest(BaseModel):
    customer: str
    issue: str


wfr = WorkflowRuntime()
llm = DaprChatClient()


@wfr.activity(name="classify_ticket")
def classify_ticket(ctx, input_data: str) -> str:
    """Classify a support ticket by priority and category."""
    response = llm.generate(
        messages=(
            f"Classify this support ticket.\n\n{input_data}\n\n"
            "Return JSON with: priority (high/normal/low), category (billing/technical/general), summary."
        )
    )
    return response.get_message().content


@wfr.activity(name="generate_resolution")
def generate_resolution(ctx, input_data: str) -> str:
    """Generate a resolution for a high-priority ticket."""
    response = llm.generate(
        messages=(
            f"Provide a resolution for this high-priority ticket.\n\n{input_data}\n\n"
            "Return JSON with: resolution, estimated_time, customer_message."
        )
    )
    return response.get_message().content


@wfr.workflow(name="support_workflow")
def support_workflow(ctx: DaprWorkflowContext, input_data: dict):
    customer = input_data.get("customer")
    issue = input_data.get("issue")

    # Step 1: Classify the ticket
    ticket_info = f"Customer: {customer}\nIssue: {issue}"
    classification_raw = yield ctx.call_activity(classify_ticket, input=ticket_info)

    try:
        classification = json.loads(classification_raw)
    except (json.JSONDecodeError, TypeError):
        classification = {"priority": "normal", "category": "general", "summary": issue}

    priority = classification.get("priority", "normal")

    # Step 2: Gate — only resolve high-priority tickets
    if priority != "high":
        return {
            "status": "acknowledged",
            "priority": priority,
            "message": f"Thank you {customer}. Your {priority}-priority ticket has been logged.",
        }

    # Step 3: Generate resolution
    resolution_raw = yield ctx.call_activity(
        generate_resolution,
        input=f"Customer: {customer}\nIssue: {issue}\nCategory: {classification.get('category')}",
    )

    try:
        resolution = json.loads(resolution_raw)
    except (json.JSONDecodeError, TypeError):
        resolution = {"resolution": resolution_raw}

    return {"status": "resolved", "priority": "high", "resolution": resolution}


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

wfr.start()
sleep(3)

workflow_client = wf.DaprWorkflowClient()


@app.post("/workflow/start")
def start_workflow(request: SupportRequest):
    try:
        instance_id = str(uuid.uuid4())
        logger.info(f"Starting workflow for {request.customer}")
        workflow_client.schedule_new_workflow(
            workflow=support_workflow,
            input=request.dict(),
            instance_id=instance_id,
        )
        return {"instanceId": instance_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=8001)
