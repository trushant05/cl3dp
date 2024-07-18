# Introduction

<p align="justify">This guide provides a comprehensive walkthrough for installing, testing, and conducting ink printing experiments using Aerotech stages. The document outlines the essential software installations necessary for the process and offers a brief overview of each software component.</p>

<p align="justify"> Note: This document is targeted towards setup in Barton Research Group at University of Michigan. If you intend to develop for company in collaboration, there are some changes in hardware which are as follow:</p>

### Vision System
<p align="justify"> Cameras used at UofM is manufactured by Basler which uses PylonSDK. Pylon library for that is called PyPylon which can be installed from upstream package manager like Pip. </p>

<p align="justify"> While in case of company in collaboration, the camera is manufactured by Teledyne Flir which uses Spinnaker SDK. Spinnaker has customized Python SDK which can only be downloaded from their website. Make sure to check version of base SDK and Python one since they need to be same for compatibility.</p>

### Printing System
<p align="justify"> Stages used at UofM and company in collaboration are from the same manufacturer and hence the codebase is similar. There is a small difference in extrusion system. For UofM system, the pressure is used to control extrusion so apply pressure to print and cut suppy to stop. While in case of company, they have an extra 4th stage which acts as a smart pump. For them the pressure is kept on for the entire experiment and this 4th stage moves up-down to allow flow of ink.</p>
