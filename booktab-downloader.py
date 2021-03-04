import os
import shutil
import getpass
import img2pdf
import subprocess
from PIL import Image

##########################################################################
# CUSTOM SETTINGS: edit this BEFORE running the program.

# 1. Specify your operating system user name
osuser = getpass.getuser()

# 2. (OPTIONAL) Edit the output path.
out_path = "C:/Users/"+osuser+"/Desktop/"

# DO NOT EDIT THIS PATH
user_path = "C:/Users/"+osuser+"/AppData/Roaming/Booktab/"

# Resolve swf path
swfrenderpaths = [
    "C:/Program Files (x86)/SWFTools/",
    "C:/Users/"+osuser+"/Desktop/SWFRender/"
]

swfrenderpath = None

for path in swfrenderpaths:
    if (os.path.isfile(path + "swfrender.exe")):
        swfrenderpath = path + "swfrender.exe"
        break

if not swfrenderpath:
    print("ERROR: SWFTOOLS not installed.")
    print("Please, download it from here http://www.swftools.org/swftools-2013-04-09-1007.exe and run as administrator")
    print("In one of the following folders: ")
    for path in swfrenderpaths:
        print("  -" + path)
    exit(1)

swfrendercommand = ["-r", "240"]
swfpreviewcommand =  ["-r", "72", "-p", "1"]
invalidimagesize = 5000
##########################################################################

print("Booktab Image Downloader")
print("(C) brearlycoffee.cf")

# list all directories in path
user_list = [dI for dI in os.listdir(user_path) if os.path.isdir(os.path.join(user_path,dI)) and "@" in dI]
print("\n[User list - About",str(len(user_list)),"users found]")
for i in range(len(user_list)):
    print(str(i+1)+" "+user_list[i])
    
notvalid = True
while notvalid:
    codein = input('\nChoose user: ')
    if codein and (int(codein) >= 1) and (int(codein) <= len(user_list)):
        notvalid = False
    else:
        notvalid = True   
    if notvalid == False:
        if user_list[int(codein)-1] == "all-users" or user_list[int(codein)-1] == "appstate" or user_list[int(codein)-1] == "logs":
            print("The item does not belong to any user.")
            notvalid = True
    else:
        print("Insert a valid user.")

############################################
book_path = "C:\\Users\\"+osuser+"\\AppData\\Roaming\\Booktab\\"+str(user_list[int(codein)-1])

book_list = [dI for dI in os.listdir(book_path) if os.path.isdir(os.path.join(book_path,dI)) and dI != "appstate" and dI != "demo0"]
print("\n[Book list - About",str(len(book_list)),"books found]")
for i in range(len(book_list)):
    print(str(i+1)+" "+book_list[i])
    
notvalid = True
while notvalid:
    codein = input('\nChoose book to extract: ')
    if codein and (int(codein) >= 1) and (int(codein) <= len(book_list)):
        notvalid = False
    else:
        notvalid = True
        
    if notvalid == False:
        if book_list[int(codein)-1] == "appstate" or book_list[int(codein)-1] == "demo0":
            print("The item does not belong to any book.")
            notvalid = True
    else:
        print("Insert a valid book code.")


book_path = book_path + "\\"+book_list[int(codein)-1]+"\\"
out_path = out_path + book_list[int(codein)-1] + "/"

try:
    os.mkdir(out_path)
except OSError:
    print("ERROR: Unable to create directory or directory already exists!")
    exit(1)

print("Selected book: "+book_list[int(codein)-1])
print("Source directory: "+book_path)
print("Destination directory: "+out_path)

print("\nCopying files")
swfcount = 0
pdfcount = 0  
for root, dirs, files in os.walk(book_path):
    for file in files:
        if len(os.listdir(root)) == 1 and file.find(".") == -1:
            path_file = os.path.join(root,file)
            shutil.copy2(path_file,out_path)
            swfcount+=1
            print(str(swfcount)+" copied files.", end="\r")
        else:
            path_file = os.path.join(root,file)
            if file.find(".") == -1 and file.find("-") == -1:
                shutil.copy2(path_file,out_path)
                swfcount+=1
                print(str(swfcount)+" copied files.", end="\r")
