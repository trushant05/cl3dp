# Git Bash

### 1. Download [Git Bash](https://git-scm.com/download/win) from Git website:
![](../assets/git_bash_download.png)

### 2. Select **64-bit** Git for Windows Setup in **Standalone Installer**:
![](../assets/git_bash_version_selection.png)

## Note: Unless specified below keep default settings in installer.

### 3. Open Git Bash setup tool:
![](../assets/gitbash_license.png)

### 4. Keep default component selection:
![](../assets/gitbash_component_selection.png)

### 5. Change default branch to main instead of master:
![](../assets/gitbash_default_branch.png)

### 6. Complete installation and press Finish:
![](../assets/gitbash_setup_complete.png)

### 7. Configure Git Bash to work with Anaconda:
 If Anaconda is installed for current user then navigate to following location, else look for it in the root directory. Got to your user directory as follow:

Goto **{User} -> AppData -> Local -> miniconda3 -> etc -> profile.d** 

Alternative location **{User} -> miniconda3 -> etc -> profile.d**

![](../assets/git_bash_toggle.png)
![](../assets/git_bash_hidden.png)


- Open Git Bash from directory containing profile.d and execute following command:
```
echo ". ${PWD}/conda.sh" >> ~/.bashrc
```

- If the path contains spaces even in user name then use following command:
```
echo ". '${PWD}'/conda.sh" >> ~/.bashrc
```

- Open a new Git Bash terminal and write conda in it to test if its working.
