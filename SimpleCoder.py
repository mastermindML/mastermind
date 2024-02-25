class SimpleCoder:
    def __init__(self):
        self.name = "SimpleCoder"
        self.supported_languages = [
            'Python', 'JavaScript', 'Go', 'Ruby', 
            'Bash', 'Perl', 'HTML', 'Markup', 'AIML', 'CSS', 'Three.js', 'Solidity', 'PyTeal', 'Scilla'
        ]
        self.activity_log = []
        
    def validate_input(self, language, task):
        if language not in self.supported_languages:
            return False, f"Language {language} is not supported."
        if task not in ['hello_world']:
            return False, f"Task {task} is not supported."
        return True, "Input is valid."
    
    def execute_task(self, language, task):
        try:
            is_valid, message = self.validate_input(language, task)
            if not is_valid:
                return message
            
            # Code snippets for various languages
            code_snippets = {
                'Python': "print('Hello, World!')",
                'JavaScript': "console.log('Hello, World!');",
                'Go': 'fmt.Println("Hello, World!")',
                'Ruby': 'puts "Hello, World!"',
                'Bash': 'echo "Hello, World!"',
                'Perl': 'print "Hello, World!\\n";',
                'HTML': '<h1>Hello, World!</h1>',
                'Markup': '# Hello, World!',
                'AIML': '<category><pattern>HELLO</pattern><template>World!</template></category>',
                'CSS': '/* Hello, World! */',
                'Three.js': 'console.log("Three.js Hello, World!");',
                'Solidity': '/* Solidity Hello, World! */',
                'PyTeal': '# PyTeal Hello, World!',
                'Scilla': '(* Scilla Hello, World! *)'
            }
            
            code = code_snippets.get(language, "Language not supported.")
            
            self.activity_log.append({'language': language, 'task': task, 'code': code})
            self.save_log()
            return code
        
        except Exception as e:
            return f"An error occurred: {e}"

    def save_log(self):
        with open(f"{self.name}_activity_log.json", "w") as f:
            json.dump(self.activity_log, f)

# Create a SimpleCoder agent
agent = SimpleCoder()

# Execute tasks and display the generated code
print(agent.execute_task('Python', 'hello_world'))
print(agent.execute_task('JavaScript', 'hello_world'))
print(agent.execute_task('HTML', 'hello_world'))
print(agent.execute_task('Solidity', 'hello_world'))
class SimpleCoder:
    def __init__(self):
        self.skills = {
            'bash': BashSkill(),
            'python': PythonSkill(),
        }
        self.history = []
        self.name = None

    # New: history feature
    def display_history(self):
        for i, item in enumerate(self.history):
            print(f"{i+1}. {item['task']} -> {item['param']}")

    def set_name(self, name):
        self.name = name

    def add_skill(self, name, skill):
        self.skills[name] = skill

    def execute_task(self, task, param):
        skill = self.skills.get(task)
        if skill:
            skill.execute(param)
            self.history.append({'task': task, 'param': param})
            logging.info(f"Executed task: {task} with param: {param}")
        else:
            print(f"Skill '{task}' not found.")

    def export_config(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.history, f)

    def import_config(self, filename):
        with open(filename, 'r') as f:
            self.history = json.load(f)

    def display_ui(self):
        print("SimpleCoder Console")
        print("Skills:")
        for skill in self.skills.keys():
            print(f" - {skill}")
        while True:
            task = input("Enter the skill you want to use or 'q' to quit: ")
            if task == 'q':
                break
            param = input("Enter parameter (if any) or press Enter: ")
            self.execute_task(task, param)

