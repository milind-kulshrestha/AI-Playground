import os
from typing import Optional
from typing_extensions import TypedDict
from dataclasses import dataclass
from datetime import datetime, timedelta
import yaml
from pathlib import Path

from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.settings import UsageLimits, ModelSettings
from websearch import websearch_exa
import logfire

# Configure logging
logfire.configure(send_to_logfire='if-token-present')

class SearchResultType(TypedDict):
    """Structured type for search results"""
    query: str
    results: list[dict]
    source: str
    timestamp: str

@dataclass
class SearchDependencies:
    """Dependencies for the search agent"""
    websearch: websearch_exa
    api_key: str
    tool_params: dict  # Store tool parameters from config

def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Initialize the agent with configuration
config = load_config()
web_search_agent = Agent(
    config['model']['name'],
    deps_type=SearchDependencies,
    result_type=SearchResultType,
    system_prompt=config['model']['system_prompt'],
    model_settings=ModelSettings(**config['model']['settings'])
)

@web_search_agent.tool(retries=2)
async def search_web(
    ctx: RunContext[SearchDependencies],
    queries: list[str],
) -> dict:
    """Search the web using the websearch service"""
    links_per_query = ctx.deps.tool_params['web_search']['links_per_query']
    
    with logfire.span('web_search', queries=queries):
        try:
            results = ctx.deps.websearch.get_search_results(
                queries=queries,
                links_per_query=links_per_query
            )
            
            if not results:
                raise ModelRetry("No results found. Try reformulating the query.")
            
            return {
                "query": ", ".join(queries),
                "results": [
                    {
                        'title': r.title if hasattr(r, 'title') else '',
                        'url': r.url if hasattr(r, 'url') else '',
                        'text': r.text if hasattr(r, 'text') else ''
                    } for r in results
                ],
                "source": "web",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logfire.error("Web search failed", error=str(e))
            raise ModelRetry(f"Search failed: {str(e)}")

@web_search_agent.tool(retries=2)
async def search_twitter(
    ctx: RunContext[SearchDependencies],
    query: str,
) -> dict:
    """Search Twitter/X for recent posts"""
    twitter_params = ctx.deps.tool_params['twitter']
    days_lookback = twitter_params['days_lookback']
    max_results = twitter_params['max_results']
    
    start_date = (datetime.now() - timedelta(days=days_lookback)).isoformat()
    
    with logfire.span('twitter_search', query=query):
        try:
            results = ctx.deps.websearch.search_twitter(
                query=query,
                num_results=max_results,
                start_published_date=start_date
            )
            
            if not results:
                raise ModelRetry("No tweets found. Try adjusting the query.")
            
            return {
                "query": query,
                "results": [
                    {
                        'text': r.text if hasattr(r, 'text') else '',
                        'url': r.url if hasattr(r, 'url') else ''
                    } for r in results
                ],
                "source": "twitter",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logfire.error("Twitter search failed", error=str(e))
            raise ModelRetry(f"Twitter search failed: {str(e)}")

@web_search_agent.tool(retries=2)
async def get_linkedin_profile(
    ctx: RunContext[SearchDependencies],
    name: str,
    school: str = ''
) -> dict:
    """Find someone's LinkedIn profile"""
    with logfire.span('linkedin_search', name=name):
        try:
            profile_url = ctx.deps.websearch.get_linkedin(name, school)
            
            if not profile_url:
                raise ModelRetry(f"Could not find LinkedIn profile for {name}")
            
            return {
                "query": name,
                "results": [{
                    'url': profile_url,
                    'name': name,
                    'school': school
                }],
                "source": "linkedin",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logfire.error("LinkedIn search failed", error=str(e))
            raise ModelRetry(f"LinkedIn search failed: {str(e)}")

async def main():
    # Get API key from environment
    api_key = os.getenv('EXA_API_KEY')
    if not api_key:
        raise ValueError("EXA_API_KEY environment variable is required")

    # Get configuration
    config = load_config()
    
    # Initialize dependencies
    deps = SearchDependencies(
        websearch=websearch_exa(api_key),
        api_key=api_key,
        tool_params=config['tool_parameters']
    )
    
    try:
        result = await web_search_agent.run(
            "What are the latest developments in quantum computing?",
            deps=deps,
            usage_limits=UsageLimits(**config['usage_limits']['development'])
        )
        print("Results:", result.data)
        
    except UsageLimitExceeded as e:
        print(f"Usage limit exceeded: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())