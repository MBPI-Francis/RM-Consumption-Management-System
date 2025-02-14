UPDATES: 02/14/2025



UPDATES - The two environments are REMOVED:
This action is necessary since there are several reasons to not include the environments in the repository.

1. The venv/ folder contains system-specific paths and compiled binaries that work only on the machine where it was created.
2. If someone else clones the repository on a different OS (Windows, macOS, Linux), the environments may not work
3. The venv/ folder contains installed dependencies, which can be hundreds of megabytes in size.
4. Pushing it to GitHub bloats the repository, making cloning and pulling much slower.



UPDATES - environment.yml
- The developer already created environment.yml so that it can be use to create a conda environment



UPDATES - The "RUN THIS TO START API SERVER" file
1. This is a batch file that you can double-click to start the server.

2.  After running it, a terminal/command prompt will appear on your screen.

3. Note: Closing the terminal will stop the API server, which will impact the entire program. The program might not function properly or run at all.



UPDATES - The "Runnable Warehouse Program EXE" folder
1. The "Runnable Warehouse Program EXE" folder only works on computers within the Masterbatch network. It will not function on computers 
outside the network because the executable file is specifically configured to run only on Masterbatch computers.


2. To run the program you can go to this path: "frontend/main.py"
Run the main.py that is located inside the frontend folder



===========================================================================================================================================================


There are two backend folders. These backend folders are where the APIs are located.
1. backend - This is the latest version of the API. Bugs are fixed
2. backend(old) - This is the old version that has bugs



There are two frontend folders. These frontend folders are where the GUI files are located.
1. frontend - This is the latest GUI of the program. Bugs are fixed
2. frontend(old) - This is old GUI version of the program. It has bugs and lacking in UI/UX features

The "Runnable Warehouse Program EXE" folder is where the executable program is located.
All subfiles and subfolders inside this folder are all important to run the Warehouse Program. 


The program is currently using the "backend" and "frontend" folder to run it. 
In addition, the "backend(old)" and "frontend(old)" folders were not used but are still important for restoring the previous features of the system.