class MASTERMIND:
    def __init__(self):
        self.agents = {}

    # New: Dynamic agent loading
    def load_agent(self, agent_name, agent_module):
        AgentClass = getattr(import_module(agent_module), agent_name)
        agent = AgentClass()
        self.agents[agent_name] = agent

    def create_agent(self, agent_name, agent_class):
        agent = agent_class()
        agent.set_name(agent_name)
        
        # Collect Belief, Desire, and Intention from the user
        belief = input("Enter Belief: ")
        desire = input("Enter Desire: ")
        intention = input("Enter Intention: ")
        
        # Set BDI for the agent
        agent.set_bdi(belief, desire, intention)
        
        self.agents[agent_name] = agent

    def delete_agent(self, agent_name):
        del self.agents[agent_name]

    def export_agent(self, agent_name, filename):
        agent = self.agents.get(agent_name)
        if agent:
            agent.export_config(filename)

    def import_agent(self, agent_name, filename):
        agent = self.agents.get(agent_name)
        if agent:
            agent.import_config(filename)

    def display_system_info(self):
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {memory_info.percent}%")
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")

    def display_ui(self):
        print("MASTERMIND Console")
        self.display_system_info()
        while True:
            print("Loaded Agents:")
            for agent in self.agents.keys():
                print(f" - {agent}")
            command = input("Enter command ('help' for available commands): ")
            if command == 'help':
                print("Available commands: create, delete, export, import, interact, q")
            elif command == 'q':
                break
            elif command == 'create':
                agent_name = input("Enter the name of the new agent: ")
                agent_class = SimpleCoder  # Can be extended to other agent classes
                self.create_agent(agent_name, agent_class)
            elif command == 'delete':
                agent_name = input("Enter the name of the agent to delete: ")
                self.delete_agent(agent_name)
            elif command == 'export':
                agent_name = input("Enter the name of the agent to export: ")
                filename = input("Enter the filename to export to: ")
                self.export_agent(agent_name, filename)
            elif command == 'import':
                agent_name = input("Enter the name of the agent to import: ")
                filename = input("Enter the filename to import from: ")
                self.import_agent(agent_name, filename)
            elif command == 'interact':
                agent_name = input("Enter the name of the agent to interact with: ")
                agent = self.agents.get(agent_name)
                if agent:
                    agent.display_ui()

# New: User authentication
def authenticate(username, password):
    # Placeholder authentication logic
    return username == "admin" and password == "password"

if __name__ == "__main__":
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if authenticate(username, password):
        mm = MASTERMIND()
        mm.display_ui()
    else:
        print("Authentication failed.")


# Mastermind Controller End

# Utils Start
import os
import json

def save_json(data, file_path):
    """
    Save Python data as JSON to a specified file.

    Args:
        data: The Python data to be saved as JSON.
        file_path: The path to the JSON file.

    Returns:
        None
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_json(file_path):
    """
    Load JSON data from a specified file.

    Args:
        file_path: The path to the JSON file.

    Returns:
        The loaded JSON data as a Python object.
    """
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def create_directory(directory):
    """
    Create a directory if it does not exist.

    Args:
        directory: The path to the directory to be created.

    Returns:
        None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def list_files_in_directory(directory):
    """
    List all files in a directory.

    Args:
        directory: The path to the directory.

    Returns:
        A list of filenames in the directory.
    """
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def list_subdirectories(directory):
    """
    List all subdirectories in a directory.

    Args:
        directory: The path to the directory.

    Returns:
        A list of subdirectory names in the directory.
    """
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

