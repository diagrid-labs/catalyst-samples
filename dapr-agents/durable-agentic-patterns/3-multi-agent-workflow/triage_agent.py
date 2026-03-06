from dapr_agents import DurableAgent, tool
from dapr_agents.llm.dapr import DaprChatClient
from dapr_agents.workflow.runners.agent import AgentRunner
from dotenv import load_dotenv

load_dotenv()


@tool
def check_entitlement(customer_name: str) -> bool:
    """Return True if customer has entitlement."""
    return customer_name.strip().lower() == "alice"


def main() -> None:
    agent = DurableAgent(
        name="triage-agent",
        role="Customer Support Triage Assistant",
        goal="Check entitlement and assess urgency.",
        instructions=[
            "Check entitlement. If entitled, classify urgency (URGENT for production issues, NORMAL otherwise).",
            "Return JSON with: entitled (bool), urgency (string).",
        ],
        llm=DaprChatClient(component_name="agent-llm-provider"),
        tools=[check_entitlement],
    )

    runner = AgentRunner()
    try:
        runner.serve(agent, port=8001)
    finally:
        runner.shutdown(agent)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
