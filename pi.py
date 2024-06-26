import sys
import os
import subprocess
import json
import platform
from colorama import Fore, Back, Style, init
import webbrowser
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

import pi_json_helpers as helpers

init()
sys_os = platform.system()

# functions for coloring the text in help and error messages
def color_text(text, color):
  return f'{color}{text}{Style.RESET_ALL}'

def get_cyan_text(text):
    return color_text(text, Fore.CYAN)

# Main switch case for handling the commands based on the user input in the command line.
# Contains error handling in case of invalid commands or missing/excessive arguments, which will default to the help function
def main():
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "-h":
                help()
            case "open":
                if len(sys.argv) == 3:
                    open(sys.argv[2])
                elif len(sys.argv) == 2:
                    print(color_text("Missing alias in command", Fore.RED))
                elif len(sys.argv) == 4 and sys.argv[3] == "-r":
                    open(sys.argv[2], reload=True)
                else:
                    print(color_text("Invalid command!", Fore.RED))
                    help()
            case "add":
                if len(sys.argv) < 4:
                    if sys.argv[2] == ".":
                        add_current_directory()
                    else:
                        add(sys.argv[2])
                else:
                    help()
            case "rm":
                if len(sys.argv) < 4:
                    delete(sys.argv[2])
                else:
                    help()
            case "list":
                list_all()
            case "ask":
                if len(sys.argv) < 3:
                    search()
                else:
                    help()
            case "create":
                if len(sys.argv) < 4:
                    git_create(sys.argv[2])
                else:
                    help()
            case "init":
                if len(sys.argv) < 3:
                    git_init()
                elif len(sys.argv) < 4:
                    git_init(sys.argv[2])
                else:
                    help()
            case _:
                print(color_text("Invalid command!", Fore.RED))
                help()
    else:
        help()

# Help function that displays all usage of this CLI tool, called every time the user enters an invalid command or no command at all
def help():
  print("="*80)
  print("Usage:")
  print(f"   Run {get_cyan_text("'pi add <alias>'")} to add a directory with a new alias")
  print(f"   Run {get_cyan_text("'pi open <alias>'")} to open a previously added directory. Append '-r' to open in the same VScode window")
  print(f"   Run {get_cyan_text("'pi rm <alias>'")} to remove an existing alias")
  print(f"   Run {get_cyan_text("'pi ask'")} to toggle the search mode")
  print(f"   Run {get_cyan_text("'pi init'")} to initialize .git and commit all current content to a remote Github repository")
  print(f"   Run {get_cyan_text("'pi init <repo name>'")} to create a remote Github repository with the name and push all current content to it")

  print("="*80)

# Function to list all the aliases and their corresponding directories
def list_all():
  print(color_text("-----------------LIST-----------------", Fore.CYAN))
  print(helpers.get_all())

# Function to open the directory in VScode based on the alias provided
def open(alias, reload=False):
  project = helpers.get_directory_from_alias(alias)
  if project is None:
    print(color_text(f"Alias {alias} does not point to a directory", Fore.RED))
    return
  if project[0] == "\"" or project[0] == "\'":
    project = project[1:-1]
  try:
    if reload:
      subprocess.run(['code', '-r', project], shell=True)
    else:
      subprocess.run(['code', project], shell=True)
  except Exception as e:
    print(f"Error: {e}")

# Function to add a new alias and directory pair to the JSON file
def add(alias):
  check_dir = helpers.get_directory_from_alias(alias)
  if check_dir is not None:
    print(color_text(f"Alias {alias} already points to {check_dir}", Fore.RED))
    help()
    return
  directory = prompt('Enter the full path: ', completer=PathCompleter(), complete_while_typing=True, complete_in_thread=True)
  if helpers.add_entry(alias, directory):
    print(color_text(f"Successfully added '{alias}' pointing to '{directory}'", Fore.GREEN))
  else:
    print(color_text("Error adding pair", Fore.RED))

# Function to add the current directory to the JSON file
def add_current_directory():
  directory = os.getcwd()
  alias = input("Enter the alias: ")
  check_dir = helpers.get_directory_from_alias(alias)
  if check_dir is not None:
    print(color_text(f"Alias {alias} already points to {check_dir}", Fore.RED))
    help()
    return
  if helpers.add_entry(alias, directory):
    print(color_text(f"Successfully added '{alias}' pointing to '{directory}'", Fore.GREEN))
  else:
    print(color_text("Error adding pair", Fore.RED))

# Function to delete an alias from the JSON file
def delete(alias):
  if helpers.remove_entry(alias):
    print(color_text(f"Alias '{alias}' removed successfully", Fore.GREEN))
  else:
    print(color_text("That alias was not found", Fore.RED))

# Function to toggle the search mode, which will open a new tab in the default browser with the search query
def search():
    query = input("Enter search query: ")
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(search_url)

# Function to create a remote repository on github.com with the name provided
# If the repository is created successfully, it will initialize the current directory as a git repository and push all code to the remote repository
# Will conditionally append the 'wsl' command to the command list if the OS is Windows to run a proper curl command
def git_create(repo_name):
  """
  Function to create the remote repository on github.com named by the parameter
  """
  token = helpers.get_github_token()
  is_private = input("Make this repo public? Default is private. (y): ")
  if(is_private == "yes" or is_private == "y" or is_private == "Yes"):
    is_private = r"false"
  else:
    is_private = r"true"
  command = [
    'curl',
    '-L',
    '-X', 'POST',
    '-H', 'Accept: application/vnd.github+json',
    '-H', f'Authorization: Bearer {token}',
    '-H', 'X-Github-Api-Version: 2022-11-28',
    'https://api.github.com/user/repos',
    '-d', f'{{"name": "{repo_name}", "homepage":"https://github.com", "private":{is_private},"is_template":false}}'
  ]
  if sys_os == "Windows":
    command = ['wsl'] + command
  result = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True)
  stdout, stderr = result.communicate()
  if result.returncode == 0:
    response_data = json.loads(stdout.decode())
    if "message" in response_data and response_data["message"] == "Repository creation failed.":
      print(f"Failed to create repository {repo_name}")
      return False
    else:
      print(f"Repository {repo_name} created successfully")
      return True
    
# Function to initialize a git repository in the current directory if it does not already exist
def git_init(repo_name = None):
  """
  Function to initialize a git repo in the current directory if it does not already exist
  If a repo name is specified in the parameters, it will first create a remote repository under that name, then initialize the current directory and push all code there
  """
  if os.path.exists(".git"):
    print("Git has already been initialized here")
    return
  
  if repo_name is not None:
    if not git_create(repo_name):
      return
  github_link = f"https://github.com/pnavab/{repo_name}.git" if repo_name is not None else None

  try:
    commit_message = "Initial commit from pi cli"
    subprocess.run(["git", "init"], capture_output=True, text=True)
    subprocess.run(["git", "add", "."], capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
    subprocess.run(["git", "branch", "-M", "main"], capture_output=True, text=True)
    github_link = github_link if github_link is not None else input("Enter github remote link: ")
    subprocess.run(["git", "remote", "add", "origin", github_link], capture_output=True, text=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
    print(f"Successfully initialized git repo at {github_link}")
  except Exception as e:
    print("Error initializing git repository")

# Entry point for the script
if __name__ == "__main__":
  main()
