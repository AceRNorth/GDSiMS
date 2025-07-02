# GDSiMS GUI
GDSiMS GUI is a Graphical User Interface (GUI) for [GDSiMS](https://github.com/AceRNorth/GeneralMetapop): the Gene Drive Simulator of Mosquito Spread, a model program developed by Ace R. North and Sara Perez Vizan. 

Full documentation website for GDSiMS [here](https://acernorth.github.io/GeneralMetapop/ ).

GDSiMS GUI is a graphical user interface for a malaria mosquito population model program. The model simulates the potential of gene drive technology to suppress mosquito populations and thus reduce malaria transmission. Gene drives are genetic elements that can quickly spread through a population via super-Mendelian inheritance frequencies (>50%). They can be engineered with specific properties to e.g. suppress mosquito populations via reduced female fertility (as modelled here). Our program can inform current gene drive development research, policy and regulation. 

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

## Should I use GDSiMS GUI or the model program (GDSiMS)?
The graphical user interface (GUI) is best suited to beginners to the model and non-programmers. The GUI offers ‘in-house’ selected data visualisation features which best illustrate the model behaviours. Plots and animations otherwise need to be created from scripts separate to the model program (we provide sample Python scripts).

The GUI is easy and quick to install, though only currently available on Windows 10 and 11 systems and ARM-based Macs. The model program uses cross-platform tools to ensure compatibility with all systems, which, though simplified and documented, makes it a more complex installation process. 

The model program is best suited to advanced users in need of quick custom parameter set changes. The model program also offers a command-line interface (CLI), which may be used by those not familiar with C++, and offers more pre-defined sets compared to the GUI. Directly interacting with the C++ code also provides flexible use cases thanks to its flexible architecture.

Both are freely available on their respective GitHub repositories, have an open-source licence and aim to have a documentation website with tutorials (tutorials for the GUI are in progress).

## Installation
### Download (Recommended)
GDSiMS GUI is currently available for Windows 10 and 11 and ARM-based macOS (Apple Silicon) via the Releases tab on the right-hand side of the repository. Click on the latest release and scroll down to download the appropriate asset for your system. 

Output file locations are discussed in the [Usage](#usage) section below.

#### Windows
Download the GDSiMS_Win ZIP folder and extract the files before running the GDSiMS executable.

Note: Windows Defender may pop up when attempting to run the executable. This is because it doesn’t recognise the distributor. The application is safe, so you can click on ‘More info’ and then ‘Run anyway’.

#### Mac (ARM-based, i.e. Apple Silicon)
Download the GDSiMS_Mac DMG file and click to open it. 

The DMG file will open a prompt, asking you to drag the GDSiMS application into your Applications directory (you have to physically drag the icon into the other icon). This will install it as an app onto your system, and you can then find the app in your Applications folder using the Finder and click to run it.

   ![install_mac_drag_app](https://github.com/user-attachments/assets/0e045d03-42cb-42ad-b053-7199e8ed9f71)

When clicking to run, you may get a warning saying '"GDSiMS not opened - Apple could not verify "GDSiMS" is free of malware that may harm your Mac or compromise your privacy". If so, click Done. This warning can be bypassed by following these short [instructions](https://support.apple.com/en-gb/guide/mac-help/mchleab3a043/mac). You should then be able to run the app normally.

### Source (Deprecated)
Old versions of the distributions are available on the repository via git clone and Git LFS. These will be removed soon.
#### Windows
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

#### Mac

1. Install [Homebrew](https://brew.sh/). This can be easily done by opening a terminal window and running this command:
   
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   
   i. Make sure to follow the Next steps given at the end - these will be slightly different on your system to the image below, make sure to copy the commands given to **you**.

      ![install_mac_finish_brew](https://github.com/user-attachments/assets/e146eb3a-33ae-477b-b707-1953998a928a)

2. Install [Git](https://git-scm.com/downloads/mac) if not already installed:
   
   ```bash
   brew install git
   ```
   
3. Then, install [Git LFS](https://git-lfs.com/):
   
   ```bash
   brew install git-lfs
   ```
   
   i. Make sure to follow the Caveats given towards the end by running these commands:
   
      ```bash
      git lfs install
      git lfs install --system
      ```
      
     ![install_mac_finish_git_lfs](https://github.com/user-attachments/assets/3c1c42d5-502f-4010-80d8-ce4c62ca8419)


4. Navigate to your chosen directory and clone the repository:
   
   ```bash
   cd /Users/username/Documents/
   git clone https://github.com/AceRNorth/GDSiMS.git
   ```
   
   Note: Mac users must clone the repository. ZIP downloading will not work due to the way the large .dmg file has been stored on GitHub.

5. Open your chosen folder on the Finder and click on the ```dist_mac``` folder and then on the ```GDSiMS.dmg``` file.
   
   i. The .dmg file will open a prompt, asking you to drag the GDSiMS application into your Applications directory (you have to physically drag the icon into the other icon). This will install it as an app onto your system, and you can then find the app in your Applications folder using the Finder and click to run it.

   ![install_mac_drag_app](https://github.com/user-attachments/assets/e9f38974-6b17-47ff-b818-53a89497c9c4)


## Usage
The GUI provides features to enter model parameters, run the model program and view the output data. 

1. Load a parameter set from available pre-defined sets by selecting one from the drop-down and clicking Load. Parameters can also be tweaked at any time before running, including those in the advanced parameter window dialog.

2. Select an output data destination directory and choose the name for your simulation before clicking Run. The interface will give updates on the simulation’s progress whilst it’s running, and plotting options will become available upon completion of the simulation. 

   Note: By default, the output files will be created in the ```_internal``` subdirectory for Windows, and in the app's ```Contents/Frameworks/``` subdirectory for Mac. You can access the app's contents on Mac by right-clicking on the GDSiMS app in your Applications directory and choosing "Show Package Contents".

4. Choose from the tabs to view different plot and animation options, interact via the plot sidebar to select plotting parameters and click Plot or Play to update the canvas.

![GDSiMS_GUI_snapshot](https://github.com/user-attachments/assets/7b1cd53d-ab03-4e9b-adec-adc0c0ca0b77)



