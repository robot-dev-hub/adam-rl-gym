# Adam RL Gym

<div align="center">
  <h1 align="center">Adam RL GYM</h1>
  <p align="center">
    <a href="README.md"> 🌎English </a> | <span> 🇨🇳中文 </span>
  </p>
</div>

<p align="center">
  <strong>这是一个基于Unitree机器人的强化学习实现仓库，并扩展支持Adam机器人。</strong> 
</p>

---

## 🌟 功能特性

- **多机器人支持**：除了Unitree的Go2、H1、H1_2和G1机器人外，还支持Adam1 Servo机器人
- **训练配置自动保存**：在训练过程中自动保存训练配置参数
- **Mujoco环境键盘控制**：在Mujoco仿真环境中添加了键盘控制功能
- **多模拟器支持**：Adam1 Servo仅支持Isaac Gym和Mujoco部署测试，Unitree支持在真实机器人部署

---

## 📦 安装与配置

请参考[setup_zh.md](/doc/setup_zh.md)获取中文安装和配置步骤，或[setup_en.md](/doc/setup_en.md)获取英文说明。

---

## 🔁 流程概述

使用强化学习实现运动控制的基本工作流程是：

`训练` → `播放` → `模拟到模拟` → `模拟到现实`

- **训练**：使用Gym仿真环境让机器人与环境交互，寻找最大化设计奖励的策略。不建议在训练期间进行实时可视化，以避免降低效率。
- **播放**：使用Play命令验证训练好的策略，确保其符合预期。
- **模拟到模拟**：将在Gym中训练的策略部署到其他模拟器（如Mujoco），确保其不会过度适应Gym的特性。
- **模拟到现实**：将策略部署到物理机器人上，实现运动控制（仅Unitree机器人）。

---

## 🛠️ 用户指南

### 1. 训练

运行以下命令开始训练：

```bash
python legged_gym/scripts/train.py --task=adam1_servo
```

#### ⚙️ 参数说明
- `--task`：必填参数；值可以是(adam1_servo, go2, g1, h1, h1_2)。
- `--headless`：默认以图形界面启动；设置为true可进入无头模式（效率更高）。
- `--resume`：从日志中的检查点恢复训练。
- `--experiment_name`：要运行/加载的实验名称。
- `--run_name`：要执行/加载的运行名称。
- `--load_run`：要加载的运行名称；默认为最新运行。
- `--checkpoint`：要加载的检查点编号；默认为最新文件。
- `--num_envs`：并行训练的环境数量。
- `--seed`：随机种子。
- `--max_iterations`：最大训练迭代次数。
- `--sim_device`：仿真计算设备；指定CPU为`--sim_device=cpu`。
- `--rl_device`：强化学习计算设备；指定CPU为`--rl_device=cpu`。

**默认训练结果目录**：`logs/<experiment_name>/<date_time>_<run_name>/model_<iteration>.pt`

**配置自动保存**：训练配置参数会自动保存到`logs/<experiment_name>/<date_time>_<run_name>/config.json`

---

### 2. 播放

要在Gym中可视化训练结果，请运行以下命令：

```bash
python legged_gym/scripts/play.py --task=adam1_servo
```

**说明**：

- Play的参数与Train的参数相同。
- 默认情况下，它会加载实验文件夹最后一次运行中的最新模型。
- 您可以使用`load_run`和`checkpoint`指定其他模型。

#### 💾 导出网络

Play会导出Actor网络，将其保存在`logs/{experiment_name}/exported/policies`中：
- 标准网络（MLP）导出为`policy_1.pt`。
- RNN网络导出为`policy_lstm_1.pt`。

---

### 3. 模拟到模拟（Mujoco）

在Mujoco模拟器中运行Sim2Sim，支持键盘控制：

```bash
python deploy/deploy_mujoco/deploy_mujoco.py adam1_servo.yaml
```

#### ⌨️ 键盘控制

在Mujoco中运行时，您可以使用以下按键控制机器人：
- **移动**：小键盘8/I（前进），小键盘2/K（后退），小键盘4/J（左移），小键盘6/L（右移）
- **旋转**：小键盘7/U（左转），小键盘9/O（右转）

---

### 4. 模拟到现实(仅Unitree 机器人)

有关部署到真实机器人的信息，请参阅`deploy/deploy_real/`目录中的文档。

---

## 📁 项目结构

```
adam-rl-gym/
├── deploy/                 # 部署脚本
│   ├── deploy_mujoco/      # 带键盘控制的Mujoco部署
│   ├── deploy_real/        # 真实机器人部署
│   └── pre_train/          # 预训练模型
├── doc/                    # 文档
├── legged_gym/             # 主要RL gym库
│   ├── envs/               # 环境实现
│   │   ├── adam1_servo/    # Adam1 Servo机器人环境
│   │   ├── g1/             # Unitree G1机器人环境
│   │   ├── go2/            # Unitree Go2机器人环境
│   │   ├── h1/             # Unitree H1机器人环境
│   │   ├── h1_2/           # Unitree H1_2机器人环境
│   │   └── base/           # 基础环境类
│   ├── scripts/            # 训练和播放脚本
│   └── utils/              # 实用函数
├── resources/              # 机器人URDF和网格文件
└── rsl_rl/                 # RL算法实现
```

---

## 📝 许可证

该项目保留了Unitree RL Gym原始的[BSD-3-Clause](LICENSE)许可证。

---

## 致谢

本项目基于原始的Unitree RL Gym框架。特别感谢原始开发者的贡献。