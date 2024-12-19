from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import YFinanceTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class AssistantCrew:
    """The Assistant Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def equity_research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["equity_research_analyst"],
            llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
            tools=[YFinanceTool()]

        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def equity_research(self) -> Task:
        return Task(
            config=self.tasks_config["research_publicly_traded_company"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            verbose=True,
            manager_llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434"),  # Mandatory if manager_agent is not set
            respect_context_window=True,  # Enable respect of the context window for tasks
            memory=True,  # Enable memory usage for enhanced task execution
            manager_agent=None,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
            planning=True,  # Enable planning feature for pre-execution strategy
        )



