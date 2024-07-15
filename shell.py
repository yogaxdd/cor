import subprocess
import os

print("<!> Please Wait...")
run_shell_command('git clone https://github.com/dylanaraps/neofetch.git')
print("<!> Please Wait...")
os.chdir('neofetch')
print("<!> Please Wait...")
run_shell_command('chmod +x neofetch')
print("[+] Done")
run_shell_command('./neofetch')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_shell_command(command):
    """Function to run a shell command and print its output."""
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
    
    print("Welcome to the Python Shell Interface!")
    print("Script By : @yogakokxd")
    print("Type 'run-script' to run script bot")
    print("Type 'exit' to quit.")
    
    while True:
        command = input(">> ")
        
        if command.lower() == 'exit':
            print("Exiting the shell. Goodbye!")
            break
        elif command.lower() == 'run-script':
            # Clone the Neofetch repository and run it
            run_shell_command('python main.py')
        else:
            run_shell_command(command)
