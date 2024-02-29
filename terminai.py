import curses
import requests
import os
import subprocess

def get_api_key():
    env_file = './.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            return file.read().strip()
    else:
        api_key = input("Enter your OpenAI API key: ").strip()
        with open(env_file, 'w') as file:
            file.write(api_key)
        return api_key

class TerminAI:
    def __init__(self, stdscr, api_key):
        self.stdscr = stdscr
        self.api_key = api_key
        self.setup_terminai_folder()
        self.main()

    def setup_terminai_folder(self):
        folder_path = './terminai'
        os.makedirs(folder_path, exist_ok=True)
        os.chmod(folder_path, 0o700)

    def talk_to_ai(self, message):
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        }
        response = requests.post(api_url, headers=headers, json=data)
        response_json = response.json()
        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            return result.stdout + result.stderr
        except subprocess.CalledProcessError as e:
            return f"An error occurred while executing the command: {e}"

    def main(self):
        self.stdscr.clear()
        self.stdscr.addstr("Welcome to TerminAI. Type 'exit' to quit, or type a command to execute it.\n")
        self.stdscr.addstr("AI: How can I assist you today?\n")
        curses.echo()
        self.stdscr.keypad(True)

        while True:
            self.stdscr.addstr("> ")
            input_str = self.stdscr.getstr().decode('utf-8')

            if input_str == 'exit':
                break
            elif input_str.startswith("cmd:"):
                command = input_str[4:]
                output = self.execute_command(command)
                self.stdscr.addstr(f"Executed: {command}\nOutput:\n{output}\n")
            else:
                response = self.talk_to_ai(input_str)
                self.stdscr.addstr(f"AI: {response}\n")

            self.stdscr.refresh()

        self.stdscr.addstr("Goodbye!")
        self.stdscr.refresh()
        self.stdscr.getch()

if __name__ == '__main__':
    api_key = get_api_key()  # Get the API key before initializing curses
    curses.wrapper(TerminAI, api_key)
