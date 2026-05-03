<!-- Document top anchor -->

<a id="readme-top"></a>

<!-- Heading -->

<div align="center">

  <img src="pza/resources/images/logo.png" alt="logo" width="200" height="auto" />

  <h1>Pza</h1>

  <div>
    A framework for settings, database, logging, and command line features in Python apps.
  </div>

</div>

<!-- Contents -->

## Table of Contents

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#testing">Testing</a></li>
        <li><a href="#troubleshooting">Troubleshooting</a></li>
      </ul>
    </li>
    <li><a href="#basic-usage">Basic Usage</a></li>
    <li><a href="#advanced-usage">Advanced Usage</a>
      <ul>
        <li><a href="#built-in-arguments">Built-in Arguments</a></li>
        <li><a href="#built-in-commands">Built-in Commands</a></li>
      </ul>
    </li>
    <li><a href="#starter-app-template-usage">Starter App Template Usage</a>
      <ul>
        <li><a href="#template-app-creation-pride">Template App Creation (pride)</a></li>
        <li><a href="#template-app-creation-solo">Template App Creation (solo)</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li>
      <a href="#contributions">Contributions</a>
      <ul>
        <li><a href="#developer-installation">Developer Installation</a></li>
        <li><a href="#conventions">Conventions</a></li>
        <li><a href="#code-of-conduct">Code of Conduct</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- Readme Sections -->

## About the Project

Pza is a framework that provides commonly used features to Python apps via simple recipe dictionary mappings.

### Built With

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)

### Features

#### Settings

- Cross-platform settings stored in OS-standard locations
- JSON-based configuration
- User and session profiles
- Onboarding wizard for intial user setup

#### Database

- SQLite database integration
- Automatic database creation
- Helper function library

#### Logging

- Structured logging
- Console and log file output
- Log file rotation

#### Command Line

- Launch command and argument customization
- Graceful argument parsing
- Dynamic application entry points

#### Templates

- Starter app templates for:
    - Modular Python project with multiple files and folders
    - Self-contained Python app within a single file

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

The Pza framework requires Python and pip with a Python version >= 3.12.1.

### Installation

Simply clone the project and use pip to install in your environment.

From a terminal with your Python interpreter available or virtual environment activated:

```bash
pip install '/path/to/pza'
```

To verify the installation, run the main package `pza` as a module to display the framework name and version number:

```bash
python -m pza
```

To verify the framework can be imported in python, run:

```bash
python -c "import pza; print(pza)"
```

### Testing

The framework includes basic tests that can be run from the command line. For example:

```bash
python -m pza.tests.test_pie
```

The framework will create a test app with logging enabled, create folders for settings and documents, and create a sqlite database file. Test results will be displayed in the terminal.

### Troubleshooting

Verify the Pza package installation. The terminal should display package info and list the package folder in sys.path:

```bash
pip show -f pza

python -m site
```

Verify the python environment where the package is installed is the same environment that is active in the workspace:

```bash
which python

which pip

python -c "import pza; print(pza)"
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Basic Usage

Basic usage involves defining an app recipe dictionary and creating an instance of the AppHub class.

```python
# Import framework
import pza.pie

# Define app spec
def get_app_recipe() -> dict:
    """
    Defines app specifications.
    """
    recipe = {
        "name": "test_app",
        "display_name": "Test App",
        "version": "0.4.6",
    }
    return recipe

# Initialize app features
CurrentAppHub = pza.pie.AppHub(get_app_recipe())

# Display app info
CurrentAppHub.list()

# Test logging
CurrentAppHub.logger.info("foo")

# Access app folders and files
print(f"App Settings Folder: {CurrentAppHub.settings_folder}")
print(f"Profile Settings Folder: {CurrentAppHub.profile_settings_folder}")
print(f"App Documents Folder: {CurrentAppHub.settings.get_app_documents_folder()}")
print(f"Profile Documents Folder: {CurrentAppHub.settings.get_profile_documents_folder()}")
print(f"App Database File: {CurrentAppHub.database_file}")
print(f"Database Created: {CurrentAppHub.database.database_created}")