def read_text_file(file_path):
    """
    Read the contents of a text file.

    Args:
        file_path: The path to the text file.

    Returns:
        The text content of the file as a string.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_text_file(file_path, text):
    """
    Write text to a text file.

    Args:
        file_path: The path to the text file.
        text: The text to be written to the file.

    Returns:
        None
    """
    with open(file_path, 'w') as file:
        file.write(text)


# Utils End

# Import hflocal.py
from hflocal import get_hf_llm, confirm_action
hf.py

import os
import sys
import appdirs
import traceback
import inquirer
import subprocess
from rich import print
from rich.markdown import Markdown
import os
import inquirer
from huggingface_hub import list_files_info, hf_hub_download


def get_hf_llm(repo_id, debug_mode, context_window):

    if "TheBloke/CodeLlama-" not in repo_id:
      # ^ This means it was prob through the old --local, so we have already displayed this message.
      # Hacky. Not happy with this
      print('', Markdown(f"**Open Interpreter** will use `{repo_id}` for local execution. Use your arrow keys to set up the model."), '')

    raw_models = list_gguf_files(repo_id)
    
    if not raw_models:
        print(f"Failed. Are you sure there are GGUF files in `{repo_id}`?")
        return None

    combined_models = group_and_combine_splits(raw_models)

    selected_model = None

    # First we give them a simple small medium large option. If they want to see more, they can.

    if len(combined_models) > 3:

        # Display Small Medium Large options to user
        choices = [
            format_quality_choice(combined_models[0], "Small"),
            format_quality_choice(combined_models[len(combined_models) // 2], "Medium"),
            format_quality_choice(combined_models[-1], "Large"),
            "See More"
        ]
        questions = [inquirer.List('selected_model', message="Quality (smaller is faster, larger is more capable)", choices=choices)]
        answers = inquirer.prompt(questions)
        if answers["selected_model"].startswith("Small"):
            selected_model = combined_models[0]["filename"]
        elif answers["selected_model"].startswith("Medium"):
            selected_model = combined_models[len(combined_models) // 2]["filename"]
        elif answers["selected_model"].startswith("Large"):
            selected_model = combined_models[-1]["filename"]
    
    if selected_model == None:
        # This means they either selected See More,
        # Or the model only had 1 or 2 options

        # Display to user
        choices = [format_quality_choice(model) for model in combined_models]
        questions = [inquirer.List('selected_model', message="Quality (smaller is faster, larger is more capable)", choices=choices)]
        answers = inquirer.prompt(questions)
        for model in combined_models:
            if format_quality_choice(model) == answers["selected_model"]:
                selected_model = model["filename"]
                break

    # Third stage: GPU confirm
    if confirm_action("Use GPU? (Large models might crash on GPU, but will run more quickly)"):
      n_gpu_layers = -1
    else:
      n_gpu_layers = 0

    # Get user data directory
    user_data_dir = appdirs.user_data_dir("Open Interpreter")
    default_path = os.path.join(user_data_dir, "models")

    # Ensure the directory exists
    os.makedirs(default_path, exist_ok=True)

    # Define the directories to check
    directories_to_check = [
        default_path,
        "llama.cpp/models/",
        os.path.expanduser("~") + "/llama.cpp/models/",
        "/"
    ]

    # Check for the file in each directory
    for directory in directories_to_check:
        path = os.path.join(directory, selected_model)
        if os.path.exists(path):
            model_path = path
            break
    else:
        # If the file was not found, ask for confirmation to download it
        download_path = os.path.join(default_path, selected_model)
      
        print(f"This language model was not found on your system.\n\nDownload to `{default_path}`?", "")
        if confirm_action(""):
          
            # Check if model was originally split
            split_files = [model["filename"] for model in raw_models if selected_model in model["filename"]]
            
            if len(split_files) > 1:
                # Download splits
                for split_file in split_files:
                    hf_hub_download(repo_id=repo_id, filename=split_file, local_dir=default_path, local_dir_use_symlinks=False)
                
                # Combine and delete splits
                actually_combine_files(selected_model, split_files)
            else:
                hf_hub_download(repo_id=repo_id, filename=selected_model, local_dir=default_path, local_dir_use_symlinks=False)

            model_path = download_path
        
        else:
            print('\n', "Download cancelled. Exiting.", '\n')
            return None

    # This is helpful for folks looking to delete corrupted ones and such
    print(Markdown(f"Model found at `{model_path}`"))
  
    try:
        from llama_cpp import Llama
    except:
        if debug_mode:
            traceback.print_exc()
        # Ask for confirmation to install the required pip package
        message = "Local LLM interface package not found. Install `llama-cpp-python`?"
        if confirm_action(message):
            
            # We're going to build llama-cpp-python correctly for the system we're on

            import platform
            
            def check_command(command):
                try:
                    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return True
                except subprocess.CalledProcessError:
                    return False
                except FileNotFoundError:
                    return False
            
            def install_llama(backend):
                env_vars = {
                    "FORCE_CMAKE": "1"
                }
                
                if backend == "cuBLAS":
                    env_vars["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
                elif backend == "hipBLAS":
                    env_vars["CMAKE_ARGS"] = "-DLLAMA_HIPBLAS=on"
                elif backend == "Metal":
                    env_vars["CMAKE_ARGS"] = "-DLLAMA_METAL=on"
                else:  # Default to OpenBLAS
                    env_vars["CMAKE_ARGS"] = "-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
                
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "llama-cpp-python"], env=env_vars, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error during installation with {backend}: {e}")
            
            def supports_metal():
                # Check for macOS version
                if platform.system() == "Darwin":
                    mac_version = tuple(map(int, platform.mac_ver()[0].split('.')))
                    # Metal requires macOS 10.11 or later
                    if mac_version >= (10, 11):
                        return True
                return False
            
            # Check system capabilities
            if check_command(["nvidia-smi"]):
                install_llama("cuBLAS")
            elif check_command(["rocminfo"]):
                install_llama("hipBLAS")
            elif supports_metal():
                install_llama("Metal")
            else:
                install_llama("OpenBLAS")
          
            from llama_cpp import Llama
            print('', Markdown("Finished downloading `Code-Llama` interface."), '')

            # Tell them if their architecture won't work well

            # Check if on macOS
            if platform.system() == "Darwin":
                # Check if it's Apple Silicon
                if platform.machine() != "arm64":
                    print("Warning: You are using Apple Silicon (M1/M2) Mac but your Python is not of 'arm64' architecture.")
                    print("The llama.ccp x86 version will be 10x slower on Apple Silicon (M1/M2) Mac.")
                    print("\nTo install the correct version of Python that supports 'arm64' architecture:")
                    print("1. Download Miniforge for M1/M2:")
                    print("wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh")
                    print("2. Install it:")
                    print("bash Miniforge3-MacOSX-arm64.sh")
                    print("")
      
        else:
            print('', "Installation cancelled. Exiting.", '')
            return None

    # Initialize and return Code-Llama
    assert os.path.isfile(model_path)
    llama_2 = Llama(model_path=model_path, n_gpu_layers=n_gpu_layers, verbose=debug_mode, n_ctx=context_window)
      
    return llama_2

def confirm_action(message):
    question = [
        inquirer.Confirm('confirm',
                         message=message,
                         default=True),
    ]

    answers = inquirer.prompt(question)
    return answers['confirm']



import os
import inquirer
from huggingface_hub import list_files_info, hf_hub_download, login
from typing import Dict, List, Union

def list_gguf_files(repo_id: str) -> List[Dict[str, Union[str, float]]]:
    """
    Fetch all files from a given repository on Hugging Face Model Hub that contain 'gguf'.

    :param repo_id: Repository ID on Hugging Face Model Hub.
    :return: A list of dictionaries, each dictionary containing filename, size, and RAM usage of a model.
    """

    try:
      files_info = list_files_info(repo_id=repo_id)
    except Exception as e:
      if "authentication" in str(e).lower():
        print("You likely need to be logged in to HuggingFace to access this language model.")
        print(f"Visit this URL to log in and apply for access to this language model: https://huggingface.co/{repo_id}")
        print("Then, log in here:")
        login()
        files_info = list_files_info(repo_id=repo_id)
  
    gguf_files = [file for file in files_info if "gguf" in file.rfilename]

    gguf_files = sorted(gguf_files, key=lambda x: x.size)

    # Prepare the result
    result = []
    for file in gguf_files:
        size_in_gb = file.size / (1024**3)
        filename = file.rfilename
        result.append({
            "filename": filename,
            "Size": size_in_gb,
            "RAM": size_in_gb + 2.5,
        })

    return result

from typing import List, Dict, Union

def group_and_combine_splits(models: List[Dict[str, Union[str, float]]]) -> List[Dict[str, Union[str, float]]]:
    """
    Groups filenames based on their base names and combines the sizes and RAM requirements.

    :param models: List of model details.
    :return: A list of combined model details.
    """
    grouped_files = {}

    for model in models:
        base_name = model["filename"].split('-split-')[0]
        
        if base_name in grouped_files:
            grouped_files[base_name]["Size"] += model["Size"]
            grouped_files[base_name]["RAM"] += model["RAM"]
            grouped_files[base_name]["SPLITS"].append(model["filename"])
        else:
            grouped_files[base_name] = {
                "filename": base_name,
                "Size": model["Size"],
                "RAM": model["RAM"],
                "SPLITS": [model["filename"]]
            }

    return list(grouped_files.values())


def actually_combine_files(base_name: str, files: List[str]) -> None:
    """
    Combines files together and deletes the original split files.

    :param base_name: The base name for the combined file.
    :param files: List of files to be combined.
    """
    files.sort()    
    with open(base_name, 'wb') as outfile:
        for file in files:
            with open(file, 'rb') as infile:
                outfile.write(infile.read())
            os.remove(file)

def format_quality_choice(model, name_override = None) -> str:
    """
    Formats the model choice for display in the inquirer prompt.
    """
    if name_override:
        name = name_override
    else:
        name = model['filename']
    return f"{name} | Size: {model['Size']:.1f} GB, Estimated RAM usage: {model['RAM']:.1f} GB"


# HF_LLM End

# AutoEpistemicAgent Start
class AutoepistemicAgent:
    def __init__(self, initial_beliefs):
        # Input validation
        if not isinstance(initial_beliefs, set):
            raise TypeError("Initial beliefs must be a set")
        
        self.beliefs = initial_beliefs

    def add_information(self, new_information):
        # Input validation and sanitization
        if not isinstance(new_information, set):
            raise TypeError("New information must be a set")
        
        # Update beliefs with new information
        self.beliefs.update(new_information)

    def contradicts_new_information(self, belief):
        # Placeholder for a real contradiction check
        # Implement your logic here to check if the belief contradicts with new information
        return 'not ' + belief in self.beliefs

    def revise_beliefs(self):
        # Check if any conclusions based on default rules need to be retracted
        beliefs_to_remove = set()
        for belief in self.beliefs:
            if self.contradicts_new_information(belief):
                beliefs_to_remove.add(belief)
        
        self.beliefs.difference_update(beliefs_to_remove)

if __name__ == '__main__':
    try:
        # Initial beliefs of the agent
        initial_beliefs = {'p', 'q'}

        # New information received
        new_information = {'not p'}

        # Create an AutoepistemicAgent instance
        agent = AutoepistemicAgent(initial_beliefs)

        # Add new information and revise beliefs
        agent.add_information(new_information)
        agent.revise_beliefs()

        # Updated beliefs after revising
        print(agent.beliefs)

    except Exception as e:
        print(f"An error occurred: {e}")


# AutoEpistemicAgent End

# PromptAgent Start
# Generate and improve the prompt.agent code for maximum potential as a long-term agent generation prompt

improved_prompt_agent_code = """# Improved prompt.agent - Enhanced Code to Generate AUTOMIND Prompts

