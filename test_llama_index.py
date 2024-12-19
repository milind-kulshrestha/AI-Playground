#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:57:49 2024

@author: mk
"""

from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from llama_index.tools.

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

add_tool = FunctionTool.from_defaults(fn=add)

llm = Ollama(model="llama3.1:70b", request_timeout=120.0,)
agent = ReActAgent.from_tools([multiply_tool, add_tool], llm=llm, verbose=True,max_iterations=20)

response = agent.chat("What is 20+(2*4)? Calculate step by step.")

print(response)

finance_tools = YahooFinanceToolSpec().to_tool_list()

agent = ReActAgent.from_tools(finance_tools, llm = llm, verbose=True)

response = agent.chat("What is the current price of AAPL?")

print(response)

from llama_index.tools.wikipedia import WikipediaToolSpec
from llama_index.agent.openai import OpenAIAgent

tool_spec = WikipediaToolSpec()

agent = ReActAgent.from_tools(tool_spec.to_tool_list(), llm = llm, verbose = True)

response = agent.chat("Who is Ben Afflecks spouse?")

print(response)
