import glob
import os
import shutil
from pathlib import Path

# CreateNewCreateNew
# Easily and quickly create new entries into the "Create New" file menu on Linux desktops.
# Scroll down templates section to see add your own templates.

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


def ask(question):
    user_input = input(f'{question} [y/n]: ').lower()
    if user_input in ['y', 'yes']:
        return True
    else:
        if user_input in ['n', 'no']:
            return False
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


folder_path = str(Path.home()) + "/.local/share/templates/"
files = glob.glob(folder_path + "*.desktop")


def add(name, file_type, icon, group=""):
    snake_case_name = name.lower().replace(" ", "-")
    desktop_file_path = f'{folder_path}/{snake_case_name}-template.desktop'
    desktop_file = open(desktop_file_path, "w+")

    # Write the template metadata file
    new_text = ""

    def append_line(s):
        nonlocal new_text
        new_text += s + "\n"

    append_line("[Desktop Entry]")
    append_line(f'Name={name}...')
    append_line(f'Comment=Create a new {snake_case_name} file using the .{file_type} format.')
    append_line("Type=Link")
    if group == "":
        append_line(f'URL=template-files/{snake_case_name}-template.{file_type}')
    else:
        append_line(f'URL=template-files/{group}/{snake_case_name}-template.{file_type}')
    append_line(f'Icon={icon}')
    append_line("generated=true")

    desktop_file.write(new_text)
    print(f'Created {os.path.basename(desktop_file_path)}')


logo()

template_files = os.path.join(__location__, 'template-files')
if os.path.isdir(template_files):
    print(f'Moved template files to {folder_path}')
    copy_and_overwrite(template_files, folder_path + "template-files")
else:
    print("No template folder found here, nothing is moved")

if ask("Remove old generated .desktop files"):
    # Check if there actually are any .desktop files
    if len(files) != 0:
        print("Removing old template .desktop files")
        for template in files:
            if not os.path.basename(template).startswith('.'):
                text = open(template).read()
                isAutomaticallyAdded = False
                for line in text.splitlines():
                    if line == "generated=true":
                        isAutomaticallyAdded = True
                        break
                if isAutomaticallyAdded:
                    os.remove(template)
                    print(f'Removed {os.path.basename(template)}')
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

# Markdown
add("Markdown", "md", "text-markdown")
# Vector Drawing (Inkscape)
add("Vector Drawing", "svg", "image-x-svg+xml")

# Scripting
if ask("Would you like to add templates for scripting?"):
    # Shell script
    add("Shell Script", "sh", "utilities-terminal")
    # Python script
    add("Python Script", "py", "text-x-python")
