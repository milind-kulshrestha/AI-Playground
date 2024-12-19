# from pydantic_ai import Agent
# from pydantic import BaseModel

# #result = agent.run_sync('Where does "hello world" come from?') 

# class CityLocation(BaseModel):
#     city: str
#     country: str

# agent = Agent(  
#     #system_prompt=' reply with a poem',  
#     model="ollama:llama3.2", #result_type=CityLocation
# )

# result = agent.run_sync('Where were the olympics held in 2012?')

# print('data:', result.data)
# print('all_messages_json:', result.all_messages_json())
# print('new_messages_json:', result.new_messages_json() or None)
# print('cost_request_token:', result.cost().request_tokens or None)
# print('cost_response_token:', result.cost().response_tokens or None)
# print('cost_total_token:', result.cost().total_tokens or None)
# print('cost_details:', result.cost().details or None)

# from pydantic import BaseModel
#
# from pydantic_ai import Agent
#
#
# class CityLocation(BaseModel):
#     city: str
#     country: str
#
#
# agent = Agent('openai:gpt-4o', result_type=CityLocation, result_retries=2
# )
#
# result = agent.run_sync('Where were the olympics held in 2012?')
# print(result.data)
# #> city='London' country='United Kingdom'
# print(result.cost())
# #> Cost(request_tokens=57, response_tokens=8, total_tokens=65, details=None)

from pydantic_ai import Agent, RunContext
import random

roulette_agent = Agent(  
    'openai:gpt-4o',
    deps_type=int,
    result_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the '
        'customer has won based on the number they provide.'
    ),
)


@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:  
    """check if the square is a winner"""
    return 'winner' if square == ctx.deps else 'loser'


# Run the agent
success_number = random.randint(1, 36) 
print(success_number)
result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
print(result.data)  
#> True

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.data)
#> False

def generate_search_queries(self, topic, n):
        user_prompt = f"""I'm writing a research report on {topic} and need help coming up with diverse search queries.
Please generate a list of {n} search queries that would be useful for writing a research report on {topic}. These queries can be in various formats, from simple keywords to more complex phrases. Do not add any formatting or numbering to the queries."""

        completion = self.get_llm_response(
            system='The user will ask you to help generate some search queries. Respond with only the suggested queries in plain text with no extra formatting, each on its own line.',
            user=user_prompt,
            temperature=1
        )
        return [s.strip() for s in completion.split('\n') if s.strip()][:n]