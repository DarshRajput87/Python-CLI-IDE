import argparse
import shlex
import ast
import os
import subprocess
from components.header import print_header

# Track the current Python file being edited
current_file = None

def run_command(args_list):
    global current_file

    if not args_list:
        return

    cmd = args_list[0]

    # Directory commands
    if cmd == "cd":
        if len(args_list) < 2:
            print("Usage: cd <directory>")
            return
        try:
            os.chdir(args_list[1])
            print(f"Changed directory to {os.getcwd()}")
        except FileNotFoundError:
            print(f"Directory not found: {args_list[1]}")

    elif cmd == "ls":
        print("\n".join(os.listdir(os.getcwd())))

    # Create new file
    elif cmd == "new":
        if len(args_list) < 2:
            print("Usage: new <file.py>")
            return
        filename = args_list[1]
        current_file = filename
        with open(filename, "w") as f:
            f.write("# New Python file\n")
        print(f"Created new file: {filename}. Now use 'write' to add code.")

    # Edit existing file
    elif cmd == "edit":
        if len(args_list) < 2:
            print("Usage: edit <file.py>")
            return
        filename = args_list[1]
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return
        current_file = filename
        print(f"Editing existing file: {filename}. Current content:\n")
        with open(filename, "r") as f:
            content = f.read()
            print(content)
        print("Now use 'write' to add or modify code.")

    # Write code to current file
    elif cmd == "write":
        if not current_file:
            print("No file selected. Use 'new <file.py>' or 'edit <file.py>' first.")
            return
        print(f"Enter Python code for {current_file}. Type 'END' on a new line to finish.")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        choice = input("Append to file or overwrite? (a/o) [a]: ").strip().lower()
        mode = "a" if choice in ["", "a"] else "w"
        with open(current_file, mode) as f:
            f.write("\n".join(lines) + "\n")
        print(f"Code written to {current_file}.")

    # Run Python file
    elif cmd == "run":
        if len(args_list) < 2:
            if current_file:
                filename = current_file
            else:
                print("Usage: run <file.py>")
                return
        else:
            filename = args_list[1]
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return
        print(f"Running {filename}...\n")
        try:
            subprocess.run(["python", filename], check=False)
        except Exception as e:
            print(f"Error running file: {e}")

    # Built-in CLI commands
    elif cmd in ["run_cli", "build", "help", "status"]:
        parser = argparse.ArgumentParser(description='Python Interactive CLI Parser', prog='cli')
        parser.add_argument('command', choices=['run_cli','build','help','status'])
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-f', '--file', help='Specify a file', default=None)
        try:
            args = parser.parse_args(args_list)
        except SystemExit:
            return

        if args.command == 'run_cli':
            print("Running the project...")
        elif args.command == 'build':
            print("Building the project...")
        elif args.command == 'help':
            parser.print_help()
        elif args.command == 'status':
            print("Project status: All systems operational")
        if getattr(args, 'verbose', False):
            print("Verbose mode enabled!")
        if getattr(args, 'file', None):
            print(f"File specified: {args.file}")

    # About command
    elif cmd == "about":
        print("\n=== CompilerCLI - Python CLI IDE ===")
        print("Designer / Author: Diya Desai")
        print("Version: 1.0.0")
        print("\nServices / Features:")
        print("- Interactive Python CLI IDE")
        print("- File management: new, edit, write, run")
        print("- Syntax checking for Python code")
        print("- Directory navigation: cd, ls")
        print("- Built-in CLI commands: run_cli, build, status, help")
        print("- Multi-use editing and code execution\n")

    # Treat unknown input as Python code for syntax check
    else:
        code_input = " ".join(args_list)
        try:
            ast.parse(code_input)
            print("Python code is valid!")
        except SyntaxError as e:
            print(f"Parser Error: {e}")

def main():
    print_header()
    print("Interactive Python CLI Parser Mini-IDE. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("cli> ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting CLI...")
                break
            if user_input.strip() == "":
                continue
            args_list = shlex.split(user_input)
            run_command(args_list)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit the CLI.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_command(sys.argv[1:])
    else:
        main()
