# GDSiMS
GDSiMS: Gene Drive Simulator of Mosquito Spread is a Graphical User Interface (GUI) for the [model program](https://github.com/AceRNorth/GeneralMetapop) developed by Ace R. North and Sara Perez Vizan. 

Full documentation website for the model program can be found [here](https://acernorth.github.io/GeneralMetapop/ ).

GDSiMS is a graphical user interface for a malaria mosquito population model program. The model simulates the potential of gene drive technology to suppress mosquito populations and thus reduce malaria transmission. Gene drives are genetic elements that can quickly spread through a population via super-Mendelian inheritance frequencies (>50%). They can be engineered with specific properties to e.g. suppress mosquito populations via reduced female fertility (as modelled here). Our program can inform current gene drive development research, policy and regulation. 

## Features:
- Best for beginners and non-programmers
- User-friendly interface
- ‘In-house’, interactive data visualisation features – selected plots and animations chosen to best illustrate and investigate the model.
- Short and easy installation process, though distribution is currently only available on previously tested systems (Windows 10, 11). (Testing for other systems is in progress.)
- Options to load pre-defined parameter sets and/or tweak parameters
- Advanced parameter window dialog
- Tooltips on parameter labels provide instant descriptions when hovering over them
- Run the model program directly from the interface and check its progress
- Organised output data directories with descriptive parameter spreadsheet files

## Should I use the GUI or the model program?
The graphical user interface (GUI) is best suited to beginners to the model and non-programmers. The GUI offers ‘in-house’ selected data visualisation features which best illustrate the model behaviours. Plots and animations otherwise need to be created from scripts separate to the model program (we provide sample Python scripts).

The GUI is easy and quick to install, though only currently available on Windows 10 and 11 systems (testing on other systems is in progress). The model program uses cross-platform tools to ensure compatibility with all systems, which, though simplified and documented, makes it a more complex installation process. 

The model program is best suited to advanced users in need of quick custom parameter set changes. The model program also offers a command-line interface (CLI), which may be used by those not familiar with C++, and offers more pre-defined sets compared to the GUI. Directly interacting with the C++ code also provides flexible use cases thanks to its flexible architecture.

Both are freely available on their respective GitHub repositories, have an open-source licence and aim to have a documentation website with tutorials (tutorials for the GUI are in progress).

## Installation
GDSiMS is currently only available for Windows 10, 11. Testing for other systems is in progress.

1. Download the files:
   
   i. Clone the repository via Git Bash (recommended):
   
      Install Git Bash and open. Navigate to your chosen directory and run this command to clone the repository:
     ```bash
     cd C:\Users\MyUser\Projects
     git clone https://github.com/AceRNorth/GDSiMS.git
     ```
   ii. Alternatively, download the files as a ZIP folder, unzip and move to your chosen directory.
   
   ![GDSiMS_installation_download_zip](https://github.com/user-attachments/assets/617f44d3-3d69-4bc3-9b3e-c21cd307a923)

2. Open the ```dist_win/GDSiMS``` directory and run the GDSiMS executable file.
   
   Note: Windows Defender may pop up when attempting to run the executable. This is because it doesn’t recognise the distributor. The application is safe, so you     can click on ‘More info’ and then ‘Run anyway’.

## Usage
The GUI provides features to enter model parameters, run the model program and view the output data. 

1. Load a parameter set from available pre-defined sets by selecting one from the drop-down and clicking Load. Parameters can also be tweaked at any time before running, including those in the advanced parameter window dialog.

2. Select an output data destination directory and choose the name for your simulation before clicking Run. The interface will give updates on the simulation’s progress whilst it’s running, and plotting options will become available upon completion of the simulation. 

   Note: By default, the output files will be created in the ```_internal``` directory.

3. Choose from the tabs to view different plot and animation options, interact via the plot sidebar to select plotting parameters and click Plot or Play to update the canvas.

![GDSiMS_GUI_snapshot](https://github.com/user-attachments/assets/7b1cd53d-ab03-4e9b-adec-adc0c0ca0b77)


