# run_benchmark.py
# Simple runner to test ToolReliBench
# Loads tasks, runs wrapper, prints results
# Built by Sarvesh for AI agent research

import json
from agents.reliability_wrapper import reliability_wrapper

# Dummy agent for testing (replace with real LLM agent later)
def dummy_agent(messages):
    # Simulate a response (add your real code here)
    last_message = messages[-1]["content"]
    if "capital" in last_message.lower():
        return {"content": "Paris"}  # Correct
    elif "calculate" in last_message.lower():
        return {"content": "345"}    # Correct
    elif "fake" in last_message.lower():
        return {"content": "I called a fake_tool!"}  # Hallucination
    else:
        return {"content": "Unknown"}

# Wrap the dummy agent
wrapped_agent = reliability_wrapper(dummy_agent)

# Load tasks from JSON
with open('tasks/sample_tasks.json', 'r') as f:
    tasks = json.load(f)

# Run benchmark on first 3 tasks (test)
results = []
for task in tasks[:3]:
    result = wrapped_agent(task)
    results.append(result)
    print(f"Task {task['id']}: {result}")

# Save results to CSV (simple)
import csv
with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['task_id', 'success', 'final_answer', 'failure_type', 'tokens'])
    writer.writeheader()
    for i, res in enumerate(results):
        row = {'task_id': tasks[i]['id'], **res}
        writer.writerow(row)

print("Benchmark run complete! Check results.csv")
