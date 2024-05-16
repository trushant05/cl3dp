# Source Code Setup

### 1. Download [southern_research_deployment](https://github.com/Trushant-Adeshara-UM/southern_research_deployment) zip from Github and extract it to desired location:
![](../assets/srcode_download.png)

### 2. Open root directory of southern_research_deployment in Git Bash:
![](../assets/srcode_git_bash.png)

### 3. Create a new conda environment using following command and select y in the prompt:
```
conda create --prefix envs python=3.8
```
![](../assets/srcode_conda_env_create.png)

### 4. Activate conda environment and install dependencies:
```
conda activate ./envs
```

### 5. Possible errors:
```
# sympy not found
pip install sympy

# yaml not found
pip install pyyaml
``
# argparse not found
pip install argparse`
