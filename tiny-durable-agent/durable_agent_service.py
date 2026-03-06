from dapr_agents import DurableAgent
from dapr_agents.workflow.runners import AgentRunner

runner = AgentRunner()
agent = DurableAgent(name="Assistant", system_prompt="You are a helpful assistant")

try:
    runner.subscribe(agent)
    runner.serve(agent, port=8001)
finally:
    runner.shutdown()
