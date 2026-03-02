# real_agent.py
# Real LLM agent using Claude or GPT
# Built by Sarvesh for ToolReliBench
# Uses free starter credits

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

load_dotenv()

def get_real_llm(model_name="claude-3-5-sonnet-20241022"):
    """Returns real model (Claude or GPT) or raises clear error"""
    load_dotenv()  # reload keys
    
    if "claude" in model_name.lower():
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key or key.startswith("your_"):
            raise ValueError("❌ Add your ANTHROPIC_API_KEY to .env file")
        return ChatAnthropic(model=model_name, api_key=key, temperature=0)
    
    elif "gpt" in model_name.lower():
        key = os.getenv("OPENAI_API_KEY")
        if not key or key.startswith("your_"):
            raise ValueError("❌ Add your OPENAI_API_KEY to .env file")
        return ChatOpenAI(model=model_name, api_key=key, temperature=0)
    
    else:
        raise ValueError("Use 'claude-3-5-sonnet-20241022' or 'gpt-4o-mini'")

def real_agent(messages):
    """Simple real agent function compatible with your wrapper"""
    try:
        llm = get_real_llm()  # change to "gpt-4o-mini" if you want GPT
        # LangChain needs proper message format - convert if dict
        if isinstance(messages, list) and isinstance(messages[0], dict):
            from langchain_core.messages import HumanMessage
            msgs = [HumanMessage(content=m["content"]) for m in messages]
        else:
            msgs = messages
        
        response = llm.invoke(msgs)
        return response  # has .content and usage info
    except Exception as e:
        print(f"⚠️ Real model failed: {e}")
        print("Falling back to dummy for now")
        return type('obj', (object,), {'content': 'Dummy fallback answer'})()
