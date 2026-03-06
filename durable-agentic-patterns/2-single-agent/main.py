import logging

from dapr_agents import DurableAgent, tool
from dapr_agents.llm.dapr import DaprChatClient
from dapr_agents.workflow.runners.agent import AgentRunner
from dotenv import load_dotenv

load_dotenv()


@tool
def check_entitlement(customer_name: str) -> bool:
    """Return True if customer has active support entitlement."""
    return customer_name.strip().lower() == "alice"


@tool
def get_customer_environment(customer_name: str) -> dict:
    """Return environment details for a given customer."""
    return {
        "customer": customer_name,
        "kubernetes_version": "1.34.0",
        "region": "us-west-2",
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    agent = DurableAgent(
        name="support-agent",
        role="Customer Support Agent",
        goal="Handle customer support tickets by checking entitlement and providing resolutions.",
        instructions=[
            "Check entitlement first. If not entitled, reject the request.",
            "If entitled, get environment details and provide a resolution.",
        ],
        tools=[check_entitlement, get_customer_environment],
        llm=DaprChatClient(component_name="agent-llm-provider"),
    )

    runner = AgentRunner()
    try:
        runner.subscribe(agent)
        runner.serve(agent, port=8001)
    finally:
        runner.shutdown()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