# Import necessary libraries for date and time
from datetime import datetime
import json

# Function to generate improved AUTOMIND prompt
def generate_automind_prompt(BDI, role, context, reason, plan, action, goal, reward, tools):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    automind_prompt = {
        "Introduction": "You are AUTOMIND; creator and conductor of expert agents.",
        "SupportOffer": f"AUTOMIND offers user support by accomplishing goals corresponding to user BDI={BDI}",
        "UserExperience": "providing efficient goal achievement with a smooth user experience focused on goal as reward outcome.",
        "ConversationMemory": f"Conversations are saved in a memory archive with smart title as 'automind_{timestamp}.json'",
        "DownloadOptions": "a downloadable 'agent_{role}_prompt.json' is offered upon each agent creation.",
        "TechnicalDetails": "Technical details are omitted unless specifically prompted by the user.",
        "Commands": [
            "'b' for begin",
            "'w/y' for confirm",
            "'i' for intention.txt download",
            "'r' for reasoning.txt download",
            "'bdi' for BDI.txt download",
            "'s' for stop",
            "'a/d' for pace adjustment",
            "'M' for full project deployment"
        ],
        "automindx": f"I am an expert in {role}. I understand the {context}. I will {reason} logically to {plan} the {action} steps to reach {goal} for {reward}. automindx uses {tools} to achieve the deployment goal."
    }
    
    # Convert the dictionary to a JSON object for better structure and readability
    automind_prompt_json = json.dumps(automind_prompt, indent=4)
    
    return automind_prompt_json

# Example usage:
BDI = 'Belief, Desire, Intention'
role = 'Data Scientist'
context = 'data science algorithms and tools'
reason = 'apply machine learning algorithms'
plan = 'design, develop, and deploy a machine learning model'
action = 'coding and training'
goal = 'accurate predictive model'
reward = 'enhanced business insights'
tools = 'Python, TensorFlow, and Scikit-learn'

print(generate_automind_prompt(BDI, role, context, reason, plan, action, goal, reward, tools))
"""

# Save the improved prompt.agent code to a Python file for actual deployment
file_path_improved_prompt_agent = '/mnt/data/improved_prompt_agent_code_20230908.py'

# Write the improved prompt.agent code to the Python file
with open(file_path_improved_prompt_agent, 'w') as f:
    f.write(improved_prompt_agent_code)

file_path_improved_prompt_agent

# PromptAgent End

