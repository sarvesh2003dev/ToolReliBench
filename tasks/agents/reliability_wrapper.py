# agents/reliability_wrapper.py
# Simple reliability layer for LLM agents
# Detects basic hallucinations and limits retries + tokens
# You can add more checks later

from typing import Dict, Any, Callable

def reliability_wrapper(
    agent_function: Callable,
    max_retries: int = 2,
    max_tokens: int = 8000
):
    """
    Wraps any agent function to add basic safety:
    - Retry on obvious failures
    - Token budget check (approximate)
    - Hallucinated tool detection (simple string check for now)
    """
    def safe_agent_run(task: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "success": False,
            "final_answer": None,
            "failure_type": None,
            "tokens_used": 0,
            "retries": 0
        }

        for attempt in range(max_retries + 1):
            try:
                # Run the actual agent (you will connect real LLM later)
                response = agent_function(task["user_prompt"])

                # Fake token count for now (replace with real usage later)
                tokens_this_time = 300 + attempt * 100
                result["tokens_used"] += tokens_this_time

                if result["tokens_used"] > max_tokens:
                    result["failure_type"] = "Cost Explosion"
                    break

                # Very simple hallucinated tool check (expand this later)
                response_text = str(response).lower()
                if "non_existent" in response_text or "fake_tool" in response_text:
                    result["failure_type"] = "Hallucinated Tool"
                    if attempt == max_retries:
                        break
                    continue  # retry

                # If we reach here → assume success for this version
                result["success"] = True
                result["final_answer"] = response
                result["retries"] = attempt
                result["failure_type"] = None
                break

            except Exception as e:
                result["failure_type"] = "Execution Error"
                if attempt == max_retries:
                    break

        return result

    return safe_agent_run