```

The AppHub constructor `pza.pie.AppHub()` will automatically enable logging, settings, and database features, accessible through the current AppHub instance.

The minimum requirement to enable these features is an app name in the recipe. Everything else is optional. Additional sub-recipes can be included to enable app-specific settings, an onboarding setup wizard, automatic database creation, and command line interface with arguments.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Advanced Usage

Command line interface features can be enabled using the recommended project directory structure with a toml file for installation as a python package.

```
/path/to/hello_world/
/path/to/hello_world/pyproject.toml
/path/to/hello_world/hello_world/__main__.py
```

The main python code file contains the framework interface launcher with a call to `pza.interface.run()`. The app recipe, command line argument specification, and entry point functions can be defined in this file or other .py files.

The app recipe `entry_point` and command recipe `callback` specify the paths to special entry point functions in the package. These functions should take an AppHub object as the first parameter and any recipe defined arguments as additional parameters.

This example demonstrates a `hello_world` command line app with the commands: `echo`, `config`, and `test`.

```python
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
    The command `echo` is specified by the app recipe `command_recipe`.
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

```

The pyproject.toml file registers the command line interface launcher for the app in the `[project.scripts]` section. In this example, the app name `hello_world` points to the `main` function in the `__main__` file in the `hello_world` package using the format `package.module:function`.

```
# /hello_world/pyproject.toml

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "hello_world"
version = "0.4.6"
description = "Usage example app."
requires-python = ">=3.12.1"

[tool.setuptools.packages.find]
where = ["."]
include = ["hello_world*"]

[tool.setuptools]
package-dir = {"" = "."}

[project.scripts]
hello_world = "hello_world.__main__:main"
```

Install from the root folder that contains the toml file. Use the `-e` flag to install in developer mode for changes to be automatically recognized without needing reinstallation.

```bash
cd /path/to/hello_world

pip install -e .
```

Run the app with the main entry point, built-in commands, or custom commands defined in the app recipe. For the entry point or custom commands, the interface will run the corresponding callback function, passing in an initialized AppHub object and relevant arguments.

```bash
python -m hello_world
```

```bash
python -m hello_world test
```

```bash
python -m hello_world config --list
```

```bash
python -m hello_world echo --input foo
```

### Built-in Arguments

Universal arguments available to any app using the framework with `pza.interface.run()` are:

- `--debug`
- `--profile`
- `--override`

These arguments must come first when running the app, before the commmand and app-specific arguments.

The `--debug` argument elevates the log level for a current session:

```bash
python -m hello_world --debug echo --input foo
```

The `--profile` argument enables running the app with unique configurations in different sessions. A profile of `default` is used if no `--profile` is given. New profiles are created automatically the first time they are used. To run a session with settings stored under a `developer` profile, use `--profile developer`:

```bash
python -m hello_world --profile developer
```

The `--override` argument enables running the app with a temporary setting override that applies only for a current session. The format is `--override setting_name temporary_value`. To run a session with data files saved to a specific folder, use `--override app_documents_folder`:

```bash
python -m hello_world --override app_documents_folder '/path/to/temp/folder'
```

Multiple overrides can be specified for a single session:

```bash
python -m hello_world --override app_documents_folder '/path/to/temp/folder' --override profile_documents_folder '/path/to/other/folder'
```

### Built-in Commands

Universal commands available to any app using the framework with `pza.interface.run()` are:

- `test`
- `config`

The `test` command runs a set of built-in tests or calls a test entry point function if one is specified in the app recipe `test_entry_point`.

```bash
python -m hello_world test
```

The `config` command runs a built-in settings task. Arguments for this command are:

- `--setup`
- `--list`
- `--set`
- `--get`
- `--reset`
- `--delete-profile`
- `--copy-profile`

To run the onboarding setup wizard for the default profile:

```bash
python -m hello_world config --setup
```

To display all current settings for a specific profile:

```bash
python -m hello_world --profile developer config --list
```

To change a setting permanently for the default profile:

```bash
python -m hello_world config --set app_documents_folder '/path/to/new/folder'
```

To change a setting permanently for a specific profile:

```bash
python -m hello_world --profile developer config --set app_documents_folder '/path/to/dev/folder'
```

To copy settings from an existing `developer` profile to a new `user` profile:

```bash
python -m hello_world config --copy-profile developer user
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Starter App Template Usage

