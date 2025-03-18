import os
import argparse
import cmd2

# Default values for required variables
host = ""
username = ""
password = ""
ftdname = ""

# Define the available commands
COMMANDS = ["get_configuration", "create_configuration", "delete_configuration"]

class CLI(cmd2.Cmd):
    """Custom CLI for selecting and running commands with tab completion."""

    prompt = "fpcopydevice# "  # CLI prompt
    def cmdloop(self):
        """Override cmdloop to show available commands when '?' is pressed."""
        self.print_help()
        super().cmdloop()

    def print_help(self):
        """Show available commands when '?' is pressed."""
        print("\nAvailable commands:")
        print("  run get-configuration     - Run the get-main program")
        print("  run create-configuration  - Run the create_configuration program")
        print("  run delete-configuration  - Run the delete_configuration program")
        print("  exit             - Exit the CLI\n")

    def do_run(self, line):
        """Run one of the main programs: get-main, create_configuration, delete_configuration."""
        args = line.split()
        if not args:
            self.perror("Please specify a command (get-main, create_configuration, delete_configuration)")
            return
        
        command = args[0]

        if command not in COMMANDS:
            self.perror(f"Invalid command: {command}. Use ? or tab for available commands.")
            return

        
        os.system(f"python3 -m src.{command} --host {host} --username {username} --password {password} --ftdname {ftdname}")

    def complete_run(self, text, line, begidx, endidx):
        """Enable tab completion for available commands."""
        return [cmd for cmd in COMMANDS if cmd.startswith(text)]

    def do_exit(self, line):
        """Exit the CLI."""
        return True

    def do_help(self, line):
        """Show available commands."""
        print("\nAvailable commands:")
        print("  run get-main     - Run the get-main program")
        print("  run create_configuration  - Run the create_configuration program")
        print("  run delete_configuration  - Run the delete_configuration program")
        print("  exit             - Exit the CLI\n")

if __name__ == "__main__":
    CLI().cmdloop()
