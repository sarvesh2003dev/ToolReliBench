# ToolReliBench

Tool-Use Benchmark + Reliability Wrapper for LLM Agents

Built to solve real problems that OpenAI, Anthropic and DeepMind care about:  
- Detect hallucinated tool calls  
- Measure agent autonomy  
- Prevent cost explosions and loops  
- Structured failure analysis  

## Why this matters
AI companies want agents that are reliable with tools.  
This project shows I can build, test and document exactly that.

## Features
- 20+ realistic tasks  
- 6 clear metrics (correct tool, parameters, success rate, hallucination detection, recovery, cost)  
- Failure taxonomy with 8 types  
- Simple reliability wrapper (easy to add to any agent)  
- All results saved as CSV  

## Failure Taxonomy
| Category       | Failure Mode               | Example                              |
|----------------|----------------------------|--------------------------------------|
| Tool Selection | Hallucinated Tool          | Calls tool that does not exist       |
| Tool Selection | Wrong Tool                 | Uses calculator for date             |
| Parameter      | Invalid Params             | Missing required field               |
| Execution      | Tool Error (no recovery)   | API fails and stops                  |
| Execution      | Tool Error (recovered)     | Retries and succeeds                 |
| Planning       | Infinite Loop / Drift      | Keeps calling same tool              |
| Verification   | Wrong Final Answer         | Tool works but answer is wrong       |
| Resource       | Cost Explosion             | Uses too many tokens                 |

## How to run (very easy)
1. Clone or download the repo  
2. pip install -r requirements.txt  
3. Add your API keys  
4. python run_benchmark.py  

## Author
Sarvesh (sarvesh2003dev)  
Open source project for AI agent research 2026

Star ⭐ if you like reliable agents!
