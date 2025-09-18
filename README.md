============================

NextFly Project Launcher

============================



NextFly is a batch tool to automate building and running local projects.

It allows you to manage multiple projects, switch between JDK versions, start servers, and launch Maven builds easily from a single interface.



=================================

* Repository Structure

=================================



NextFly/

├── scripts/

│   └── NextFly\_launcher.bat  # Main script for build and run

├── config/

│   ├── config.env.example    # Example configuration (public)

│   └── config.env            # Real configuration (local, not versioned)

├── README.md		       # This file

├── README.it.md               # Italian version of this file

├── README.ru.md              # Russian version of this file

└── .gitignore                # Git ignore rules



=================================

* &nbsp;Configuration

=================================



**Clone the repository:**



git clone https://github.com/AngelDragon999/NextFly.git





**Copy the example configuration and customize it:**



cd NextFly\\config

copy config.env.example config.env





Open config.env and update the paths for your local projects, JDK, Maven, and servers according to your environment.



===============================

* Using the Script

===============================



**Open a command prompt in the scripts/ folder:**



cd ..\\scripts





**Run the script:**



NextFly\_launcher.bat





Follow the interactive menu to:



* Start project servers
* Build projects with Maven
* Switch between JDK 8 and JDK 21 and others that You can add in. 



===============================

* Important Notes

===============================



* **Never commit config.env, it contains local paths and sensitive configuration.**
* All scripts read variables from config.env to function correctly.
* To add new scripts, place them in the scripts/ folder and update the README with instructions.



===============================

* Benefits

===============================



1. Centralized project management
2. Avoids path and JDK errors
3. Easy distribution and collaboration via Git
4. Ready to expand with new scripts in the future





