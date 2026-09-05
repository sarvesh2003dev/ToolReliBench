# ToolReliBench

A practical benchmark and reliability wrapper for evaluating tool-using LLM agents.

> For the extended research implementation, long-horizon metrics, synthetic traces, and reproducibility materials, see [ToolReliBench1](https://github.com/sarvesh2003dev/ToolReliBench1).

## What it measures

- Tool-selection accuracy and parameter correctness
- Hallucinated tool calls and silent verification claims
- Recovery after tool errors
- Context drift, loops, and cost growth
- Structured failure categories for debugging agent behavior

## Quick start

```bash
git clone https://github.com/sarvesh2003dev/ToolReliBench.git
cd ToolReliBench
pip install -r requirements.txt
python run_benchmark.py
```

Results are written to CSV so experiments can be compared across models and architectures.

## Why it matters

Reliable tool use is a core requirement for production agents. ToolReliBench makes failure modes visible, measurable, and easier to reproduce.

## Author

Sarvesh Tamshe — [@sarvesh2003dev](https://github.com/sarvesh2003dev)

## License

MIT
