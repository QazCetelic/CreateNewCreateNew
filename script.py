import glob
import os
import shutil
from pathlib import Path

# CreateNewCreateNew
# Easily and quickly create new entries into the "Create New" file menu on Linux desktops.
# Scroll down to the templates section to add your own templates to the script.

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


always_true = False

def ask(question: str):
    global always_true
    if always_true:
        return True
    else:
        user_input = input(f'{question} [y/n/a]: ').lower()
        if user_input in ['y', 'yes']:
            return True
        else:
            if user_input in ['n', 'no']:
                return False
            else:
                if user_input in ['a', 'all']:
                    always_true = True
                    return True
                else:
                    print("Invalid response, try again.")
                return ask(question)


def logo():
    print("""                     ,--.                       """)
    print("""   ,----..         ,--.'|                       """)
    print("""  /   /   \    ,--,:  | |                       """)
    print(""" |   |     :,`--.'`|  | |                ,---,  """)
    print(""" |   |  .\ /|   |  |  | |            ,-+-. /  | """)
    print(""" |   | /--` |   |   \ | |   ,---.   ,--.'|'   | """)
    print(""" |   | |    |   | '  '; |  /     \ |   |  ,"| | """)
    print(""" |   | |    |   ' ;.    | /    / ' |   | /  | | """)
    print(""" |   | '___ |   | | \   |.    ' /  |   | |  | | """)
    print(""" |   | | .'||   | |  ; .''   ; :__ |   | |  |/  """)
    print(""" |   | '/  ||   | '`--'  '   | '.'||   | |--'   """)
    print(""" |   |    / |   | |      |   |    :|   |/       """)
    print("""  \   \ .'  |   |.'       \   \  / '---'        """)
    print("""   `---`    '---'          `----'               """)


folder_path = str(Path.home()) + "/Templates/"
files = glob.glob(folder_path + "*.desktop")


def add(name: str, file_type: str, icon: str, group=""):
    snake_case_name = name.lower().replace(" ", "-")
    type = ["file", "folder"][file_type == ""]
    suffix = [f".{file_type}", ""][type == "folder"]

    new_lines: list[str] = []

    new_lines.append("[Desktop Entry]")
    new_lines.append(f"Name={name}...")
    new_lines.append(f"Comment=Create a new {name} {type}.")
    new_lines.append("Type=Link")
    if group == "":
        new_lines.append(f"URL=template-files/{snake_case_name}-template{suffix}")
    else:
        new_lines.append(f"URL=template-files/{group}/{snake_case_name}-template{suffix}")
    new_lines.append(f"Icon={icon}")
    new_lines.append("generated=true")

    desktop_file_path = f'{folder_path}/{snake_case_name}-template.desktop'
    desktop_file = open(desktop_file_path, "w+")
    desktop_file.write('\n'.join(new_lines))
    desktop_file.close()

    print(f'Created {os.path.basename(desktop_file_path)}')


logo()

template_files = os.path.join(__location__, "template-files")
if os.path.isdir(template_files):
    print(f"Moved template files to {folder_path}")
    copy_and_overwrite(template_files, folder_path + "template-files")
else:
    print("No template folder found here, nothing is moved")

if ask("Remove old generated .desktop files"):
    # Check if there actually are any .desktop files
    if len(files) != 0:
        print("Removing old template .desktop files")
        for template in files:
            if not os.path.basename(template).startswith('.'):
                file = open(template, "r")
                lines = file.readlines()
                isAutomaticallyAdded = False
                for line in lines:
                    if line == "generated=true":
                        isAutomaticallyAdded = True
                        break
                if isAutomaticallyAdded:
                    os.remove(template)
                    print(f'Removed {os.path.basename(template)}')
                file.close()
    else:
        print("No template .desktop files found")

#  _____                          _         _
# |_   _|  ___  _ __ ___   _ __  | |  __ _ | |_   ___  ___
#   | |   / _ \| '_ ` _ \ | '_ \ | | / _` || __| / _ \/ __|
#   | |  |  __/| | | | | || |_) || || (_| || |_ |  __/\__ \
#   |_|   \___||_| |_| |_|| .__/ |_| \__,_| \__| \___||___/
#                         |_|

# You can add your own templates, using the following format: add([Name], [File Type], [Icon], [Group: Optional])
# Name:         Name used for the .desktop file and for the "Create New" menu.
# File Type:    Used for the link to the template file and for showing which type is used in the "Create New" menu.
# Icon:         Which icon should be used in the menu.
# Group:        The submenu in the file templates folder.

# Open Document Formats
if ask("Would you like to add templates for the open document formats which are used by programs like Libre Office?"):
    add("Openoffice Document", "odt", "libreoffice-text", "libreoffice")
    add("Openoffice Presentation", "odp", "libreoffice-presentation", "libreoffice")
    add("Openoffice Spreadsheet", "ods", "libreoffice-spreadsheet", "libreoffice")
    add("Openoffice Drawing", "odg", "libreoffice-drawing", "libreoffice")
    add("Openoffice Formula", "odf", "libreoffice-formula", "libreoffice")
    add("Openoffice Database", "odb", "libreoffice-database", "libreoffice")

# Microsoft Office
if ask("Would you like to add templates for Microsoft office?"):
    add("Microsoft Word", "docx", "x-office-document", "msoffice")
    add("Microsoft Powerpoint", "pptx", "x-office-presentation", "msoffice")
    add("Microsoft Excel", "xlsx", "x-office-spreadsheet", "msoffice")

add("Markdown", "md", "text-markdown")
add("Vector Drawing", "svg", "image-x-svg+xml")

if ask("Would you like to add templates for scripting?"):
    add("Shell Script", "sh", "application-x-shellscript")
    add("Python Script", "py", "text-x-python")

# Code
if ask("Would you like to add templates for Haxe?"):
    add("Haxe Project", "", "folder-new")
    add("Vala Project", "", "folder-new")
