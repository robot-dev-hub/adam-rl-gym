from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO


class Adam1ServoRoughCfg(LeggedRobotCfg):

    class init_state(LeggedRobotCfg.init_state):
        pos = [0.0, 0.0, 0.45]  # x,y,z [m]
        default_joint_angles = { # = target angles [rad] when action = 0.0
            'left_hip_yaw_joint': 0,
            'left_hip_roll_joint': 0,
            'left_hip_pitch_joint': -0.15,
            'left_knee_joint': -0.35,
            'left_ankle_roll_joint': 0.0,
            'left_ankle_pitch_joint': -0.2,

            'right_hip_yaw_joint': 0,
            'right_hip_roll_joint': 0,
            'right_hip_pitch_joint': -0.15,
            'right_knee_joint': -0.35,
            'right_ankle_roll_joint': 0.0,
            'right_ankle_pitch_joint': -0.2,

            'torso_joint': 0,

            'left_shoulder_pitch_joint': 0.,
            'left_shoulder_roll_joint': 0,
            'left_shoulder_yaw_joint': 0,
            'left_elbow_pitch_joint': 0.,

            'right_shoulder_pitch_joint': 0.,
            'right_shoulder_roll_joint': 0,
            'right_shoulder_yaw_joint': 0,
            'right_elbow_pitch_joint': 0.,
        }

    class env(LeggedRobotCfg.env):
        # 3 + 3 + 3 + 12 + 12 + 12 + 2 = 47
        num_observations = 47
        num_privileged_obs = 50
        num_actions = 12
      

    class control(LeggedRobotCfg.control):
        # PD Drive parameters:
        control_type = 'P'
        # PD Drive parameters
        stiffness = {
            'hip_yaw_joint': 5,    
            'hip_roll_joint': 5,   
            'hip_pitch_joint': 5,  
            'knee_joint': 10.,       
            'ankle_roll_joint': 3,  
            'ankle_pitch_joint': 3, 
        }  # [N*m/rad] 
        damping = {
            'hip_yaw_joint': 0.3,
            'hip_roll_joint': 0.3,
            'hip_pitch_joint': 0.3,
            'knee_joint': 0.5,
            'ankle_roll_joint': 0.1,
            'ankle_pitch_joint': 0.1,
        }  # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 8

    class sim(LeggedRobotCfg.sim):
        dt =  0.0025

    class domain_rand(LeggedRobotCfg.domain_rand):
        randomize_friction = True
        friction_range = [0.1, 1.25]
        randomize_base_mass = True
        added_mass_range = [-1., 3.]
        push_robots = True
        push_interval_s = 3
        max_push_vel_xy = 0.8

    class asset(LeggedRobotCfg.asset):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/adam1_servo/urdf/adam1_servo_12dof.urdf'
        name = "adam1_servo"
        foot_name = "ankle_pitch"
        penalize_contacts_on = ["hip", "knee"]
        terminate_after_contacts_on = ["pelvis"]
        self_collisions = 0  # 1 to disable, 0 to enable...bitwise filter
        flip_visual_attachments = False
        armature = 1e-3

    class rewards(LeggedRobotCfg.rewards):
        soft_dof_pos_limit = 0.9
        base_height_target = 0.45

        class scales(LeggedRobotCfg.rewards.scales):
            tracking_lin_vel = 1.0
            tracking_ang_vel = 0.5
            lin_vel_z = -2.0
            ang_vel_xy = -0.05
            orientation = -1.0
            base_height = -10.0
            dof_acc = -2.5e-7
            dof_vel = -1e-3
            feet_air_time = 0.0
            collision = 0.0
            action_rate = -0.01
            dof_pos_limits = -5.0
            alive = 0.15
            hip_pos = -1.0
            contact_no_vel = -0.2
            feet_swing_height = -20.0
            contact = 0.18


class Adam1ServoRoughCfgPPO(LeggedRobotCfgPPO):
    class policy:
        init_noise_std = 0.8
        actor_hidden_dims = [32]
        critic_hidden_dims = [32]
        activation = 'elu' # can be elu, relu, selu, crelu, lrelu, tanh, sigmoid
        # only for 'ActorCriticRecurrent':
        rnn_type = 'lstm'
        rnn_hidden_size = 64
        rnn_num_layers = 1
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
    class runner( LeggedRobotCfgPPO.runner ):
        policy_class_name = "ActorCriticRecurrent"
        # policy_class_name = "ActorCritic"   # for onnx
        max_iterations = 10000
        run_name = ''
        experiment_name = 'adam1_servo'