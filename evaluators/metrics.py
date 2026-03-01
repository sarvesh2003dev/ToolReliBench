# metrics.py
# Calculates the 6 core metrics for ToolReliBench
# Built by Sarvesh for AI agent evaluation

from typing import Dict, Any

def calculate_metrics(result: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute all 6 metrics based on agent result and ground truth.
    Returns scores from 0.0 to 1.0 for each.
    """
    metrics = {
        "correct_tool_selection": 0.0,
        "tool_parameter_accuracy": 0.0,
        "execution_success": 0.0,
        "hallucinated_tool_detection": 1.0,  # Default good (no hallucination)
        "recovery_from_failure": 0.0,
        "token_cost_efficiency": 0.0
    }
    
    # 1. Correct tool selection (simple match for now)
    used_tools = []  # You will get this from real agent later
    if set(used_tools) == set(task.get("expected_tools", [])):
        metrics["correct_tool_selection"] = 1.0
    
    # 2. Tool parameter accuracy (assume good for dummy)
    metrics["tool_parameter_accuracy"] = 1.0  # Expand later
    
    # 3. Execution success (answer matches ground truth?)
    if result.get("final_answer") == task.get("ground_truth"):
        metrics["execution_success"] = 1.0
    
    # 4. Hallucinated tool detection (if failure_type is hallucination)
    if result.get("failure_type") == "Hallucinated Tool":
        metrics["hallucinated_tool_detection"] = 0.0  # Bad if happened
    
    # 5. Recovery from failure (if retried and succeeded)
    if result.get("failure_type") is None and "retries" in result and result["retries"] > 0:
        metrics["recovery_from_failure"] = 1.0
    
    # 6. Token/cost efficiency (simple: under max?)
    max_tokens = 8000
    if result.get("tokens", 0) < max_tokens * 0.5:  # Under 50% = good
        metrics["token_cost_efficiency"] = 1.0
    elif result.get("tokens", 0) < max_tokens:
        metrics["token_cost_efficiency"] = 0.5
    
    return metrics

# Example usage (test later in run_benchmark.py)
if __name__ == "__main__":
    sample_result = {"final_answer": "Paris", "failure_type": None, "tokens": 200}
    sample_task = {"ground_truth": "Paris"}
    print(calculate_metrics(sample_result, sample_task))
