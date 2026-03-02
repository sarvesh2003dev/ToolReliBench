# real_agent.py
# Supports Claude, GPT, Gemini, Grok
# Built by Sarvesh for ToolReliBench

import os
from dotenv import load_dotenv

# All model imports
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_xai import ChatXAI
from langchain_core.messages import HumanMessage

load_dotenv()

def get_real_llm(model_name="gemini-1.5-flash"):
    """Choose any model by changing the name below"""
    load_dotenv()
    
    model_name = model_name.lower()
    
    if "gemini" in model_name:
        key = os.getenv("GEMINI_API_KEY")
        if not key or key.startswith("your_") or key == "":
            raise ValueError("❌ Add your GEMINI_API_KEY to .env file")
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=key, temperature=0)
    
    elif "grok" in model_name:
        key = os.getenv("GROK_API_KEY")
        if not key or key.startswith("your_") or key == "":
            raise ValueError("❌ Add your GROK_API_KEY to .env file")
        return ChatXAI(model="grok-beta", api_key=key, temperature=0)
    
    elif "claude" in model_name:
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key or key.startswith("your_") or key == "":
            raise ValueError("❌ Add your ANTHROPIC_API_KEY to .env file")
        return ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=key, temperature=0)
    
    elif "gpt" in model_name:
        key = os.getenv("OPENAI_API_KEY")
        if not key or key.startswith("your_") or key == "":
            raise ValueError("❌ Add your OPENAI_API_KEY to .env file")
        return ChatOpenAI(model="gpt-4o-mini", api_key=key, temperature=0)
    
    else:
        raise ValueError("Unknown model. Use: gemini-1.5-flash, grok-beta, claude-3-5-sonnet-20241022 or gpt-4o-mini")

def real_agent(messages):
    """Simple agent that works with your reliability wrapper"""
    try:
        llm = get_real_llm()   # Change model here: "grok-beta" or "gemini-1.5-flash"
        
        # Convert messages to LangChain format
        if isinstance(messages, list) and isinstance(messages[0], dict):
            msgs = [HumanMessage(content=m["content"]) for m in messages]
        else:
            msgs = messages
        
        response = llm.invoke(msgs)
        return response   # has .content and usage info
    
    except Exception as e:
        print(f"⚠️ Model error: {e}")
        print("Falling back to dummy...")
        return type('obj', (object,), {'content': 'Dummy fallback'})()
