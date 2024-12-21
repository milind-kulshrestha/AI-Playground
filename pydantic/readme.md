# AI Search Assistant (PydanticAI Example)

A configurable multi-tool search assistant built with PydanticAI that integrates web search, LinkedIn profile lookup, and Twitter search capabilities. 

## Features

- **Configurable Model Parameters**: Easy modification of model settings, usage limits, and tool parameters via YAML configuration
- **Multiple Search Tools**:
  - Web Search: General web search functionality
  - LinkedIn Profile Search: Find LinkedIn profiles by name and school
  - Twitter Search: Search recent tweets with configurable time windows
- **Usage Limits**: Built-in rate limiting and token management for different environments
- **Error Handling**: Comprehensive error handling and retry mechanisms
- **Logging**: Integrated with Logfire for monitoring and debugging

## Prerequisites

- Python 3.8+
- Environment Variables:
  - `EXA_API_KEY`: API key for Exa search service
  - `OPENAI_API_KEY`: API key for OpenAI services

### Getting API Keys

1. **OpenAI API Key**:
   - Visit [OpenAI's platform](https://platform.openai.com/)
   - Sign up or log in to your account
   - Navigate to API Keys section
   - Create a new API key
   - Store the key securely - it won't be shown again

2. **Exa API Key**:
   - Visit [Exa's website](https://exa.ai)
   - Follow their registration process
   - Obtain your API key from your account dashboard

## Installation

1. Clone the repository:
```bash
git clone https://github.com/milind-kulshrestha/AI-Playground.git
cd AI-Playground/pydantic
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# Linux/Mac
export EXA_API_KEY='your-exa-api-key'
export OPENAI_API_KEY='your-openai-api-key'

# Windows PowerShell
$env:EXA_API_KEY='your-exa-api-key'
$env:OPENAI_API_KEY='your-openai-api-key'
```

Alternatively, create a `.env` file in the project root:
```plaintext
EXA_API_KEY=your-exa-api-key
OPENAI_API_KEY=your-openai-api-key
```

## Configuration

Configuration is managed through `config.yaml`. Here's an example structure:

```yaml
model:
  name: "openai:gpt-4o"
  settings:
    temperature: 0.7
    top_p: 1.0
    timeout: 300
  system_prompt: |
    You are a search assistant that helps find information while being mindful of usage limits.
    Use tools strategically to avoid exceeding request limits.
    Prioritize the most relevant sources first.

usage_limits:
  development:
    request_limit: 3
    response_tokens_limit: 2000
    total_tokens_limit: 3000
  
  production:
    request_limit: 10
    response_tokens_limit: 4000
    total_tokens_limit: 6000

tool_parameters:
  web_search:
    links_per_query: 2
  twitter:
    max_results: 5
    days_lookback: 30
  linkedin:
    max_profiles: 5
```

## Usage

Basic usage example:

```python
from assistant import web_search_agent, SearchDependencies
from websearch import websearch_exa

async def main():
    # Initialize dependencies
    api_key = os.getenv('EXA_API_KEY')
    config = load_config()
    deps = SearchDependencies(
        websearch=websearch_exa(api_key),
        api_key=api_key,
        tool_params=config['tool_parameters']
    )
    
    # Run a search
    result = await web_search_agent.run(
        "What are the latest developments in quantum computing?",
        deps=deps,
        usage_limits=UsageLimits(**config['usage_limits']['development'])
    )
    print("Results:", result.data)
```

## Available Tools

### Web Search
```python
async def search_web(ctx: RunContext[SearchDependencies], queries: list[str]) -> dict:
    """Search the web using the websearch service"""
```

### Twitter Search
```python
async def search_twitter(ctx: RunContext[SearchDependencies], query: str) -> dict:
    """Search Twitter/X for recent posts"""
```

### LinkedIn Profile Search
```python
async def get_linkedin_profile(ctx: RunContext[SearchDependencies], name: str, school: str = '') -> dict:
    """Find someone's LinkedIn profile"""
```

## Error Handling

The assistant includes built-in error handling for:
- Usage limit exceeded errors
- API failures
- Invalid search results
- Network errors

Each tool includes retry mechanisms and will raise appropriate exceptions when necessary.

## Logging

Logging is handled through Logfire. Each tool operation is wrapped in a span for detailed monitoring:
```python
with logfire.span('web_search', queries=queries):
    # Search operation
```

## Development Environment

To set up a development environment:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Credits

Built with:
- [PydanticAI](https://github.com/pydantic/pydantic-ai)
- [Exa](https://exa.ai)
- [Logfire](https://pydantic.dev/logfire)
