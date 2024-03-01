"""
MASTERMIND Controller Documentation
===================================

The MASTERMIND Controller is a sophisticated framework designed to manage and execute a collection of agents, each with distinct capabilities and tasks. It employs a modular architecture, facilitating the seamless integration and management of agents. This document provides an extensive overview of the MASTERMIND Controller's components, functionalities, and usage.

Components:
-----------
- `AgentInterface`: An abstract base class that defines the essential methods each agent must implement. These methods include `initialize`, `execute`, `get_data`, and `shutdown`.
- `MASTERMIND`: The core class that orchestrates the loading, execution, and management of agents. It handles directory setup, dynamic agent loading, and concurrent agent execution.

Key Functionalities:
-------------------
1. **Directory Setup**: The `MASTERMIND` class automatically creates and manages three key directories: `agents`, `tools`, and `executor`. These directories are essential for organizing agent scripts based on their development stage and functionality.
2. **Dynamic Agent Loading**: Agents are dynamically loaded from the `agents` and `tools` directories. This allows for the addition or removal of agent scripts without modifying the core controller code.
3. **Concurrent Agent Execution**: Agents are executed concurrently, each in its own thread, enabling efficient utilization of system resources and parallel task processing.

Usage Guide:
------------
1. Implement agent classes in Python files and place them in the `agents` or `tools` directories. Ensure each agent class inherits from `AgentInterface` and implements all abstract methods.
2. Run the `MASTERMINDcontroller.py` script. The controller will automatically load and execute all agents found in the designated directories.

AgentInterface Methods:
-----------------------
- `initialize()`: Prepares the agent for execution. This might involve setting up necessary resources or configurations.
- `execute()`: Contains the main logic of the agent. This is where the agent performs its designated task.
- `get_data()`: Retrieves any data or results produced during the agent's execution.
- `shutdown()`: Cleans up resources and performs any necessary teardown activities post-execution.

Example:
--------
Below is an example of how to implement a simple agent that conforms to the `AgentInterface`:

    class SimpleAgent(AgentInterface):
        def initialize(self):
            print("Initializing SimpleAgent.")
            
        def execute(self):
            print("Executing task in SimpleAgent.")
            
        def get_data(self):
            return "Data from SimpleAgent."
            
        def shutdown(self):
            print("Shutting down SimpleAgent.")

To execute this agent, place its script in the `agents` directory and run the `MASTERMINDcontroller.py` script.

"""

import os
import json
import logging
import threading
from abc import ABC, abstractmethod
import psutil
import importlib.util
import sys

logging.basicConfig(level=logging.INFO)

class AgentInterface(ABC):
    """Abstract base class defining the essential methods for agents managed by MASTERMIND."""

    @abstractmethod
    def initialize(self):
        """Prepare the agent for execution."""
        pass

    @abstractmethod
    def execute(self):
        """Core logic of the agent."""
        pass

    @abstractmethod
    def get_data(self):
        """Retrieve execution results or data."""
        pass

    @abstractmethod
    def shutdown(self):
        """Clean up resources post-execution."""
        pass

class MASTERMIND:
    """Core class responsible for managing agent lifecycles within the MASTERMIND framework."""

    def __init__(self):
        self.agents = {}
        self.directories = ["agents", "tools", "executor"]
        self._setup_directories()
        self._load_agents_from_directory("agents")
        self._load_agents_from_directory("tools")

    def _setup_directories(self):
        """Ensures the existence of required directories and sets appropriate permissions."""
        for directory in self.directories:
            os.makedirs(directory, exist_ok=True)
            os.chmod(directory, 0o700)

    def _load_agents_from_directory(self, directory):
        """Dynamically loads and initializes agents from the specified directory."""
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                agent_name = filename[:-3]  # Strip off '.py'
                module_path = os.path.join(directory, filename)
                self._load_agent_module(agent_name, module_path)

    def _load_agent_module(self, agent_name, module_path):
        """Loads an agent module and initializes its class if it implements AgentInterface."""
        spec = importlib.util.spec_from_file_location(agent_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[agent_name] = module
        spec.loader.exec_module(module)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, AgentInterface) and attribute != AgentInterface:
                self.agents[agent_name] = attribute()
                logging.info(f"Loaded agent: {agent_name}")

    def execute_agents(self):
        """Executes all loaded agents concurrently in separate threads."""
        for agent_name, agent_instance in self.agents.items():
            thread = threading.Thread(target=self._execute_single_agent, args=(agent_name, agent_instance,))
            thread.start()
            thread.join()

    def _execute_single_agent(self, agent_name, agent_instance):
        """Handles the lifecycle of a single agent, including initialization, execution, and shutdown."""
        try:
            agent_instance.initialize()
            agent_instance.execute()
            data = agent_instance.get_data()
            logging.info(f"Agent {agent_name} executed successfully with data: {data}")
            agent_instance.shutdown()
        except Exception as e:
            logging.error(f"Error executing agent {agent_name}: {e}")

if __name__ == "__main__":
    mastermind = MASTERMIND()
    mastermind.execute_agents()
    logging.info("All agents have been executed.")
