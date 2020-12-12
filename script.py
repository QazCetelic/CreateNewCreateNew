import glob
import os
import shutil
from pathlib import Path

#                          _  _           _                                __                    _                            _         _
#  ___   ___  _ __   ___  | || |       __| |  ___  __      __ _ __        / _|  ___   _ __      | |_   ___  _ __ ___   _ __  | |  __ _ | |_   ___  ___
# / __| / __|| '__| / _ \ | || |      / _` | / _ \ \ \ /\ / /| '_ \      | |_  / _ \ | '__|     | __| / _ \| '_ ` _ \ | '_ \ | | / _` || __| / _ \/ __|
# \__ \| (__ | |   | (_) || || |     | (_| || (_) | \ V  V / | | | |     |  _|| (_) || |        | |_ |  __/| | | | | || |_) || || (_| || |_ |  __/\__ \
# |___/ \___||_|    \___/ |_||_|      \__,_| \___/   \_/\_/  |_| |_|     |_|   \___/ |_|         \__| \___||_| |_| |_|| .__/ |_| \__,_| \__| \___||___/
#                                                                                                         |_|

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

includeFiletype = False

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


def ask(question):
    user_input = input(f'{question} [y/n]: ').lower()
    if user_input == 'y':
        return True
    else:
        if user_input == 'n':
            return False
        else:
            print("Invalid response, try again.")
            return ask(question)

def logo():
    print("""                     ,--.                       """)
    print("""   ,----..         ,--.'|                       """)
    print("""  /   /   \    ,--,:  : |                       """)
    print(""" |   :     :,`--.'`|  ' :                ,---,  """)
    print(""" .   |  ;. /|   :  :  | |            ,-+-. /  | """)
    print(""" .   ; /--` :   |   \ | :   ,---.   ,--.'|'   | """)
    print(""" ;   | ;    |   : '  '; |  /     \ |   |  ,"' | """)
    print(""" |   : |    '   ' ;.    ; /    / ' |   | /  | | """)
    print(""" .   | '___ |   | | \   |.    ' /  |   | |  | | """)
    print(""" '   ; : .'|'   : |  ; .''   ; :__ |   | |  |/  """)
    print(""" '   | '/  :|   | '`--'  '   | '.'||   | |--'   """)
    print(""" |   :    / '   : |      |   :    :|   |/       """)
    print("""  \   \ .'  ;   |.'       \   \  / '---'        """)
    print("""   `---`    '---'          `----'               """)
                                               

folder_path = str(Path.home()) + "/.local/share/templates/"
files = glob.glob(folder_path + "*.desktop")

def add(name, file_type, icon, group=""):
    lower_name = name.lower().replace(" ", "-")
    desktop_file_path = folder_path + "/" + lower_name + "-template.desktop"
    desktop_file = open(desktop_file_path, "w+")

    new_text = ""
    def line(input):
        nonlocal new_text
        new_text += input + "\n"

    line("[Desktop Entry]")
    if includeFiletype:
        line(f'Name={name}... (.{file_type})')
    else:
        line(f'Name={name}...')
    line(f'Comment=Create a new {lower_name} file using the .{file_type} format.')
    line("Type=Link")
    if group == "":
        line(f'URL=template-files/{lower_name}-template.{file_type}')
    else:
        line(f'URL=template-files/{group}/{lower_name}-template.{file_type}')
    line(f'Icon={icon}')
    line("generated=true")
    desktop_file.write(new_text)
    print(f'Created {os.path.basename(desktop_file_path)}')

logo()

if os.path.isdir(os.path.join(__location__, 'template-files')):
    print(f'Moved template files to {folder_path}')
    copy_and_overwrite(os.path.join(__location__, 'template-files'), folder_path + "template-files")
else:
    print("No template folder found here, nothing is moved")

if ask("Replace old .desktop files"):
    if len(files) != 0:
        print("Removing old template .desktop files")
        for template in files:
            if not os.path.basename(template).startswith('.'):
                text = open(template).read()

                isAutomaticallyAdded = False
                for line in text.splitlines():
                    if line == "generated=true":
                        isAutomaticallyAdded = True
                if isAutomaticallyAdded:
                    os.remove(template)
                    print(f'Removed {os.path.basename(template)}')
                    
includeFiletype = ask("Include file type in menu?")

#  _____                          _         _
# |_   _|  ___  _ __ ___   _ __  | |  __ _ | |_   ___  ___
#   | |   / _ \| '_ ` _ \ | '_ \ | | / _` || __| / _ \/ __|
#   | |  |  __/| | | | | || |_) || || (_| || |_ |  __/\__ \
#   |_|   \___||_| |_| |_|| .__/ |_| \__,_| \__| \___||___/
#                         |_|

# You can add your own templates, using the following format: add([Name], [File Type], [Icon], [Group: Optional])
# Name: name used for the .desktop file and for the "Create New" menu
# File Type: used for the link to the template file and for showing which type is used in the "Create New" menu
# Icon: which icon should be used in the menu
# Group: the submenu in the file templates folder

# Open Document Formats
if ask("Would you like to create templates for the open document formats which are usable for programs like Libre Office?"):
    add("Document", "odt", "libreoffice-text", "libreoffice")
    add("Presentation", "odp", "libreoffice-presentation", "libreoffice")
    add("Spreadsheet", "ods", "libreoffice-spreadsheet", "libreoffice")
    add("Drawing", "odg", "libreoffice-drawing", "libreoffice")
    add("Formula", "odf", "libreoffice-formula", "libreoffice")
# Microsoft Office
if ask("Would you like to create templates for Microsoft office"):
    add("MS Word", "docx", "gnome-mime-application-msword", "msoffice")
    add("MS Powerpoint", "pptx", "gnome-mime-application-powerpoint", "msoffice")
    add("MS Excel", "xlsx", "gnome-mime-application-msexcel", "msoffice")
# Markdown
add("Markdown", "md", "text-markdown")
# Vector Drawing (Inkscape)
add("Vector Drawing", "svg", "draw-polygon")