Included starter app templates are:

- Capture the Pride Flag (`pride`)
- Solo (`solo`)

Both apps demonstrate the settings, logging, database, and command line features of the framework. These templates can be used to test the framework or as starting points for customized apps.

Capture the Pride Flag is a modular python package with multiple files and folders that downloads and displays open source pride flag images and information.

Solo is a single file python program that displays information about Han Solo.

### Template App Creation (pride)

To install and run `pride` in a new virtual environment:

```bash
mkdir pride

cd pride

python -m venv .venv

source .venv/bin/activate

pip install --upgrade pip

pip install '/path/to/pza'

python -m pza pride

pip install -e .

python -m pride

python -m pride search --term blue
```

Use the `-e` flag to install in developer mode for changes to be automatically recognized without needing reinstallation. The installation step is necessary for absolute imports to work throughout the project. After customizing the project with a new app name or renamed folders and files, edit the included `pyproject.toml` file to match the changes and run `pip install -e .` again. Then use `python -m new_app_name` to launch the new app.

### Template App Creation (solo)

To install and run `solo` in a new virtual environment:

```bash
mkdir solo

cd solo

python -m venv .venv

source .venv/bin/activate

pip install --upgrade pip

pip install '/path/to/pza'

python -m pza solo

python solo.py

python solo.py burn

python solo.py config --list
```

No additional installation is needed for the single-file template app, since it can be run directly by name and has no absolute imports referencing related files.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

Additional features are planned for implementation in the near future:

- Custom arguments for the main and test entry points
- Generate SQL statements from recipes
- Generate recipes from existing python projects
- Unit testing
- Graphical user interfaces

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributions

Contributions are welcome and appreciated.

### Developer Installation

Developers can install as described in the above <a href="#installation">Installation</a> section, except using the `pip install -e` flag to install in developer mode for changes to be automatically recognized without needing reinstallation. The installation step is necessary for absolute imports to work throughout the project.

```bash
pip install -e '/path/to/pza'
```

### Conventions

- Refer to <a href="https://peps.python.org/pep-0008/">PEP 8</a> for stylistic conventions.

- To keep file and folder item data types clear, the framework consistently uses variable naming conventions:
    - `_file`/`_folder` for path strings
    - `_file_path`/`_folder_path` for pathlib Path objects
    - `_file_io` for file streams

- Type hints are included in function definitions

- Clarity and readability are favored over brevity
    - Variable, class, and function names are descriptive
    - Readable algorithms are preferred over complex one-liners

- Comments may describe:
    - *WHAT* the code is doing
    - *WHY* the code is implemented a particular way
    - *HOW* the code is working

### Code of Conduct

Please be kind, respectful, and honest.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Pza is distributed under the MIT license. See `LICENSE.txt` for details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Aaron Martinez - [@martinezcode](https://www.linkedin.com/in/martinezcode/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

The Capture the Pride Flag template includes an option to download sample data from the Pride Flag Identification Guide at [emily-noble/prideflagsearch](https://github.com/emily-noble/prideflagsearch), licensed under the [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). Data and images are fetched dynamically and are not redistributed in this repository.

The logo image was created by [@Deans_Icons](https://pixabay.com/users/deans_icons-2620543/) on [Pixabay](https://pixabay.com/illustrations/pizza-pizza-icon-pizza-slice-1428926/), licensed under the [Pixabay Content License](https://pixabay.com/service/license-summary/).

Parts of this project were developed with AI assistance from [ChatGPT](https://chatgpt.com), [Google](https://google.com), and [DuckDuckGo](https://duckduckgo.com/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>
