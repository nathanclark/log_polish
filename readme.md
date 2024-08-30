# 🌟 LogPolish: AI-Powered Git Commit Messages

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

Elevate your Git history with LogPolish - the intelligent CLI tool that transforms your commit messages using the power of AI!

![LogPolish Demo](https://via.placeholder.com/600x300.png?text=LogPolish+Demo+GIF)

## 🚀 Features

- 🤖 Leverages AI (Claude or OpenAI) to generate concise and informative commit messages
- 🔄 Interactive mode for reviewing and updating suggested messages
- 🔍 Diff viewer for informed decision-making
- 🏷️ Custom prefix support for standardized commit messages
- 🔐 Secure API key management with .env file
- 🔀 Supports multiple Git branches
- 🎨 Rich, colorful console output for better readability

## 🛠️ Installation

1. Clone the repository:

   ```
   git clone https://github.com/nathanclark/logpolish.git
   cd logpolish
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up your API key:
   Run the script and follow the prompts to set up your Claude AI or OpenAI API key:
   ```
   python logpolish.py
   ```

## 💻 Usage

Basic usage:

```
python logpolish.py --repo-path /path/to/your/repo --branch main --count 5 --prefix "[FEATURE]"
```

Options:

- `--repo-path`: Path to the Git repository (default: current directory)
- `--branch`: Branch to analyze (default: HEAD)
- `--count`: Number of recent commits to analyze (default: 5)
- `--prefix`: Prefix to add to all commit messages (optional)

## 📘 How It Works

1. LogPolish analyzes recent commits in your specified Git branch.
2. It uses AI to generate improved commit messages based on the diff.
3. You can review, accept, update, or skip each suggested message.
4. Accepted messages are automatically applied to your Git history.

## 🗑️ Uninstallation

You can uninstall LogPolish either manually or by using the provided uninstall script.

### Manual Uninstallation

1. Remove the LogPolish directory:

   ```
   rm -rf /path/to/logpolish
   ```

2. Remove the .env file if you want to delete your API keys:

   ```
   rm /path/to/.env
   ```

3. Optionally, uninstall the dependencies if you don't need them for other projects:
   ```
   pip uninstall -r requirements.txt -y
   ```

### Automated Uninstallation

We provide an `uninstall.py` script for easy removal of LogPolish:

1. Navigate to the LogPolish directory:

   ```
   cd /path/to/logpolish
   ```

2. Run the uninstall script:
   ```
   python uninstall.py
   ```

This script will remove the LogPolish files, the .env file, and optionally uninstall the dependencies.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Click](https://click.palletsprojects.com/) for the CLI interface
- [Rich](https://rich.readthedocs.io/) for beautiful terminal formatting
- [GitPython](https://gitpython.readthedocs.io/) for Git integration
- [Anthropic](https://www.anthropic.com/) and [OpenAI](https://openai.com/) for AI capabilities

---

Made with ❤️ by Nathan

Give your Git logs a polish with LogPolish! ✨
