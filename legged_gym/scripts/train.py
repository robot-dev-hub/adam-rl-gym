import os
import numpy as np
from datetime import datetime
import sys
import json

import isaacgym
from legged_gym.envs import *
from legged_gym.utils import get_args, task_registry
import torch

def save_config_to_log_dir(env_cfg, log_dir):
    """保存环境配置到日志目录"""
    # 创建配置保存目录（如果不存在）
    os.makedirs(log_dir, exist_ok=True)
    
    # 将配置转换为字典
    cfg_dict = {}
    # 重点保存control部分
    if hasattr(env_cfg, 'control'):
        cfg_dict['control'] = {}
        # 获取control的所有属性
        for attr in dir(env_cfg.control):
            if not attr.startswith('_'):
                value = getattr(env_cfg.control, attr)
                # 确保值是可序列化的
                try:
                    json.dumps(value)
                    cfg_dict['control'][attr] = value
                except (TypeError, OverflowError):
                    # 如果值不可序列化，尝试转换为字符串
                    try:
                        cfg_dict['control'][attr] = str(value)
                    except:
                        pass
    
    # 保存配置到JSON文件
    config_path = os.path.join(log_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(cfg_dict, f, indent=4)
    
    print(f"配置已保存到: {config_path}")

def train(args):
    env, env_cfg = task_registry.make_env(name=args.task, args=args)
    ppo_runner, train_cfg = task_registry.make_alg_runner(env=env, name=args.task, args=args)
    
    # 获取日志目录并保存配置
    log_dir = ppo_runner.log_dir
    if log_dir is not None:
        save_config_to_log_dir(env_cfg, log_dir)
    
    ppo_runner.learn(num_learning_iterations=train_cfg.runner.max_iterations, init_at_random_ep_len=True)

if __name__ == '__main__':
    args = get_args()
    train(args)
