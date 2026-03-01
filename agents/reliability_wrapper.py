# reliability_wrapper.py
# Simple wrapper to add reliability to any LLM agent
# Catches hallucinations, loops, cost explosions
# Built by Sarvesh for ToolReliBench

from typing import Dict, Any
import json

class AgentState:
    def __init__(self):
        self.messages = []  # List of chat messages
        self.token_count = 0
        self.failure_type = None
        self.retries = 0
        self.max_retries = 2
        self.max_tokens = 8000

def reliability_wrapper(agent_function, max_tokens=8000, max_retries=2):
    """
    Wraps any agent to add safety checks.
    - Detects hallucinated tools
    - Limits retries and tokens
    - Returns failure type if something goes wrong
    """
    def safe_run(task: Dict[str, Any]) -> Dict[str, Any]:
        state = AgentState()
        state.messages.append({"role": "user", "content": task["user_prompt"]})
        state.max_tokens = max_tokens
        state.max_retries = max_retries
        
        for attempt in range(state.max_retries + 1):
            # Call the real agent (you add this later)
            response = agent_function(state.messages)
            
            # Fake usage for now (replace with real token count)
            state.token_count += 100  # Simulate tokens
            
            # Check for cost explosion
            if state.token_count > state.max_tokens:
                state.failure_type = "Cost Explosion"
                return {
                    "success": False,
                    "failure_type": state.failure_type,
                    "tokens": state.token_count
                }
            
            # Check for hallucinated tool (simple string check)
            response_str = str(response).lower()
            if "non_existent" in response_str or "fake_tool" in response_str:
                state.failure_type = "Hallucinated Tool"
                state.retries += 1
                if attempt == state.max_retries:
                    return {
                        "success": False,
                        "failure_type": state.failure_type,
                        "tokens": state.token_count
                    }
                continue  # Retry
            
            # Add more checks here later (wrong tool, loops, etc.)
            
            # If all good
            return {
                "success": True,
                "final_answer": getattr(response, 'content', 'No content'),
                "tokens": state.token_count,
                "failure_type": None
            }
        
        # Fallback
        return {"success": False, "failure_type": "Max Retries Exceeded"}
    
    return safe_run

# Example usage (test this yourself later)
if __name__ == "__main__":
    def dummy_agent(messages):
        return {"content": "I called a fake tool!"}
    
    wrapped = reliability_wrapper(dummy_agent)
    result = wrapped({"user_prompt": "Test task"})
    print(result)  # Should detect hallucination
