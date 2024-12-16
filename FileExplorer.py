from datetime import datetime
import subprocess
from Files import *
from Trash import *
import pickle


'''
This project aims the implement a file explorer in python
        The file explorer uses two primary data structures to represent the system.
                ->N-ary Tree
                    -->N-ary tree structure is used to represent the directories where each node in a
                        tree represents a directory.
                ->Linked Lists
                    -->Linked lists are used to represent the files inside the folder i.e. the files 
                        withing a directory are stored as linked list.Each file is node in this linked list.        
'''

class FileExplorer:

    def save_state(self, filename="file_explorer_state.pkl"):
        """Save the current state of the FileExplorer to a file."""
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        print("State saved successfully.")

    @classmethod
    def load_state(cls, filename="file_explorer_state.pkl"):
        """Load the FileExplorer state from a file."""
        try:
            with open(filename, "rb") as f:
                print("State loaded successfully.")
                return pickle.load(f)
        except FileNotFoundError:
            print("No previous state found. Starting a new file explorer.")
            return cls()  # Return a new instance if no file exists

    class Node:
        def __init__(self, name):
            self.name = name
            self.num_items = 0
            self.date = [datetime.now(), datetime.now()]
            self.child_directories = []
            self.path = []
            self.files = Files()
            self.parent = None

    def __init__(self):
        self.root = self.Node("Home")
        self.total_directories = 0
        self.trash = Trash()

    #Time Complexity:O(n)
    def mkdir(self, cur_dir: Node, folder_name: str):
        if folder_name == "":
            print("mkdir: enter valid name.")
            return
        for folder in cur_dir.child_directories:
            if folder.name == folder_name:
                print("\033[31m" + f"mkdir: cannot create directory ‘{folder_name}’: File exists")
                return

        cur_dir.date[1] = datetime.now()

        ins_folder = self.Node(folder_name)
        ins_folder.parent = cur_dir
        ins_folder.path = [i for i in cur_dir.path]
        ins_folder.path.append(cur_dir)

        # Add the new folder to the current directory's children
        cur_dir.child_directories.append(ins_folder)
        cur_dir.num_items += 1

        # Update total directories count
        self.total_directories += 1

        print(f"Directory '{folder_name}' created successfully.")

    #Time Complexity:O(n+m)
    def ls(self, cur_dir: Node):  # Displays the contents of the current directory
        """Lists the contents of the current directory."""

        if not cur_dir.child_directories and cur_dir.files.size == 0:
            print(f"ls: Directory '{cur_dir.name}' is empty.")
            return

        # Display subdirectories
        if cur_dir.child_directories:
            print("Directories:")
            for folder in cur_dir.child_directories:
                print(f"  {folder.name}")

        # Display files in the directory (using the linked list in Files)
        if cur_dir.files.size > 0:
            print("\nFiles:")
            cur_node = cur_dir.files.head
            while cur_node:
                print(f"  {cur_node.file_name}")
                cur_node = cur_node.next

    #Time complexity:O(n)
    def cd(self, cur_dir: Node, folder_name: str) -> Node: #used to change directory
        """Change the current working directory to the given folder."""

        # If the folder name is '..', go up to the parent directory
        if folder_name == "..":
            if cur_dir.parent:
                return cur_dir.parent
            else:
                return cur_dir
        # If the folder name is '/', go up to the root directory
        elif folder_name == "/":
            return self.root

        # Check if the folder exists in the current directory
        for folder in cur_dir.child_directories:
            if folder.name == folder_name:
                return folder

        # If the folder was not found in the current directory
        print(f"Directory '{folder_name}' not found.")
        return cur_dir  # Stay in the current directory if not found

    #Time complexity:O(m),m-number of files in cur_dir.files
    def rm(self,cur_dir: Node, file_name: str):#used to remove files(no need to write code to remove directory in this func)
        """Remove a file from the current directory."""

        # Check if the file exists in the current directory
        if self.trash.add_to_trash(file_name):  # Call the remove method on the files linked list of the current directory
            print(f"File '{file_name}' removed successfully.")
        else:
            print("\033[31m" + f"File '{file_name}' not found in '{cur_dir.name}'.")

    # Time complexity:O(n)
    def rmdir(self, cur_dir: Node, folder_name: str): #used to remove directory
        for folder in cur_dir.child_directories:
            if folder.name == folder_name:
                cur_dir.child_directories.remove(folder)
                self.trash.add_to_trash(folder)
                cur_dir.date[1] = datetime.now()
                cur_dir.num_items -= 1
                return
        print("\033[31m" + f"rmdir: failed to remove '{folder_name}': No such file or directory")


    def sort(self): #sorts the contents of the current directory (tim sort) ! Menu-driven !
        pass

    def find(self, folder_name: str): #searches for a file or a directory from the entire file explorer
        pass

    ##Time complexity:O(n),n-depth of the current directory
    def pwd(self, cur_dir: Node):
        print("/", end="")
        for i in cur_dir.path:
            print(i.name, end="/")
        print(cur_dir.name)

    #Time complexity:O(1)
    def open(self, app: str):
        subprocess.run([app])

    def properties(self, cur_dir: Node):
        print("Folder properties:")
        print(f"    Name: {cur_dir.name}")
        print(f"    Items: {cur_dir.num_items}")
        print(f"    Date created: {cur_dir.date[0]}")
        print(f"    Date modified: {cur_dir.date[1]}")
        print("    Path: ", end="")
        self.pwd(cur_dir)

    # Time complexity:O(n)
    def test_driver(self):
        subprocess.run("aplay .smb_coin.wav", shell = True)
        subprocess.run("neofetch --ascii_colors 6 7 --colors 2 2 2 2", shell = True)
        subprocess.run("figlet FILE EXPLORER | lolcat", shell=True)

        cur_node = self.root
        open_directories = [self.root.name]
        while True:
            command = input("\033[0m" + f"{"/".join(open_directories)}>")
            if command.split()[0] in ["cd", "mkdir", "rmdir", "restore", "nano", "open"] and len(command.split()) < 2:
                print("\033[31m" + f"{command.split()[0]}: missing operand")
                continue
            if command.startswith("cd"):
                if command[3:] == "..":
                    cur_node = self.cd(cur_node, command.split()[1])
                    open_directories.pop()
                elif command[3:] == "/":
                    cur_node = self.cd(cur_node, command.split()[1])
                    open_directories = [self.root.name]
                else:
                    x = self.cd(cur_node, command.split()[1])
                    if x != cur_node:
                        cur_node = x
                        open_directories.append(cur_node.name)
                    else:
                        pass

            elif command.startswith("mkdir"):
                if len(command.split()) == 2:
                    self.mkdir(cur_node, command.split()[1])
                else:
                    self.mkdir(cur_node, "")

            elif command.startswith("ls"):
                self.ls(cur_node)

            elif command.startswith("ppty"):
                self.properties(cur_node)

            elif command.startswith("nano"):
                cur_node.files.nano(command.split()[1])
                cur_node.num_items += 1
                cur_node.date[1] = datetime.now()

            elif command.startswith("rmdir"):
                self.rmdir(cur_node, command.split()[1])

            elif command.startswith("rm"):
                self.rm(cur_node, command.split()[1])

            elif command.startswith("pwd"):
                self.pwd(cur_node)

            elif command.startswith("restore"):
                self.trash.restore(command.split()[1])

            elif command.startswith("trash"):
                self.trash.display()

            elif command.startswith("garbage"):
                self.trash.garbage_collection()

            elif command.startswith("open"):
                self.open(command.split()[1])

            elif command.startswith("cls"):
                subprocess.run(["clear"])

            elif command == "bye" or command == "exit":
                print("bye!")
                break

            else:
                print("\033[31m" + f"command not found: {command.split()[0]}")
                continue


if __name__ == "__main__":
    # Load previous state or create a new one
    explorer = FileExplorer.load_state()

    # Run the test driver to start the application
    try:
        explorer.test_driver()
    finally:
        # Save state on exit
        explorer.save_state()

