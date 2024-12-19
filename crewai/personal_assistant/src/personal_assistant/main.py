#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from crews.poem_crew.poem_crew import AssistantCrew


class PoemState(BaseModel):
    request: str = ""
    report: str = ""


class PoemFlow(Flow[PoemState]):

    @start()
    def get_request(self):
        
        print("Entering Request")
        self.state.request = 'What is the latest price of AAPL?'

    @listen(get_request)
    def handle_request(self):
        print("Handling Request")
        result = (
            AssistantCrew()
            .crew()
            .kickoff(inputs={"request": self.state.request})
        )

        print("Report generated", result.raw)
        self.state.report = result.raw

    @listen(handle_request)
    def save_poem(self):
        print("Saving Report")
        with open("report.txt", "w") as f:
            f.write(self.state.report)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
