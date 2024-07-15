import subprocess
import os

def run_pip_command(command):
    """Function to run a pip command."""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(stdout)
        else:
            print(f"Error: {stderr}")
    except Exception as e:
        print(f"Failed to execute '{command}': {e}")

if __name__ == "__main__":
    print("\nWelcome to the pip shell interface!")
    print("Script By @yogakokxd")
    print("Type pip install <package> to install module")
    print("Type 'exit' to quit.")
    
    while True:
        command = input(">> ")
        
        if command.lower() == 'exit':
            print("Exiting the pip shell. Goodbye!")
            break
        elif command.startswith("pip"):
            run_pip_command(command)
        else:
            print("Invalid command. Please use 'pip install package_name' or 'exit' to quit.")
