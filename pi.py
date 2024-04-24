import sys
import os
import subprocess
from colorama import Fore, Back, Style, init
import pi_json_helpers as helpers

init()
def color_text(text, color):
  return f"{color}{text}{Style.RESET_ALL}"

def main():
  if len(sys.argv) > 1:
    if sys.argv[1] == "open":
      if len(sys.argv) == 3:
        open(sys.argv[2])
      elif len(sys.argv) == 4 and sys.argv[3] == "-r":
        open(sys.argv[2], reload=True)
      else:
        print(color_text("Make sure your request is valid!", Fore.RED))
        help()
    elif sys.argv[1] == "add":
      if len(sys.argv) < 4:
        if sys.argv[2] == ".":
          add_current_directory()
        else:
          add(sys.argv[2])
      else:
        help()
    elif sys.argv[1] == "rm":
      if len(sys.argv) < 4:
        delete(sys.argv[2])
      else:
        help()
    elif sys.argv[1] == "list":
      list_all()
    else:
      print(color_text("Make sure your request is valid!", Fore.RED))
      help()
  else:
    help()

def help():
  print("="*80)
  print("Usage:")
  print(f"   Run {color_text("'122 add <alias>'", Fore.CYAN)} to add a directory with a new alias")
  print(f"   Run {color_text("'122 open <alias>'", Fore.CYAN)} to open a previously added directory. Append '-r' to open in the same VScode window")
  print(f"   Run {color_text("'122 rm <alias>'", Fore.CYAN)} to remove an existing alias")
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

if __name__ == "__main__":
  main()