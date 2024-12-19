from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class YFinanceToolInput(BaseModel):
    """Input schema for YFinanceTool."""

    ticker: str = Field(..., description="Ticker symbol of the stock.")


class YFinanceTool(BaseTool):
    name: str = "YFinance Tool"
    description: str = "Get the latest price of a stock using YFinance."

    def _run(self, argument: str) -> str:
        latest_price = get_latest_price(ticker_symbol)
        return latest_price

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    argument: str = Field(..., description="Description of the argument.")


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
