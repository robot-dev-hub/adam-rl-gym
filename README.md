# Adam RL Gym

<div align="center">
  <h1 align="center">Adam RL GYM</h1>
  <p align="center">
    <span> 🌎English </span> | <a href="README_zh.md"> 🇨🇳中文 </a>
  </p>
</div>

<p align="center">
  <strong>This is a repository for reinforcement learning implementation based on Unitree robots, with extended support for Adam robot.</strong> 
</p>

---

## 🌟 Features

- **Support for Multiple Robots**: Includes support for Adam1 Servo robot in addition to Unitree Go2, H1, H1_2, and G1
- **Training Configuration Auto-Save**: Automatically saves training configuration parameters during training
- **Keyboard Control in Mujoco**: Added keyboard control functionality for inference in Mujoco simulation environment
- **Multi-Simulator Support**: Adam1 Servo supports only Isaac Gym and Mujoco deployment testing, Unitree robots support real robot deployment

---

## 📦 Installation and Configuration

Please refer to [setup_en.md](/doc/setup_en.md) for English installation and configuration steps, or [setup_zh.md](/doc/setup_zh.md) for Chinese instructions.

---

## 🔁 Process Overview

The basic workflow for using reinforcement learning to achieve motion control is:

`Train` → `Play` → `Sim2Sim` → `Sim2Real`

- **Train**: Use the Gym simulation environment to let the robot interact with the environment and find a policy that maximizes the designed rewards. Real-time visualization during training is not recommended to avoid reduced efficiency.
- **Play**: Use the Play command to verify the trained policy and ensure it meets expectations.
- **Sim2Sim**: Deploy the Gym-trained policy to other simulators (like Mujoco) to ensure it's not overly specific to Gym characteristics.
- **Sim2Real**: Deploy the policy to a physical robot to achieve motion control.

---

## 🛠️ User Guide

### 1. Training

Run the following command to start training:

```bash
python legged_gym/scripts/train.py --task=adam1_servo
```

#### ⚙️ Parameter Description
- `--task`: Required parameter; values can be (adam1_servo, go2, g1, h1, h1_2).
- `--headless`: Defaults to starting with a graphical interface; set to true for headless mode (higher efficiency).
- `--resume`: Resume training from a checkpoint in the logs.
- `--experiment_name`: Name of the experiment to run/load.
- `--run_name`: Name of the run to execute/load.
- `--load_run`: Name of the run to load; defaults to the latest run.
- `--checkpoint`: Checkpoint number to load; defaults to the latest file.
- `--num_envs`: Number of environments for parallel training.
- `--seed`: Random seed.
- `--max_iterations`: Maximum number of training iterations.
- `--sim_device`: Simulation computation device; specify CPU as `--sim_device=cpu`.
- `--rl_device`: Reinforcement learning computation device; specify CPU as `--rl_device=cpu`.

**Default Training Result Directory**: `logs/<experiment_name>/<date_time>_<run_name>/model_<iteration>.pt`

**Configuration Auto-Save**: The training configuration parameters are automatically saved to `logs/<experiment_name>/<date_time>_<run_name>/config.json`

---

### 2. Play

To visualize the training results in Gym, run the following command:

```bash
python legged_gym/scripts/play.py --task=adam1_servo
```

**Description**:

- Play's parameters are the same as Train's.
- By default, it loads the latest model from the experiment folder's last run.
- You can specify other models using `load_run` and `checkpoint`.

#### 💾 Export Network

Play exports the Actor network, saving it in `logs/{experiment_name}/exported/policies`:
- Standard networks (MLP) are exported as `policy_1.pt`.
- RNN networks are exported as `policy_lstm_1.pt`.

---

### 3. Sim2Sim (Mujoco)

Run Sim2Sim in the Mujoco simulator with keyboard control:

```bash
python deploy/deploy_mujoco/deploy_mujoco.py adam1_servo.yaml
```

#### ⌨️ Keyboard Control

When running in Mujoco, you can control the robot using the following keys:
- **Movement**: NumPad 8/I (Forward), NumPad 2/K (Backward), NumPad 4/J (Left), NumPad 6/L (Right)
- **Rotation**: NumPad 7/U (Rotate Left), NumPad 9/O (Rotate Right)

---

### 4. Sim2Real (Unitree robots only)

For deployment to real robots, please refer to the documentation in the `deploy/deploy_real/` directory.

---

## 📁 Project Structure

```
adam-rl-gym/
├── deploy/                 # Deployment scripts
│   ├── deploy_mujoco/      # Mujoco deployment with keyboard control
│   ├── deploy_real/        # Real robot deployment
│   └── pre_train/          # Pre-trained models
├── doc/                    # Documentation
├── legged_gym/             # Main RL gym library
│   ├── envs/               # Environment implementations
│   │   ├── adam1_servo/    # Adam1 Servo robot environment
│   │   ├── g1/             # Unitree G1 robot environment
│   │   ├── go2/            # Unitree Go2 robot environment
│   │   ├── h1/             # Unitree H1 robot environment
│   │   ├── h1_2/           # Unitree H1_2 robot environment
│   │   └── base/           # Base environment classes
│   ├── scripts/            # Training and playback scripts
│   └── utils/              # Utility functions
├── resources/              # Robot URDF and mesh files
└── rsl_rl/                 # RL algorithm implementation
```

---

## 📝 License

This project retains the original [BSD-3-Clause](LICENSE) license from Unitree RL Gym.

---

## Acknowledgements

This project is based on the original Unitree RL Gym framework. Special thanks to the original developers for their contributions.