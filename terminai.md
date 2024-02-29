# MASTERMIND modular extension
# terminAI

TerminAI is an innovative Python application that merges the power of OpenAI's GPT models with the versatility of the command-line interface, enabling users to interact with advanced AI directly from their terminal and execute shell commands within the same context.

## Features

- **AI Integration**: Engage with OpenAI's GPT models for dynamic conversations.
- **Command Execution**: Seamlessly execute shell commands by prefixing with `cmd:`.
- **Secure API Key Management**: Automates the secure storage of your OpenAI API key for repeated use.

## Getting Started

### Prerequisites

- Python 3.x
- An active internet connection
- An OpenAI API key (obtainable from [OpenAI](https://platform.openai.com/account/api-keys))

### Installation

1. Clone the repository or download `TerminAI.py` directly to your local machine.
2. Install the required Python libraries:

   ```bash
   pip install requests
   ```

   > Note: `curses` is included in the standard library for Unix-based systems. Windows users might need `windows-curses`, installable via pip.

### Configuration

On the first run, you will be prompted to enter your OpenAI API key. This key will be stored locally in a `.env` file for future use, ensuring your sessions remain seamless.

### Running TerminAI

Navigate to the directory containing `TerminAI.py` and execute:

```bash
python3 TerminAI.py
```

Follow the on-screen prompts to start interacting with the AI or execute commands.

## Usage

- **AI Interaction**: Simply type your query and press Enter to receive a response from the AI.
- **Executing Commands**: Type `cmd:` followed by your command to execute it within the terminal.
- **Exiting**: Type `exit` to terminate the session.

## Security

- The `.env` file containing your OpenAI API key is stored locally. Ensure it is securely managed and not exposed to unauthorized parties.
- Exercise caution when executing shell commands, especially those suggested by AI or from untrusted sources, to mitigate potential security risks.

## Troubleshooting

If you encounter issues, particularly with the curses interface, consider trying a different terminal emulator or adjusting your terminal settings. For connectivity issues, verify your internet connection and firewall settings.

## Contributing

Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

[GPLv3](LICENSE)

## Acknowledgments

- OpenAI for providing the GPT models and API.
- The Python community for the invaluable libraries and resources.
