# Git Bash

1. Download Git Bash from Git Website
    - Navigate to the Git website.
    - Ensure you are on the official Git website to avoid any unauthorized or malicious software.
<img src="/assets/img/install/bash/git_bash_download.png" alt="Git Bash Download" class="centered-image-medium">


2. Select 64-bit Git for Windows Setup in Standalone Installer
    - On the download page, select the 64-bit Git for Windows setup.
    - Choose the standalone installer for ease of installation.
<img src="/assets/img/install/bash/git_bash_version_selection.png" alt="Git Bash Version Selection" class="centered-image-medium">

    Note: Unless specified, keep the default settings in the installer.

3. Open Git Bash Setup Tool
    - Run the downloaded Git Bash installer.
<img src="/assets/img/install/bash/git_bash_license.png" alt="Git Bash License" class="centered-image-medium">


4. Keep Default Component Selection
    - The setup tool will present a list of components to install.
    - Keep the default component selection to ensure all necessary components are installed.
<img src="/assets/img/install/bash/git_bash_component_selection.png" alt="Git Bash License" class="centered-image-small">


5. Change Default Branch Name to Main Instead of Master
    - During the setup process, you will be prompted to configure the default branch name for new repositories.
    - Change the default branch name from "master" to "main" to align with modern conventions.
<img src="/assets/img/install/bash/git_bash_default_branch.png" alt="Git Bash Default Branch" class="centered-image-small">


6. Complete Installation and Press Finish
    - Continue through the installation process, keeping the default settings unless you have specific preferences.
    - Once the installation is complete, a prompt will indicate that the process is finished.
<img src="/assets/img/install/bash/git_bash_setup_complete.png" alt="Git Bash Setup Complete" class="centered-image-small">

7. Configure Git Bash to Work with Anaconda
    - If Anaconda is installed for the current user, navigate to the following location:
    
        ```{User} -> AppData -> Local -> miniconda3 -> etc -> profile.d```
    
    - If Anaconda is installed for all users or in the root directory, navigate to:
        
        ```{User} -> miniconda3 -> etc -> profile.d```

    <img src="/assets/img/install/bash/git_bash_toggle.png" alt="Git Bash Toggle" class="centered-image-small">

    <img src="/assets/img/install/bash/git_bash_root_dir.png" alt="Git Bash Root Directory" class="centered-image-medium">

    - Open Git Bash from directory containing profile.d and execute following command:

        ```sh
        echo ". ${PWD}/conda.sh" >> ~/.bashrc
        ```

    - If the path contains spaces even in user name then use following command:

        ```sh
        echo ". '${PWD}'/conda.sh" >> ~/.bashrc
        ```

    - Open a new Git Bash terminal and write conda in it to test if its working:

        ```sh
        conda 
        ```

