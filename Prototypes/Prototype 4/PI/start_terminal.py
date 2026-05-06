import subprocess


command = "python main.py"
subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f'{command}; read -p "Press Enter to close..."'])
