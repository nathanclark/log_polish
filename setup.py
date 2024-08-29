from dotenv import load_dotenv
import git
from rich.syntax import Syntax
from rich.panel import Panel
from rich.console import Console
import click
import sys
import os


def check_libraries():
    required_libraries = {
        'click': 'click',
        'rich': 'rich',
        'git': 'gitpython',
        'anthropic': 'anthropic',
        'openai': 'openai',
        'dotenv': 'python-dotenv'
    }
    missing_libraries = []

    for module, pip_package in required_libraries.items():
        try:
            __import__(module)
        except ImportError:
            missing_libraries.append(pip_package)

    if missing_libraries:
        print("Some required libraries are missing. Please install them using pip:")
        print(f"pip install {' '.join(missing_libraries)}")
        sys.exit(1)


check_libraries()


# Load environment variables from .env file
load_dotenv()

console = Console()

# Check for API keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize clients based on available API keys
if ANTHROPIC_API_KEY:
    from anthropic import Anthropic
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    console.print(
        "[green]Using Claude AI for commit message generation.[/green]")
elif OPENAI_API_KEY:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    console.print("[green]Using OpenAI for commit message generation.[/green]")
else:
    console.print(
        "[bold red]Error: Neither ANTHROPIC_API_KEY nor OPENAI_API_KEY is set in the .env file.[/bold red]")
    console.print(
        "Please create a .env file in the same directory as this script with one of these lines:")
    console.print("  ANTHROPIC_API_KEY=your_claude_api_key_here")
    console.print("  OPENAI_API_KEY=your_openai_api_key_here")
    sys.exit(1)

# ... (rest of the script remains the same)


def main():
    console.print("[bold blue]Welcome to LogPolish![/bold blue]")
    console.print("Let's improve your commit messages.\n")
    improve_commit_messages()


if __name__ == '__main__':
    main()
