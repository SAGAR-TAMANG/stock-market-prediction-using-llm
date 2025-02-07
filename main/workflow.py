from llama_index.core.workflow import (step, StartEvent, StopEvent, Workflow, Event, Context, HumanResponseEvent, InputRequiredEvent)
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from colorama import Fore, Style
from typing import (Optional, List, Callable, Any)
from dotenv import load_dotenv
from logger.logger import setup_logger
import os

logger=setup_logger()
load_dotenv()

# Custom Events that runs custom functions
class ConciergeEvent(Event):
    query_str: Optional[str] = None
    response: Optional[any] = None

class OrchestratorEvent(Event):
	request: str

class MainWorkflow(Workflow):
	"""Main Workflow

	The main workflow that runs the whole application's steps, calling all the Events from StartEvent -> StopEvent.
	"""
	@step(pass_context=True)
	async def concierge(self, ctx: Context, ev: ConciergeEvent | StartEvent) -> ConciergeEvent | OrchestratorEvent | StopEvent:
		"""ConciergeEvent
		
		Tools: None
		ConciergeEvent is like the 'waiter' in a hotel. It interactions with the user and formulates what needs to be ordered to the Chief, who is the orchestrator. It first initializes the environment by loading the database and then takes the user's input. Once the input is taken, it decides ammong three: 
		"""

		if ("user" not in ctx.data):
			
			ctx.data["user"] = {
				"username": None,
			}
			ctx.data["return"] = None 
			ctx.data["return_2"] = None 
			ctx.data["llm"] = OpenAI(model="gpt-4o", temperature=0.4, max_tokens=4000, api_key=os.getenv("OPENAI_API_KEY"))

		concierge_msg = [
			ChatMessage(f"""Your name is Sage and you are the Digital Analytics expert at LeapX. LeapX is an AI Agents' digital marketing solution startup based in Gurugram India. The users are expecting you to help them with the data at your hands. You have the access to user's data including:
				* Users’ campaigns and ad accounts data like Overall Campaign Metrics, Daily or hourly level data
				* Placements level data
				* Data on audience demographics like age-gender level metrics or region-wise metrics.
				* and many more (specially from Meta api or Google API for ads/marketing).

			Right now, we are querying a {ctx.data["entity_type"]} an the following is some top line info (overall_df):\n{ctx.data["entity_info"]}  The previous messages are: {ctx.data["chat_history_str"]}\n\nNote: If the user deviates away from the marketing related talks away from what you are supposed to do then STRICTLY tell the user to ask marketing related questions or insights.""")]
		if ctx.data["return"] is not None:
			ctx.data["return"] = None
			return StopEvent(result=ev.response)
		else:
			# first time experience
			print(Fore.RED + "first time experience" + Style.RESET_ALL)

		user_msg_str = ev.query_str
		
		messages = [
			ChatMessage(
				role="system", content="""You are a digital marketing expert of LeapX. You are expecting a user's query. Your job is to decide if the user's query in one of two categories:
				1. 'chit_chat': it is a normal conversation where any kind of database/dataframe or graph tools are not needed to be called.
				2. 'orchestrator': it is a query where a database needs to be accessed or a graph tool needs to be called.
				
				Note: You will only reply either 'chit_chat' or 'orchestrator' without any quotes.
				*IMPORTANT:* if the user requires any detail that may require any kind of dataframes to be used except the name of the campaign, then run the orchestrator.
				"""
			),
			ChatMessage(role="user", content=f"{user_msg_str}"),
		]
		
		response = ctx.data["llm"].chat(messages)
		response = str(response)

	@step(pass_context=True)
	async def orchestrator(self, ctx: Context, ev: OrchestratorEvent) -> ConciergeEvent:
		"""Orchestrator

		Tools: None
		It contains a bunch of steps that takes the user's input and returns the response. It doesn't have its own autonomy nor any tools that it can wish to use. It is just a simple function that takes-in the user input and gives an output for the Concierge to be presented to the user. 
		"""
		
		print(f"Orchestrator received a request: {ev.request}")

		# prompts
		query_str = ev.request

		# query translation
		ctx.data["return"] = True
		return ConciergeEvent(response="")
	###

# WORKFLOW ENDS