# Code for Advanced Usage in README

# /hello_world/hello_world/__main__.py

import pza.interface
from pza.pie import AppHub

# --- App Recipe ---

def get_app_recipe() -> dict:
    """
    Defines app specifications.
    """
    recipe = {
        "name": "hello_world",
        "display_name": "Hello World",
        "version": "0.4.6",
        "entry_point": "__main__.hello",
        "command_recipe": get_command_recipe(),
    }
    return recipe

def get_command_recipe() -> dict:
    """
    Defines command line interface commands and arguments.
    """
    recipe = {
        "echo": {
            "callback": "__main__.echo",
            "help": "Echo the input.",
            "args": [
                {
                    "name": "--input",
                    "type": str,
                    "default": "",
                    "help": "Text to echo"
                },
            ],
        },
    }
    return recipe

# --- Interface Command Handler Callback Functions ---

def hello(HelloHub: AppHub) -> None:
    """
    The main interface entry point.
    Specified by the app recipe `entry_point`.
    This is the default mode if the app is run by name
    with no command given.
    """
    HelloHub.list()
    print()
    print("Hello World!")
    return

def echo(HelloHub: AppHub, input: str | None = None) -> None:
    """
    The echo command interface entry point.
    Specified by the app recipe `command_recipe`.
    This mode is activated with `hello_world echo --input`.
    """
    HelloHub.list()
    print()
    print(input)
    return

# --- Main Program ---

def main() -> None:
    """
    Launches the interface with `pza.interface.run()`.
    Commands defined for this app are: `config`, `test`, `echo`.
    The commands `config` and `test` are provided by the framework.
    The command echo is specified by the app recipe `command_recipe`.
    """
    pza.interface.run(
        get_app_recipe(),
        verbose=False
    )
    return

if __name__ == "__main__":
    """
    Runs the main function to launch the app interface.
    """
    main()
