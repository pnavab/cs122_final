import sys
import os
import subprocess
from colorama import Fore, Back, Style, init
import pi_json_helpers as helpers
import webbrowser


init()
def color_text(text, color):
  return f'{color}{text}{Style.RESET_ALL}'

# add_color = color_text("'pi add <alias>'", Fore.CYAN)
# open_color = color_text("'pi open <alias>'", Fore.CYAN)
# rm_color = color_text("'pi rm <alias>'", Fore.CYAN)

def get_cyan_text(text):
    return color_text(text, Fore.CYAN)

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
            case _:
                print(color_text("Invalid command!", Fore.RED))
                help()
    else:
        help()

def help():
  print("="*80)
  print("Usage:")
  print(f"   Run {get_cyan_text("'pi add <alias>'")} to add a directory with a new alias")
  print(f"   Run {get_cyan_text("'pi open <alias>'")} to open a previously added directory. Append '-r' to open in the same VScode window")
  print(f"   Run {get_cyan_text("'pi rm <alias>'")} to remove an existing alias")
  print(f"   Run {get_cyan_text("'pi ask'")} to toggle the search mode")
  print("="*80)

def list_all():
  print(color_text("-----------------LIST-----------------", Fore.CYAN))
  print(helpers.get_all())

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

def add(alias):
  check_dir = helpers.get_directory_from_alias(alias)
  if check_dir is not None:
    print(color_text(f"Alias {alias} already points to {check_dir}", Fore.RED))
    help()
    return
  directory = input("Enter the full directory path: ")
  if helpers.add_entry(alias, directory):
    print(color_text(f"Successfully added '{alias}' pointing to '{directory}'", Fore.GREEN))
  else:
    print(color_text("Error adding pair", Fore.RED))

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


def delete(alias):
  if helpers.remove_entry(alias):
    print(color_text(f"Alias '{alias}' removed successfully", Fore.GREEN))
  else:
    print(color_text("That alias was not found", Fore.RED))

def search():
  query = input("Enter search query: ")
  search_url = f"https://www.google.com/search?q={query}"
  webbrowser.open_new_tab(search_url)

if __name__ == "__main__":
  main()