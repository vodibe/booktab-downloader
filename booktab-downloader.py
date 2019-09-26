import os
import shutil
##########################################################################
# CUSTOM SETTINGS: edit this BEFORE running the program.

# 1. Specify your operating system user name
osuser = "user" # <-- edit this

# 2. (OPTIONAL) Edit the output path.
out_path = "C:/Users/"+osuser+"/Desktop/"

# DO NOT EDIT THIS PATH
user_path = "C:/Users/"+osuser+"/AppData/Roaming/Booktab/"

swfrenderpath = "c:/Users/"+osuser+"/Desktop/SWFRender/"
swfrendercommand = swfrenderpath+"swfrender.exe -r 240 "
##########################################################################

print("Booktab Image Downloader")
print("(C) brearlycoffee.cf")

# list all directories in path
user_list = [dI for dI in os.listdir(user_path) if os.path.isdir(os.path.join(user_path,dI))]
print("\n[User list - About",str(len(user_list)),"users found]")
for i in range(len(user_list)):
    print(str(i+1)+" "+user_list[i])
    
notvalid = True
while notvalid:
    codein = input('\nChoose user: ')
    if (int(codein) >= 1) and (int(codein) <= len(user_list)):
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

book_list = [dI for dI in os.listdir(book_path) if os.path.isdir(os.path.join(book_path,dI))]
print("\n[Book list - About",str(len(book_list)),"books found]")
for i in range(len(book_list)):
    print(str(i+1)+" "+book_list[i])
    
notvalid = True
while notvalid:
    codein = input('\nChoose book to extract: ')
    if (int(codein) >= 1) and (int(codein) <= len(book_list)):
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
    sys.exit(0)

print("Selected book: "+book_list[int(codein)-1])
print("Source directory: "+book_path)
print("Destination directory: "+out_path)

print("\nCopying files...")
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
    sys.exit(0)

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

print("\nAdding .swf extension...")
for file in os.listdir(out_path):
    shutil.move(out_path+file,out_path+file+".swf")
print("Done.")

swfrendered = 0
print("\nRendering files...\nNOTE: This action require several minutes, please wait...")
for i in range(len(os.listdir(out_path))):
    os.system(swfrendercommand+out_path+os.listdir(out_path)[i])
    print("Rendering "+str(swfrendered+1)+"/"+str(swfcount), end="\r")
    swfrendered+=1

