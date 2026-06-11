from utils.model_loader import ModelLoader
from prompts.prompt import SYSTEM_PROMPT

# from tools.weather_information import WeatherInfoTool
# from tools.place_search import PlaceSearchTool
# from tools.expense_calculator import ExpenseCalculatorTool 
# from tools.currency_conversion import CurrencyConversionTool

from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.prebuilt import ToolNode,tools_condition

class GraphBuilder():
    def __init__(self):
        pass
    
    def agent_function(self):
        pass
    
    def build_graph(self):
        pass
    
    def __call__(self):
        pass