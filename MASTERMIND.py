
# Auto-Configuration for config.json
import os
import json

def auto_configure():
    config_path = 'config.json'
    default_agents = ['SimpleCoder.py', 'autonomize.py']
    if not os.path.exists(config_path):
        config = {'agents': default_agents}
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file)
        logging.info('config.json created with default agents: SimpleCoder.py, autonomize.py')
    else:
        logging.info('config.json already exists. Skipping auto-configuration.')

# Calling auto-configuration function during the initialization
auto_configure()

# MASTERMIND
import logging
import json
import threading
from typing import Dict, Type, Union, List
from abc import ABC, abstractmethod
import os
import psutil

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Agent Interface that all agents will implement
class AgentInterface(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass

# MASTERMIND Class
class MASTERMIND:

    def __init__(self):
        self.agent_store: Dict[str, AgentInterface] = {}
        self.data_store: Dict[str, Union[str, Dict]] = {}
        self.load_config()
        
    def load_config(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except Exception as e:
            logging.error(f"Could not load config: {e}")

    def load_agent(self, agent_name: str, agent_class: Type[AgentInterface]):
        # Security Check
        if not self.validate_agent(agent_name):
            logging.error(f"Agent {agent_name} failed the security validation.")
            return

        try:
            agent_instance = agent_class()
            agent_instance.initialize()
            self.agent_store[agent_name] = agent_instance
        except Exception as e:
            logging.error(f"Failed to load agent {agent_name}: {e}")

    def unload_agent(self, agent_name: str):
        try:
            agent_instance = self.agent_store.pop(agent_name)
            agent_instance.shutdown()
        except KeyError:
            logging.error(f"Agent {agent_name} not found.")
        except Exception as e:
            logging.error(f"Failed to unload agent {agent_name}: {e}")

    def execute_agents(self):
        threads = []
        for agent_name, agent_instance in self.agent_store.items():
            thread = threading.Thread(target=self.execute_single_agent, args=(agent_name, agent_instance,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def execute_single_agent(self, agent_name: str, agent_instance: AgentInterface):
        try:
            agent_instance.execute()
            agent_data = agent_instance.get_data()
            self.accumulate_data(agent_name, agent_data)
        except Exception as e:
            logging.error(f"Failed to execute agent {agent_name}: {e}")

    def accumulate_data(self, agent_name: str, data: Union[str, Dict]):
        # Data Validation
        if not self.validate_data(data):
            logging.error(f"Data from agent {agent_name} failed the validation check.")
            return
        self.data_store[agent_name] = data

    def get_data(self, agent_name: str):
        return self.data_store.get(agent_name, "Data not found.")

    def validate_agent(self, agent_name: str) -> bool:
        # For now, a simple validation to check if the agent is in the allowed list
        return agent_name in self.config.get("allowed_agents", [])

    def validate_data(self, data: Union[str, Dict]) -> bool:
        # Placeholder for more complex data validation
        return True

    def monitor_resources(self):
        # Simple resource monitoring using psutil
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        logging.info(f"CPU Usage: {cpu_percent}%")
        logging.info(f"Memory Usage: {memory_info.percent}%")
        
# Save data store to JSON file
def save_data_store(mastermind_instance: MASTERMIND):
    try:
        with open("data_store.json", "w") as f:
            json.dump(mastermind_instance.data_store, f)
    except Exception as e:
        logging.error(f"Failed to save data store: {e}")

# Example of a simple agent that implements the AgentInterface
class SimpleAgent(AgentInterface):

    def initialize(self):
        self.data = "Initialized"

    def execute(self):
        self.data = "Executed"

    def get_data(self):
        return self.data

    def shutdown(self):
        self.data = "Shutdown"

# Test the MASTERMIND class with a simple agent
if __name__ == "__main__":
    mastermind = MASTERMIND()
    mastermind.load_agent("SimpleAgent", SimpleAgent)
    mastermind.execute_agents()
    save_data_store(mastermind)
    mastermind.monitor_resources()
