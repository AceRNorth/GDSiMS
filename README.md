# GDSiMS
GDSiMS: Gene Drive Simulator of Mosquito Spread is a Graphical User Interface (GUI) for the [model program](https://github.com/AceRNorth/GeneralMetapop) developed by Ace R. North and Sara Perez Vizan. 

Full documentation website for the model program can be found [here](https://acernorth.github.io/GeneralMetapop/ ).

GDSiMS is a graphical user interface for a malaria mosquito population model program. The model simulates the potential of gene drive technology to suppress mosquito populations and thus reduce malaria transmission. Gene drives are genetic elements that can quickly spread through a population via super-Mendelian inheritance frequencies (>50%). They can be engineered with specific properties to e.g. suppress mosquito populations via reduced female fertility (as modelled here). Our program can inform current gene drive development research, policy and regulation. 

## Features:
- Best for beginners and non-programmers
- User-friendly interface
- ‘In-house’, interactive data visualisation features – selected plots and animations chosen to best illustrate and investigate the model.
- Short and easy installation process, though distribution is currently only available on previously tested systems (Windows 10, 11, ARM-based Macs).
- Options to load pre-defined parameter sets and/or tweak parameters
- Advanced parameter window dialog
- Tooltips on parameter labels provide instant descriptions when hovering over them
- Run the model program directly from the interface and check its progress
- Organised output data directories with descriptive parameter spreadsheet files

## Should I use the GUI or the model program?
The graphical user interface (GUI) is best suited to beginners to the model and non-programmers. The GUI offers ‘in-house’ selected data visualisation features which best illustrate the model behaviours. Plots and animations otherwise need to be created from scripts separate to the model program (we provide sample Python scripts).

The GUI is easy and quick to install, though only currently available on Windows 10 and 11 systems and ARM-based Macs. The model program uses cross-platform tools to ensure compatibility with all systems, which, though simplified and documented, makes it a more complex installation process. 

The model program is best suited to advanced users in need of quick custom parameter set changes. The model program also offers a command-line interface (CLI), which may be used by those not familiar with C++, and offers more pre-defined sets compared to the GUI. Directly interacting with the C++ code also provides flexible use cases thanks to its flexible architecture.

Both are freely available on their respective GitHub repositories, have an open-source licence and aim to have a documentation website with tutorials (tutorials for the GUI are in progress).

## Installation
GDSiMS is currently available for Windows 10 and 11 and ARM-based macOS (Apple Silicon).

### Windows
1. Download the files:
   
   i. Clone the repository via Git Bash (recommended):
   
      Install [Git Bash](https://git-scm.com/downloads) and download [Git LFS](https://git-lfs.com/). Open Git Bash and finish installing Git LFS by running this command:

      ```bash
      git lfs install
      ```
      
      Navigate to your chosen directory and run this command to clone the repository:
   
      ```bash
      cd C:\Users\MyUser\Projects
      git clone https://github.com/AceRNorth/GDSiMS.git
      ```
   ii. Alternatively, download the files as a ZIP folder, unzip and move to your chosen directory.
   
   ![GDSiMS_installation_download_zip](https://github.com/user-attachments/assets/617f44d3-3d69-4bc3-9b3e-c21cd307a923)

3. Open the ```dist_win/GDSiMS``` directory and run the GDSiMS executable file.
   
   Note: Windows Defender may pop up when attempting to run the executable. This is because it doesn’t recognise the distributor. The application is safe, so you can click on ‘More info’ and then ‘Run anyway’.

### Mac

1. Install [Homebrew](https://git-scm.com/downloads) and [Git](https://git-scm.com/downloads/mac) if not already installed. This can be easily done by opening a terminal window and running these two commands:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install git
   ```
   Then, install [Git LFS](https://git-lfs.com/):
   ```bash
   brew install git-lfs
   ```
   
2. Navigate to your chosen directort and clone the repository:
   ```bash
   cd /Users/username/Documents/
   git clone https://github.com/AceRNorth/GDSiMS.git
   ```
   Note: Mac users must clone the repository. ZIP downloading will not work due to the way the large .dmg file has been stored on GitHub.

3. Open your chosen folder on the Finder and click on the ```dist_mac``` folder and then on the ```GDSiMS.dmg``` file.
   
   i. The .dmg file will open a prompt, asking you to drag the GDSiMS application into your Applications directory (you have to physically drag the icon into the other icon). This will install it as an app onto your system, and you can then find the app in your Applications folder using the Finder and click to run it.

   ![install_mac_drag_app](https://github.com/user-attachments/assets/64ff68e2-5e6a-47ed-bbf1-b38f88fd53bb)


## Usage
The GUI provides features to enter model parameters, run the model program and view the output data. 

1. Load a parameter set from available pre-defined sets by selecting one from the drop-down and clicking Load. Parameters can also be tweaked at any time before running, including those in the advanced parameter window dialog.

2. Select an output data destination directory and choose the name for your simulation before clicking Run. The interface will give updates on the simulation’s progress whilst it’s running, and plotting options will become available upon completion of the simulation. 

   Note: By default, the output files will be created in the ```_internal``` subdirectory for Windows, and in the app's ```Contents/Frameworks/``` subdirectory for Mac. You can access the app's contents on Mac by right-clicking on the GDSiMS app in your Applications directory and choosing "Show Package Contents".

4. Choose from the tabs to view different plot and animation options, interact via the plot sidebar to select plotting parameters and click Plot or Play to update the canvas.

![GDSiMS_GUI_snapshot](https://github.com/user-attachments/assets/7b1cd53d-ab03-4e9b-adec-adc0c0ca0b77)



