from dotenv import load_dotenv, set_key
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


console = Console()


def setup_env_file():
    if not os.path.exists('.env'):
        console.print("[yellow]No .env file found. Let's create one![/yellow]")
        api_choice = console.input(
            "Which API would you like to use? (1) Claude AI, (2) OpenAI: ")

        if api_choice == '1':
            key = console.input("Please enter your Claude AI API key: ")
            set_key('.env', 'ANTHROPIC_API_KEY', key)
            console.print(
                "[green]Claude AI API key has been saved to .env file.[/green]")
        elif api_choice == '2':
            key = console.input("Please enter your OpenAI API key: ")
            set_key('.env', 'OPENAI_API_KEY', key)
            console.print(
                "[green]OpenAI API key has been saved to .env file.[/green]")
        else:
            console.print(
                "[bold red]Invalid choice. Please run the script again and choose 1 or 2.[/bold red]")
            sys.exit(1)

    load_dotenv()


setup_env_file()

# Check for API keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize clients based on available API keys
if ANTHROPIC_API_KEY:
    from anthropic import Anthropic
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    API_IN_USE = "Claude AI"
elif OPENAI_API_KEY:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    API_IN_USE = "OpenAI"
else:
    console.print(
        "[bold red]Error: No API key found in the .env file.[/bold red]")
    console.print("Please run the script again to set up your API key.")
    sys.exit(1)


@click.command()
@click.option('--repo-path', default='.', help='Path to the git repository')
@click.option('--branch', default='HEAD', help='Branch to analyze')
@click.option('--count', default=5, help='Number of recent commits to analyze')
@click.option('--prefix', default='', help='Prefix to add to all commit messages')
def improve_commit_messages(repo_path, branch, count, prefix):
    console.print(
        f"[bold green]Using {API_IN_USE} for commit message generation.[/bold green]")
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits(branch, max_count=count))

    for commit in commits:
        diff = repo.git.show(commit.hexsha, format='%b')
        original_message = commit.message.strip()
        new_message = generate_commit_message(diff)
        new_message_with_prefix = add_prefix(new_message, prefix)
        decision = present_changes_and_get_decision(
            commit, original_message, new_message_with_prefix)

        if decision == 'accept':
            update_commit_message(repo, commit, new_message_with_prefix)
        elif decision == 'update':
            updated_message = click.edit(new_message_with_prefix)
            if updated_message:
                update_commit_message(repo, commit, updated_message)


def generate_commit_message(diff):
    prompt = f"""
    Based on the following git diff, generate a concise and informative commit message.
    The message should summarize the main changes and their purpose.
    Keep the message under 72 characters if possible.
    Do not include any explanations, just the commit message itself.

    Git diff:
    {diff}
    """

    if API_IN_USE == "Claude AI":
        return generate_commit_message_claude(prompt)
    else:
        return generate_commit_message_openai(prompt)


def generate_commit_message_claude(prompt):
    try:
        message = anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        console.print(
            f"[bold red]Error generating commit message with Claude AI: {str(e)}[/bold red]")
        return f"Error generating commit message: {str(e)}"


def generate_commit_message_openai(prompt):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates concise and informative git commit messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        console.print(
            f"[bold red]Error generating commit message with OpenAI: {str(e)}[/bold red]")
        return f"Error generating commit message: {str(e)}"


def add_prefix(message, prefix):
    if prefix:
        return f"{prefix} {message}"
    return message


def present_changes_and_get_decision(commit, original_message, new_message):
    console.print("\n" + "="*50)
    console.print(
        Panel(f"[bold cyan]Commit:[/bold cyan] {commit.hexsha[:7]}", expand=False))

    console.print("[bold]Original Message:[/bold]")
    console.print(Panel(Syntax(original_message, "text",
                  theme="monokai", word_wrap=True), expand=False))

    console.print("\n[bold]Suggested Message:[/bold]")
    console.print(Panel(Syntax(new_message, "text",
                  theme="monokai", word_wrap=True), expand=False))

    while True:
        decision = console.input(
            "\n[bold yellow]What would you like to do?[/bold yellow]\n"
            "(a) Accept suggested message\n"
            "(u) Update suggested message\n"
            "(s) Skip this commit\n"
            "(d) Show diff\n"
            "Your choice [a/u/s/d]: "
        ).lower()

        if decision == 'd':
            show_diff(commit)
        elif decision in ['a', 'u', 's']:
            return {'a': 'accept', 'u': 'update', 's': 'skip'}[decision]
        else:
            console.print(
                "[bold red]Invalid choice. Please enter 'a', 'u', 's', or 'd'.[/bold red]")


def show_diff(commit):
    diff = commit.repo.git.show(commit.hexsha, format="")
    console.print("\n[bold]Commit Diff:[/bold]")
    console.print(Panel(Syntax(diff, "diff", theme="monokai",
                  line_numbers=True, word_wrap=True), expand=False))
    console.input("\nPress Enter to continue...")


def update_commit_message(repo, commit, new_message):
    try:
        repo.git.commit('--amend', '-m', new_message)
        console.print(
            f"[bold green]Successfully updated commit {commit.hexsha[:7]} with new message:[/bold green]")
        console.print(Panel(new_message, border_style="green"))
    except git.GitCommandError as e:
        console.print(
            f"[bold red]Error updating commit message: {e}[/bold red]")


def main():
    console.print("[bold blue]Welcome to LogPolish![/bold blue]")
    console.print("Let's improve your commit messages.\n")
    improve_commit_messages()


if __name__ == '__main__':
    main()
