from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from investmentcrew.tools.custom_tool import Getfinancialratios
from pydantic import BaseModel, Field
from typing import Literal

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators




class InvestmentDecision(BaseModel):
    investment_action: Literal["Hold", "Buy", "Sell"] = Field(..., description="The recommended investment action.")
    analysis: str = Field(..., description="The detailed analysis supporting the recommendation.")
    confidence_score: int = Field(..., ge=0, le=100, description="The confidence score for the recommendation (0-100%).")

class FinancialAnalysis(BaseModel):
    company_name: str = Field(..., description="The name of the company being analyzed.")
    stock_ticker: str = Field(..., description="The stock ticker symbol for the company.")
    short_term_decision: InvestmentDecision = Field(..., description="The investment decision for the short term.")
    long_term_decision: InvestmentDecision = Field(..., description="The investment decision for the long term.")
    summary: str = Field(..., description="Summary of the investment recommendations.")
    conclusion: str = Field(..., description="Conclusion balancing potential growth with risks.")


@CrewBase
class Investmentcrew():
	"""Investmentcrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def financial_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['financial_analyst'],
			verbose=True,
			tools=[Getfinancialratios()]
		)

	@agent
	def investment_decision_maker(self) -> Agent:
		return Agent(
			config=self.agents_config['investment_decision_maker'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def financial_analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['financial_analyst_task'],
		)

	@task
	def investment_decision_maker_task(self) -> Task:
		return Task(
			config=self.tasks_config['investment_decision_maker_task'],
			context=[self.financial_analyst_task()],
			output_json=FinancialAnalysis
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Investmentcrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
