import os
import subprocess

try:
    PS1 = input("enter your PS1: ")
    cwd = "."

    while True:
        cmd = input(PS1)

        parts = cmd.strip().split()  # split by spaces

        if len(parts) == 0:
            continue

        if parts[0] == "ls":
            subprocess.run(["ls"])

        if parts[0] == "pwd":
            print(os.getcwd())

        if parts[0] == "cd":
            if len(parts) < 2:
                print("no argument provided.")
            else:
                try:
                    os.chdir(parts[1])
                except FileNotFoundError:
                    print("no such directory.")
        if parts[0] == "exit":
            break
        else:
            output = subprocess.run([parts[0]])
            print(output)

except KeyboardInterrupt:
    print("\nBye Bye!")
