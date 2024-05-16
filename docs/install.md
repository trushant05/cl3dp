# Installation Overview

### A3200 Motion Control Software

<p align="justify">Developed by Aerotech, the A3200 software facilitates interaction with motion stages. While the Motion Composer is typically employed, integration with MATLAB or Python scripts is also supported. This guide emphasizes a Python-based approach, highlighting how to utilize the A3200's communication features to interface with the ASCII server and control the stages via the host computer's IP address.</p>

### Camera Integration for Feedback

<p align="justify">The implementation incorporates vision algorithms utilizing cameras from Basler (Pylon) and Blackfly. These cameras serve as feedback mechanisms, enabling precise line width estimation for controller inputs. Python APIs provided by both camera manufacturers are leveraged to maximize their functionalities.</p>

### Anaconda for Python Environment Management

<p align="justify">Given that the project is Python-centric, managing different Python package versions is crucial. This guide recommends using Conda environments for this purpose. Conda is highly effective in duplicating a set of dependencies, streamlining the setup process.</p>

### Git Bash for Windows Development

<p align="justify">The development environment is based on Windows, where native Linux commands are not directly applicable. Git Bash is introduced as a solution to this limitation. This guide includes instructions to configure Conda within Git Bash, addressing the absence of native Conda support.</p>

### Source Code and Initial Setup

<p align="justify">The software package is hosted on GitHub. Detailed instructions for the initial setup and configuration are provided. While new system installations may encounter missing dependencies, this guide assures easy resolution through pip or Conda, ensuring a smooth environment setup.</p>

