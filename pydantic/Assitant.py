from dataclasses import dataclass
from pydantic_ai import Agent, RunContext, Tool
import os
from websearch import websearch_exa

@dataclass
class Deps:
    websearch: websearch_exa
    exa_api_key: str | None


websearch_agent = Agent(
    'openai:gpt-4o',
    deps_type=Deps,
#    tools=[  

#        Tool(websearch_exa.get_linkedin_from_name, takes_ctx=True),
#        Tool(websearch_exa.search_twitter, takes_ctx=True),
#    ],
)
#dice_result = agent_b.run_sync('My guess is 4', deps='Anne')
#print(dice_result.data)
#> Congratulations Anne, you guessed correctly! You're a winner!

@websearch_agent.tool
def linkedin(ctx: RunContext[str], name: str, school: str = '') -> str:
    """Retrieve LinkedIn profile URL from a name and optional school."""
    return ctx.deps.websearch.get_linkedin(name, school)

@websearch_agent.tool
def twitter(ctx: RunContext[str], query: str, num_results: int, start_published_date: str) -> str:
    """Search for tweets related to a specific query."""
    return ctx.deps.websearch.search_twitter(query, num_results, start_published_date)

@websearch_agent.tool
def search(ctx: RunContext[str], queries: list[str], links_per_query:int) -> str:
    """Retrieve websearch results for a list of queries."""
    return ctx.deps.websearch.get_search_results(queries, links_per_query)

EXA_API_KEY = os.environ.get('EXA_API_KEY')
deps = Deps(websearch_exa(EXA_API_KEY), EXA_API_KEY)
result = websearch_agent.run_sync('Fed Powell press conference', deps=deps)
print(result.data)
