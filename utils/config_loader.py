import yaml
from pathlib import Path
from dataclasses import dataclass

_DEFAULT_CONFIG_PATH = str(Path(__file__).parent.parent / "configs" / "config.yaml")

@dataclass
class LLMConfig:
    provider: str
    model_name: str

class ConfigLoader:
    """Class used to load a config file
    """
    def __init__(self, config_path: str = _DEFAULT_CONFIG_PATH):
        self._config = self._load(config_path)
        self.provider = self._config["provider"]
        self.model_name = self._config["model_name"]

    def _load(self, config_path: str) -> dict:
        """Loads a config file from the specified config.yaml file path.

        Args:
            config_path (str): location of the config.yaml file

        Raises:
            FileNotFoundError: If config.yaml file is not found
            ValueError: If config.yaml does not contain 'llm' as first key

        Returns:
            dict: The parsed config file in a dictionary format. e.g. {"provider": "groq", "model_name": "..."}
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(path, "r") as f:
            raw = yaml.safe_load(f)

        llm_section = raw.get("llm", {})
        
        for key, value in llm_section.items():
            if isinstance(value, dict) and "provider" in value:
                return value
        
        raise ValueError("No valid provider config found under 'llm' in config.yaml")