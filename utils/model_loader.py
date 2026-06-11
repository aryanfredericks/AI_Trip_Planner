from pydantic import BaseModel,Field
from typing import Literal,Optional
from config_loader import ConfigLoader

from langchain_groq import ChatGroq

import os

class ModelLoader(BaseModel):
    
    model_provider : Literal["groq","openai"] = "groq"
    config : Optional[ConfigLoader] = Field(default=None,exclude=True) 
    
    model_config = {"arbitrary_types_allowed": True}
    
    @classmethod
    def from_config(cls, config_path: str = "../configs/config.yaml") -> "ModelLoader":
        config = ConfigLoader(config_path)
        return cls(model_provider=config.provider, config=config)
    
    
    def load_llm(self):
        """Loads the specified model into the class

        Raises:
            ValueError: If the model provider is unsupported

        Returns:
            ChatGroq | ChatOpenAI : The llm model with specified model name 
        """
        if self.model_provider == "groq":
            print(f"Loading groq model {self.config.model_name}.")
            _api_key = os.getenv("GROQ_API_KEY")
            try:
                llm = ChatGroq(model=self.config.model_name, api_key=_api_key)
                print(f"Successfully loaded groq model {self.config.model_name}.")
                return llm
            except Exception as e:
                print(f"Failed to load model : {e}")
                
        if self.model_provider == "openai":
            pass  # implement if using open ai models
        
        raise ValueError(f"Unsupported provider: {self.model_provider}")