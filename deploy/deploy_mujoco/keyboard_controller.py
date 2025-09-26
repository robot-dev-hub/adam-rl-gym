from pynput.keyboard import Listener, Key, KeyCode

class KeyboardController:
    def __init__(self):
        self.lx = 0.0  # 左右移动
        self.ly = 0.0  # 前后移动
        self.rx = 0.0  # 横向旋转
        self.ry = 0.0  # 纵向旋转
        self.listener = None
        self.pressed_keys = set()
        
    def on_press(self, key):
        # 将按键添加到已按下的集合中
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
            self.update_commands()
            # 返回False可以阻止事件继续传播，但会停止监听，所以我们不在这里返回
            
    def on_release(self, key):
        # 从已按下的集合中移除按键
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            self.update_commands()
        # 如果按下的是ESC键，则停止监听
        if key == Key.esc:
            return False
    
    def update_commands(self):
        # 重置所有命令值
        self.lx = 0.0
        self.ly = 0.0
        self.rx = 0.0
        self.ry = 0.0
        
        # 检查是否有按键对象有vk属性，并根据vk值判断是否是小键盘按键
        # 前后移动 (NumPad 8向前, NumPad 5向后 或 I/K键)
        for key in self.pressed_keys:
            # 字符按键检查
            try:
                # I/i 向前
                if hasattr(key, 'char') and key.char in ['8', 'i']:
                    self.ly = 1.0
                # K/k 向后
                elif hasattr(key, 'char') and key.char in ['2', 'k']:
                    self.ly = -1.0
                # J/j 向左
                elif hasattr(key, 'char') and key.char in ['4', 'j']:
                    self.lx = 1.0
                # L/l 向右
                elif hasattr(key, 'char') and key.char in ['6', 'l']:
                    self.lx = -1.0
                # U/u 左转
                elif hasattr(key, 'char') and key.char in ['7', 'u']:
                    self.rx = 1.0
                # O/o 右转
                elif hasattr(key, 'char') and key.char in ['9', 'o']:
                    self.rx = -1.0
            except AttributeError:
                # 忽略没有char属性的按键
                pass
    
    def start(self):
        # 开始监听键盘事件
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("Keyboard controller started.")
        print("Use NumPad or alternative keys to control:")
        print("- NumPad 8/I: Forward, NumPad 2/K: Backward")
        print("- NumPad 4/J: Left, NumPad 6/L: Right")
        print("- NumPad 7/U: Rotate Left, NumPad 9/O: Rotate Right")
    
    def stop(self):
        # 停止监听键盘事件
        if self.listener:
            self.listener.stop()
            self.listener.join()
            self.listener = None
        print("Keyboard controller stopped.")
    
    def get_commands(self):
        # 获取当前的命令值
        return {
            'lx': self.lx,
            'ly': self.ly,
            'rx': self.rx,
            'ry': self.ry
        }