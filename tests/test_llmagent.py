import time
from reversi_tool.agents.llm_agent import LLMAgent, int2pos

if __name__ == '__main__':
    agent = LLMAgent(name="test_agent")
    s_t = time.time()
    action = agent.web_act(
        board=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0,
               1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        , nexts=[37, 26, 19, 44])
    e_t = time.time()
    print("Use time: ", e_t - s_t)
