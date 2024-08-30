import os
import shutil
import subprocess


def uninstall_logpolish():
    print("Starting LogPolish uninstallation...")

    # Get the current directory (assuming the script is in the LogPolish directory)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Remove .env file
    env_file = os.path.join(current_dir, '.env')
    if os.path.exists(env_file):
        os.remove(env_file)
        print("Removed .env file.")

    # Ask user if they want to uninstall dependencies
    uninstall_deps = input(
        "Do you want to uninstall the dependencies? (y/n): ").lower() == 'y'
    if uninstall_deps:
        requirements_file = os.path.join(current_dir, 'requirements.txt')
        if os.path.exists(requirements_file):
            try:
                subprocess.run(['pip', 'uninstall', '-r',
                               requirements_file, '-y'], check=True)
                print("Uninstalled dependencies.")
            except subprocess.CalledProcessError:
                print(
                    "Failed to uninstall dependencies. You may need to remove them manually.")
        else:
            print("requirements.txt not found. Skipping dependency uninstallation.")

    # Remove the LogPolish directory
    parent_dir = os.path.dirname(current_dir)
    logpolish_dir = os.path.join(parent_dir, 'logpolish')
    try:
        shutil.rmtree(logpolish_dir)
        print(f"Removed LogPolish directory: {logpolish_dir}")
    except Exception as e:
        print(f"Failed to remove LogPolish directory. Error: {e}")
        print("You may need to remove it manually.")

    print("LogPolish uninstallation completed.")


if __name__ == "__main__":
    uninstall_logpolish()
