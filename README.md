# Thesis Master UI  

[![Forks][forks-shield]][forks-url]  
[![Stargazers][stars-shield]][stars-url]  
[![Issues][issues-shield]][issues-url]  
[![MIT License][license-shield]][license-url]  
[![LinkedIn][linkedin-shield]][linkedin-url]  

---

## Introduction  
**Thesis Master UI** is a graphical user interface (GUI) built with **Tkinter/CustomTkinter** to help users run the materials simulation pipeline without needing to use command line tools.  
This application connects directly to the `ThesisMaster` backend to:  
- Select training, result, and prediction data directories.  
- Start or stop simulation processes.  
- Monitor logs and process status in real-time.  
- Receive notifications when finished or if errors occur.  

⚠️ **Important**: You must **install and set up the backend environment** before running the UI. The UI only acts as a controller for the backend pipeline.  

---

## Relation to Backend  

The **Thesis Master project** consists of two parts:  

1. **Backend (Core Engine)**  
   - Contains all the actual simulation scripts and logic.  
   - Requires environment setup, dependencies, and shell scripts (`scripts/run_script.sh`).  
   - Handles training, prediction, and evaluation tasks.  

2. **Frontend (This UI)**  
   - Provides a user-friendly desktop interface.  
   - Passes user-selected paths and parameters to the backend.  
   - Displays progress, logs, and results in real time.  

👉 The UI cannot function on its own. It relies on the backend to perform computations, while the UI focuses only on visualization and control.  

---

## Installation  

### Requirements  
- Linux Ubuntu 20.04 (22.04 and 24.04 also)
- Miniconda already installed  
- Backend `ThesisMaster` cloned and environment variable `ROOT_WS_DUY` configured
> **Note:** The environment variable `ROOT_WS_DUY` must point to the directory where you cloned the project.  
> For example, if you cloned the code into `/home/user/my_workspace/ThesisMaster`, then set:  
> ```bash
> export ROOT_WS_DUY="/home/user/my_workspace"
> ```


### Setup  

1. Navigate to the project folder:  
   ```bash
   cd $ROOT_WS_DUY/ThesisMaster/setups/linux
   ```
2. Run the setup script to install the Conda environment:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
This will create (or recreate) a Conda environment named thesis-master from the provided environment.yaml
3. Activate the environment:
   ```bash
   conda activate thesis-master
   ```

### Run the UI  
1. Clone the repository and navigate to the UI folder:  
   ```bash
   git clone https://github.com/IricsDo/ThesisMasterUI.git
   cd ThesisMasterUI/ThesisMasterUI_Tkinter
   ```  
2. Launch the UI:  
   ```bash
   python app.py
   ```

---

## Usage Guide  

1. **Select directories**  
   - **Training Data Path**: required for training.  
   - **Result Path**: required output location.  
   - **Predict Path**: optional, used for prediction input.  

2. **Configure arguments (Settings)**  
   - Additional backend arguments will appear in the *Settings* section.  
   - ⚠️ *Currently the UI has placeholders for some arguments; you may update them later as needed.*  

3. **Control the pipeline**  
   - Press **Start** to launch the process.  
   - Logs are displayed in a separate log window.  
   - Press **Stop** to terminate a running process.  
   - Press **Reset** to clear inputs and restart.  

4. **Monitor progress**  
   - The progress bar shows process completion percentage.  
   - Colors indicate different states (running, finished, error).  
   - Notifications will pop up when the process finishes or fails.  

---

## UI Screenshots  

*(Insert UI screenshots here)*  

---

## Contact  
**Do Duy** – [LinkedIn](https://www.linkedin.com/in/duy-do-61a37b1a4/) – iric.life1407@gmail.com  

---

[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge  
[forks-url]: https://github.com/IricsDo/ThesisMaster/forks  
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge  
[stars-url]: https://github.com/IricsDo/ThesisMaster/stargazers  
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge  
[issues-url]: https://github.com/IricsDo/ThesisMaster/issues  
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge  
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt  
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555  
[linkedin-url]: https://linkedin.com/in/duy-do-61a37b1a4  
