from utils.model_loader import ModelLoader
from prompts.prompt import SYSTEM_PROMPT

from tools.weather_information import WeatherInfoTool
from tools.place_search import PlaceSearchTool
from tools.expense_calculator import ExpenseCalculatorTool 
from tools.currency_conversion import CurrencyConversionTool

from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.prebuilt import ToolNode,tools_condition

class GraphBuilder():
    def __init__(self):
        self.model_loader = None
        self.system_prompt = SYSTEM_PROMPT
        self.tools = []
        self.graph = None
        self.llm_with_tools = None
        
        self.tools.extend([
            *WeatherInfoTool().get_tools(),
            *PlaceSearchTool().get_tools(),
            *ExpenseCalculatorTool().get_tools(),
            *CurrencyConversionTool().get_tools()
        ])
    
    def agent_function(self, state : MessagesState) -> MessagesState:
        """The LLM Agent Function

        Args:
            state (MessagesState): the state of the llm to store contexts

        Returns:
            MessagesState: The output of the llm.
        """
        user_query = state['messages']
        llm_input_query = [self.system_prompt] + user_query
        llm_output = self.llm_with_tools.invoke(llm_input_query)
        return {
            'messages' : [llm_output]
        }
    
    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("llm_agent" , self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        
        graph_builder.add_edge(START, "llm_agent")
        graph_builder.add_conditional_edges("llm_agent",tools_condition)
        graph_builder.add_edge("tools","llm_agent")
        graph_builder.add_edge("llm_agent",END)
        
        self.graph = graph_builder.compile()
        return self.graph
    
    def __call__(self):
        self.model_loader = ModelLoader()
        llm = self.model_loader.load_llm()
        self.llm_with_tools = llm.bind_tools(self.tools)
        return self.build_graph()