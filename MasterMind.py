"""
MASTERMIND Cognitive Framework v3.1
Production-Grade Autonomous Agent Orchestration System
"""

import os
import sys
import asyncio
import signal
import json
import logging
import psutil
import aiohttp
from dataclasses import dataclass, field
from typing import Dict, List, Set, Any, Optional, AsyncGenerator
from contextlib import asynccontextmanager

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s|%(name)s|%(levelname)s|%(message)s',
    handlers=[
        logging.FileHandler('mastermind.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MASTERMIND')

# --------------------------
# Core Cognitive Architecture
# --------------------------

@dataclass
class Belief:
    content: str
    certainty: float = 1.0
    source: str = "perception"
    dependencies: Set[str] = field(default_factory=set)

@dataclass
class Desire:
    goal: str
    priority: int = 1
    preconditions: Set[str] = field(default_factory=set)
    postconditions: Set[str] = field(default_factory=set)

@dataclass
class Intention:
    plan: List[str]
    current_step: int = 0
    status: str = "pending"

class GoalSystem:
    def __init__(self):
        self.active_goals: List[Desire] = []
        self.completed_goals: List[Desire] = []
        self.failed_goals: List[Desire] = []
        
    async def add_goal(self, goal: Desire):
        """Thread-safe goal addition"""
        if not any(g.goal == goal.goal for g in self.active_goals):
            self.active_goals.append(goal)
            self.active_goals.sort(key=lambda x: x.priority, reverse=True)

# --------------------------
# Asynchronous Agent Base
# --------------------------

class AsyncCognitiveAgent:
    def __init__(self, name: str):
        self.name = name
        self._shutdown_event = asyncio.Event()
        self._task_queue = asyncio.Queue(maxsize=1000)
        self._current_tasks = set()
        self.beliefs: List[Belief] = []
        self.desires: List[Desire] = []
        self.intentions: List[Intention] = []
        
    async def start(self):
        """Start agent's main loop"""
        logger.info(f"Agent {self.name} starting")
        asyncio.create_task(self._run_loop())
        
    async def stop(self):
        """Graceful shutdown"""
        logger.info(f"Agent {self.name} stopping")
        self._shutdown_event.set()
        await self._task_queue.join()
        
    async def _run_loop(self):
        while not self._shutdown_event.is_set():
            task = await self._task_queue.get()
            task_obj = asyncio.create_task(self._execute_task(task))
            self._current_tasks.add(task_obj)
            task_obj.add_done_callback(lambda t: self._current_tasks.discard(t))
            
    async def _execute_task(self, task: Any):
        """Template method for task execution"""
        try:
            await self.perceive(task)
            await self.deliberate()
            return await self.act()
        except Exception as e:
            logger.error(f"Task failed: {str(e)}")
            raise
            
    async def perceive(self, data: Any):
        """Override in subclasses"""
        raise NotImplementedError
        
    async def deliberate(self):
        """BDI decision cycle"""
        raise NotImplementedError
        
    async def act(self) -> Any:
        """Action implementation"""
        raise NotImplementedError
        
    async def get_metrics(self) -> Dict[str, Any]:
        """Agent performance metrics"""
        proc = psutil.Process()
        return {
            "cpu": proc.cpu_percent(),
            "memory": proc.memory_info().rss,
            "queue_size": self._task_queue.qsize(),
            "active_tasks": len(self._current_tasks)
        }

# --------------------------
# Control Plane
# --------------------------

class MastermindController:
    def __init__(self):
        self.agents: Dict[str, AsyncCognitiveAgent] = {}
        self._shutdown_event = asyncio.Event()
        self._monitor_task: Optional[asyncio.Task] = None
        
    def _setup_signals(self):
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self.graceful_shutdown)
            
    async def add_agent(self, agent: AsyncCognitiveAgent):
        """Register and start agent"""
        self.agents[agent.name] = agent
        await agent.start()
        logger.info(f"Agent {agent.name} registered")
        
    async def monitor_system(self):
        """Resource monitoring coroutine"""
        while not self._shutdown_event.is_set():
            try:
                metrics = {}
                for name, agent in self.agents.items():
                    metrics[name] = await agent.get_metrics()
                
                sys_metrics = {
                    "cpu": psutil.cpu_percent(),
                    "memory": psutil.virtual_memory().percent,
                    "agents": len(self.agents)
                }
                
                logger.info("System Metrics: %s", json.dumps(sys_metrics))
                logger.debug("Agent Metrics: %s", json.dumps(metrics))
                
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
                
    @asynccontextmanager
    async def lifecycle(self) -> AsyncGenerator[None, None]:
        """Managed execution context"""
        self._setup_signals()
        self._monitor_task = asyncio.create_task(self.monitor_system())
        try:
            yield
        finally:
            await self.graceful_shutdown()
            
    async def graceful_shutdown(self):
        """Orderly shutdown procedure"""
        logger.info("Initiating shutdown sequence")
        self._shutdown_event.set()
        
        if self._monitor_task:
            self._monitor_task.cancel()
            
        shutdown_tasks = [agent.stop() for agent in self.agents.values()]
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        logger.info("Shutdown complete")

# --------------------------
# Example Agent Implementation
# --------------------------

class SimpleCoder(AsyncCognitiveAgent):
    def __init__(self):
        super().__init__("SimpleCoder")
        self.skills = {
            "python": self._handle_python,
            "javascript": self._handle_js
        }
        
    async def perceive(self, task: Dict):
        """Process incoming task"""
        logger.info(f"Received task: {task['id']}")
        
    async def deliberate(self):
        """Decision making"""
        if len(self.intentions) == 0:
            self.intentions.append(Intention(
                plan=["analyze", "generate", "test"]
            ))
            
    async def act(self) -> Dict:
        """Execute coding task"""
        current_step = self.intentions[0].current_step
        step_name = self.intentions[0].plan[current_step]
        
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                "https://api.codegen.com/tasks",
                json={"step": step_name}
            )
            result = await response.json()
            
        self.intentions[0].current_step += 1
        return result
        
    async def _handle_python(self, task: Dict):
        """Python-specific handling"""
        pass
        
    async def _handle_js(self, task: Dict):
        """JavaScript handling"""
        pass

# --------------------------
# Main Execution
# --------------------------

async def main():
    controller = MastermindController()
    
    async with controller.lifecycle():
        # Register agents
        coder = SimpleCoder()
        await controller.add_agent(coder)
        
        # Keep alive
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System terminated by user")
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        sys.exit(1)
