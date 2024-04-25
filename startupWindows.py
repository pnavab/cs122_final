import os
import winreg
import subprocess

cwd = os.getcwd()

key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)

try:
    path, _ = winreg.QueryValueEx(key, "PATH")
    path = path.split(";")
    
    if cwd not in path:
        path.append(cwd)
        new_path = ";".join(path)
        
        # ipdate the PATH environment variable
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        print("PATH environment variable updated successfully.")

        # refresh the path
        subprocess.run(f'setx PATH "{new_path}"', shell=True)
        print("PATH environment variable updated persistently.")
    else:
        print("Current working directory is already in the PATH.")

finally:
    winreg.CloseKey(key)

with open('.env', 'w') as f:
    f.write(f'DIRECTORY={cwd}\n')
    print(".env file created successfully.")

with open('pi.json', 'w') as f:
    f.write("{}")
    print("pi.json file created successfully.")