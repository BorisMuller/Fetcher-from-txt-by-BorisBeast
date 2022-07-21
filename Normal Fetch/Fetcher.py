import requests
import os
import sys

links_file = sys.argv[1]
prefix = 0
Flashpoint = ""
if len(sys.argv) > 2:
    if len(sys.argv) > 3:
        print("WARNING: TOO MANY ARGUMENTS GIVEN BY BAT")
    if sys.argv[2] == "noprefix":
        print("no prefix mode starting")
        prefix = ""
    else:
        print("flashpoint fetch starting")
        Flashpoint = sys.argv[2]
else:
    print("normal mode starting")

invalid_chars = ["\\", ":", "*", "?", "\"", "<", ">", "|"]

if prefix == 0:
    print("Please provide a prefix, leave empty if you aren't sure or don't need it:")
    prefix = input()
print("Please provide the shared folder, leave empty if you aren't sure or don't need it:")
shared_folder = input()
while any(illegal in shared_folder for illegal in invalid_chars):
    print(
        "Please refrain from using the following characters: \"\\\", \":\", \"*\", \"?\", \"\"\", \"<\", \">\", and \"|\"")
    print("Provide a valid shared folder:")
    shared_folder = input()
print("Please pick a folder name:")
folder_name = input()
while any(illegal in folder_name for illegal in invalid_chars) or "/" in folder_name:
    if "/" in folder_name:
        print("Please don't use any slashes in your folder name and pick only the name for the base folder.")
    else:
        print(
            "Please refrain from using the following characters: \"\\\", \":\", \"*\", \"?\", \"\"\", \"<\", \">\", and \"|\"")
    print("Provide a valid folder name:")
    folder_name = input()

if folder_name == "":
    folder_name = shared_folder

with open(links_file) as f:
    links = f.readlines()

full_links = []
for index, link in enumerate(links):
    full_link = Flashpoint
    try:
        link = link.split()[0]
    except:
        lol = "lol"
    if "." not in link:
        if "GET" not in link and "POST" not in link and "XHR" not in link:
            print(link + " is not a link")
    else:
        if prefix != "":
            full_link += prefix + link
        else:
            full_link += link
        full_links.append(full_link)

for link in full_links:
    if link[0:4] != "http":
        link = "http://" + link
    if shared_folder == "":
        location = "Downloads/" + link.split("/", 3)[3]
        directory = location.rsplit('/', 1)[0]
    elif shared_folder in link:
        location = "Downloads/" + folder_name + link.split(shared_folder, 1)[1]
        directory = location.rsplit('/', 1)[0]
    else:
        location = "Downloads/"+folder_name+"/EXTERNAL_FILES/" + link.split("/", 3)[3]
        directory = location.rsplit('/', 1)[0]
        print("WARNING: " + link + " is an external file! Make sure to change the link to this file in the main swf or the other file that calls it.")

    if not os.path.exists(directory):
        os.makedirs(directory)
    r = ''
    try:
        r = requests.get(link, allow_redirects=True)
    except:
        print(link + " is not downloadable")
    if r != "":
        file1 = open(location, "wb").write(r.content)
        print("saving to: " + location)

print("Finished! Your files have been saved in the \"" + folder_name + "\" folder")