if swfcount == 0:
    print("No valid files have been found!")
    exit(1)

while True:                
    pdfchoice = input("\nDo you want to download any PDF documents? Y/N ")
    if pdfchoice == "Y" or pdfchoice == "y" or pdfchoice == "N" or pdfchoice == "n":
        break
    else:
        print("Insert a valid answer. Y/N")

if pdfchoice == "Y" or pdfchoice == "y":
    for root, dirs, files in os.walk(book_path):
        for file in files:
            path_file = os.path.join(root,file)
            if path_file.endswith(".pdf"):
                if pdfcount == 0:
                    os.mkdir(out_path+"PDF/")
                shutil.copy2(path_file,out_path+"PDF/")
                pdfcount+=1
                print(str(pdfcount)+" copied PDFs.", end="\r")
else:
    pdfcount = -1
if pdfcount == 0:
    print("No PDFs have been found!")

print("\nAdding .swf extension")
for file in os.listdir(out_path):
    file = os.path.join(out_path, file)
    if os.path.isfile(file):
        shutil.move(file,file+".swf")
print("Done.")

swfrendered = 0
print("\nRendering preview of each swf file")

for file in os.listdir(out_path):
    file = os.path.join(out_path, file)
    if file.endswith(".png") or file.endswith(".jpg"):
        pass
    elif os.path.isfile(file) == False:
        pass
    else:
        print(str(swfrendered+1)+"/"+str(swfcount), end="\r")
        p = [swfrenderpath] + swfpreviewcommand + ["-o", file + ".png", file]
        subprocess.Popen(p).wait()
        swfrendered+=1

print("Done.")

print("""\nGood! You're almost done! Now follow these steps:
1. Open Booktab software, choose your book, then look at the order of all chapters.
2. Rename swf files in order that the first one is 1.swf/a.swf (...).
   Take a look at related png files.
3. Do not delete png files. The program will do it for you.""")

steptwo = "n"
while steptwo != "k" and steptwo != "K":
    steptwo = input("When you followed all these steps press K button: ")

print("\nDeleting png files")
for file in os.listdir(out_path):
    file = os.path.join(out_path, file)
    if file.endswith(".png") or file.endswith(".jpg"):
        os.remove(file)
print("Done.")

swfrendered = 0 
print("\nRendering files\nNOTE: This action require several minutes, please wait...")
for file in os.listdir(out_path):
    file = os.path.join(out_path, file)
    if os.path.isfile(file):
        print(str(swfrendered+1)+"/"+str(swfcount), end="\r")

        p = [swfrenderpath] + swfrendercommand + ["-o", out_path + "page.png", file]
        subprocess.Popen(p).wait()

        swfrendered+=1
print("Done.")

print("\nDeleting invlid images")     # testare a parte
for page in os.listdir(out_path):
    page = os.path.join(out_path, page)
    if os.path.isfile(page) and os.stat(page).st_size <= invalidimagesize:
        os.remove(page)
print("Done.")

print("\nDeleting swf files...")
for file in os.listdir(out_path):
    file = os.path.join(out_path, file)
    if ".swf" in file:
        os.remove(file)
print("Done.")

print("\nMerging everything into single PDF")

imagelist = []    
for file in os.listdir(out_path):
    file = os.path.join(out_path, file)
    if os.path.isfile(file):
        imagelist.append(file)

for image in imagelist:
    img = Image.open(image)
    if img.mode == "RGBA":
        img = img.convert("RGB")
        img.save(image, "PNG")

print("This action requires several minutes, please wait...")
with open(out_path+book_list[int(codein)-1]+".pdf","wb") as doc:
    doc.write(img2pdf.convert(imagelist))
print("Done.")

print("\nDeleting images")
for i in range(len(imagelist)):
    os.remove(imagelist[i])
print("Done.")

print("\nFinished! Check: "+out_path+book_list[int(codein)-1]+".pdf")
