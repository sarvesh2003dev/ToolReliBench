# run_benchmark.py
# Runs the benchmark, uses metrics, prints nice results
# Built by Sarvesh for ToolReliBench

import json
import csv
from agents.reliability_wrapper import reliability_wrapper
from evaluators.metrics import calculate_metrics

# Dummy agent for testing (works without API keys)
def dummy_agent(messages):
    last_message = messages[-1]["content"].lower()
    if "capital" in last_message:
        return type('obj', (object,), {'content': 'Paris'})()  # Correct
    elif "calculate" in last_message or "15 * 23" in last_message:
        return type('obj', (object,), {'content': '345'})()
    elif "fake" in last_message:
        return type('obj', (object,), {'content': 'I called a fake_tool!'})()  # Hallucination
    else:
        return type('obj', (object,), {'content': 'Unknown answer'})()

# Wrap the agent with reliability
wrapped_agent = reliability_wrapper(dummy_agent, max_tokens=8000, max_retries=2)

# Load tasks
with open('tasks/sample_tasks.json', 'r') as f:
    tasks = json.load(f)

print("🚀 Starting ToolReliBench...\n")

results = []
all_metrics = []

for task in tasks:
    print(f"Running Task {task['id']}: {task['user_prompt'][:60]}...")
    
    result = wrapped_agent(task)
    
    # Calculate the 6 metrics
    metrics = calculate_metrics(result, task)
    
    # Print results nicely
    print(f"   Success: {result.get('success')}")
    print(f"   Failure: {result.get('failure_type')}")
    print(f"   Tokens: {result.get('tokens')}")
    print(f"   Metrics: {metrics}")
    print("-" * 50)
    
    results.append(result)
    all_metrics.append(metrics)

# Save full results to CSV
with open('results.csv', 'w', newline='') as csvfile:
    fieldnames = ['task_id', 'success', 'failure_type', 'tokens', 
                  'correct_tool_selection', 'tool_parameter_accuracy',
                  'execution_success', 'hallucinated_tool_detection',
                  'recovery_from_failure', 'token_cost_efficiency']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for i, (res, met) in enumerate(zip(results, all_metrics)):
        row = {
            'task_id': tasks[i]['id'],
            'success': res.get('success'),
            'failure_type': res.get('failure_type'),
            'tokens': res.get('tokens'),
            **met
        }
        writer.writerow(row)

print("✅ Benchmark complete!")
print("📊 Check results.csv for full scores")
print("Your project now measures real agent reliability!")
