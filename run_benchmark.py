# run_benchmark.py
# Final Week 2 version - Uses real Claude/GPT + full metrics + reliability wrapper
# Built by Sarvesh for ToolReliBench

import json
import csv
from agents.reliability_wrapper import reliability_wrapper
from agents.real_agent import real_agent
from evaluators.metrics import calculate_metrics

print("🚀 Starting ToolReliBench with REAL models...\n")

# Wrap the real agent with your reliability layer
wrapped_agent = reliability_wrapper(real_agent, max_tokens=15000, max_retries=2)

# Load tasks
with open('tasks/sample_tasks.json', 'r') as f:
    tasks = json.load(f)

results = []
all_metrics = []

for task in tasks:
    print(f"Task {task['id']}: {task['user_prompt'][:65]}...")
    
    result = wrapped_agent(task)
    
    # Calculate 6 core metrics
    metrics = calculate_metrics(result, task)
    
    print(f"   ✅ Success : {result.get('success')}")
    print(f"   Failure    : {result.get('failure_type') or 'None'}")
    print(f"   Tokens     : {result.get('tokens', 'N/A')}")
    print(f"   Metrics    : {metrics}")
    print("─" * 60)
    
    results.append(result)
    all_metrics.append(metrics)

# Save full results
with open('results.csv', 'w', newline='') as f:
    fieldnames = ['task_id', 'success', 'failure_type', 'tokens'] + list(all_metrics[0].keys() if all_metrics else [])
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for i, (r, m) in enumerate(zip(results, all_metrics)):
        row = {
            'task_id': tasks[i]['id'],
            'success': r.get('success'),
            'failure_type': r.get('failure_type'),
            'tokens': r.get('tokens'),
            **m
        }
        writer.writerow(row)

print("\n✅ WEEK 2 COMPLETE!")
print("📊 Open results.csv to see full scores")
print("Your benchmark now measures real agent reliability!")
