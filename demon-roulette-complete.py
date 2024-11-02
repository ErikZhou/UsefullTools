import tkinter as tk
import random
import math
from datetime import datetime

class Item:
    """道具类定义"""
    def __init__(self, name, cost, effect, uses=3):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.uses = uses

    def use_item(self, game):
        if self.uses > 0:
            self.effect(game)
            self.uses -= 1
            if self.uses == 0:
                return f"{self.name} 已用完"
        return f"{self.name} 使用成功！剩余次数：{self.uses}"

class DemonRouletteGame:
    def __init__(self, root):
        self.root = root
        self.root.title("恶魔轮盘")
        self.root.geometry("900x900")
        
        # 游戏状态
        self.player_hp = 100
        self.player_gold = 100
        self.level = 1
        self.is_spinning = False
        self.current_angle = 0
        self.boss_chance = 0.1
        self.difficulty_multiplier = 1.0
        self.items = []
        self.bag = []
        
        # 设置轮盘初始值
        self.segments = [
            ("奖励 100 金币", "green"),
            ("惩罚 50 金币", "red"),
            ("神秘事件", "blue"),
            ("奖励 50 金币", "yellow"),
            ("惩罚 100 金币", "orange"),
            ("双倍奖励", "purple"),
        ]
        
        # 状态显示
        self.status_label = tk.Label(root, text=f"关卡: {self.level} | 生命值: {self.player_hp} | 金币: {self.player_gold}", font=("Arial", 16))
        self.status_label.pack(side="top", pady=10)
        
        # 结果显示标签
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)
        
        # 初始化界面元素
        self.create_roulette()
        self.create_buttons()

        # 添加每日签到奖励
        self.daily_reward()

    def create_roulette(self):
        """绘制轮盘并在每个区域添加文字"""
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack(pady=20)
        start_angle = 0
        angle_per_segment = 360 / len(self.segments)
        
        for segment, color in self.segments:
            end_angle = start_angle + angle_per_segment
            self.canvas.create_arc(
                50, 50, 550, 550, start=start_angle, extent=angle_per_segment,
                fill=color, outline="black"
            )
            
            # 根据背景色调整文字颜色，确保对比度
            text_color = "black" if color == "yellow" else "white"
            text_angle = math.radians(start_angle + angle_per_segment / 2)
            x = 300 + 200 * math.cos(text_angle)
            y = 300 - 200 * math.sin(text_angle)
            self.canvas.create_text(x, y, text=segment, fill=text_color, font=("Arial", 12, "bold"))
            
            start_angle = end_angle

    def create_buttons(self):
        """创建按钮并增加UI效果"""
        button_style = {"font": ("Arial", 14, "bold"), "width": 15, "height": 2, "bg": "#333", "fg": "#FFD700", "activebackground": "#555"}
        
        self.spin_button = tk.Button(self.root, text="转动轮盘", command=self.start_spin, **button_style)
        self.spin_button.pack(pady=10)
        
        self.shop_button = tk.Button(self.root, text="商店", command=self.open_shop, **button_style)
        self.shop_button.pack(pady=10)
        
        self.level_button = tk.Button(self.root, text="下一关", command=self.next_level, **button_style)
        self.level_button.pack(pady=10)

    def daily_reward(self):
        """每日签到奖励"""
        today = datetime.now().date()
        if today != getattr(self, 'last_login', None):
            self.last_login = today
            self.player_gold += 50
            self.result_label.config(text="每日签到奖励：+50 金币", fg="green")
            self.update_status()

    def open_shop(self):
        """打开道具商店"""
        shop_window = tk.Toplevel(self.root)
        shop_window.title("道具商店")
        
        items = [
            Item("幸运符", 30, lambda game: game.increase_reward()),
            Item("护盾", 50, lambda game: game.decrease_punishment())
        ]
        
        for item in items:
            item_button = tk.Button(shop_window, text=f"{item.name} - {item.cost} 金币", 
                                    command=lambda i=item: self.buy_item(i))
            item_button.pack()

    def buy_item(self, item):
        """购买道具"""
        if self.player_gold >= item.cost:
            self.player_gold -= item.cost
            self.bag.append(item)
            self.update_status()
            self.result_label.config(text=f"成功购买 {item.name}！", fg="green")
        else:
            self.result_label.config(text="金币不足，无法购买该道具。", fg="red")
        self.update_status()

    def use_item(self, item):
        """使用背包中的道具"""
        if item in self.bag:
            effect_message = item.use_item(self)
            self.result_label.config(text=effect_message, fg="blue")
            if item.uses == 0:
                self.bag.remove(item)
        self.update_status()

    def increase_reward(self):
        """增加奖励效果"""
        self.player_gold += 20
        self.result_label.config(text="幸运符效果：额外获得 20 金币！", fg="gold")
        self.update_status()

    def decrease_punishment(self):
        """减少惩罚效果"""
        self.player_gold += 20  # 减少惩罚的负面效果
        self.result_label.config(text="护盾效果：减少惩罚影响！", fg="blue")
        self.update_status()

    def next_level(self):
        """进入下一关，增加轮盘难度"""
        self.level += 1
        self.difficulty_multiplier += 0.1  # 增加难度
        self.player_hp += 10  # 增加生命值
        self.player_gold += 10  # 奖励金币
        self.boss_chance += 0.05  # BOSS出现几率增加

        if random.random() < self.boss_chance:
            self.segments.append(("BOSS 挑战", "black"))
        
        self.result_label.config(text=f"进入第 {self.level} 关！BOSS出现几率增加！", fg="purple")
        self.update_status()

    def start_spin(self):
        """开始轮盘旋转并添加旋转特效"""
        if not self.is_spinning:
            self.is_spinning = True
            self.spin_speed = random.randint(20, 30)
            self.animate_spin()

    def animate_spin(self):
        """轮盘旋转动画"""
        if self.spin_speed > 0:
            self.current_angle = (self.current_angle + self.spin_speed) % 360
            self.canvas.delete("pointer")
            
            # 绘制带白色边框的指针
            pointer_x = 300 + 250 * math.cos(math.radians(self.current_angle))
            pointer_y = 300 - 250 * math.sin(math.radians(self.current_angle))
            self.canvas.create_line(
                300, 300, pointer_x, pointer_y,
                fill="red", width=4, tags="pointer"
            )
            self.canvas.create_line(
                300, 300, pointer_x, pointer_y,
                fill="white", width=6, tags="pointer"
            )

            self.spin_speed -= random.uniform(0.5, 1.0)
            self.root.after(20, self.animate_spin)
        else:
            self.is_spinning = False
            self.finalize_spin()

    def finalize_spin(self):
        """根据转盘结果执行奖励、惩罚或特殊事件"""
        angle_per_segment = 360 / len(self.segments)
        selected_segment = int((self.current_angle % 360) / angle_per_segment)
        result, color = self.segments[selected_segment]
        
        if "双倍奖励" in result:
            reward = random.choice([50, 100])
            self.player_gold += 2 * reward
            self.result_label.config(text=f"双倍奖励！你获得了 {2 * reward} 金币！", fg="gold")
        
        elif "奖励" in result or "惩罚" in result:
            parts = result.split()
            if len(parts) >= 2 and parts[1].isdigit():
                value = int(parts[1]) * self.difficulty_multiplier
                if "奖励" in result:
                    self.player_gold += int(value)
                    self.result_label.config(text=f"你获得了 {int(value)} 金币！", fg="green")
                elif "惩罚" in result:
                    self.player_gold -= int(value)
                    self.result_label.config(text=f"你失去了 {int(value)} 金币！", fg="red")
            else:
                self.result_label.config(text="无法解析奖励或惩罚内容", fg="orange")
        
        elif "BOSS 挑战" in result:
            boss_damage = int(30 * self.difficulty_multiplier)
            self.player_hp -= boss_damage
            self.result_label.config(text=f"BOSS惩罚！你失去了 {boss_damage} 生命值！", fg="black")
        
        elif "神秘事件" in result:
            mystery_reward = random.randint(-50, 100)
            self.player_gold += mystery_reward
            color = "blue" if mystery_reward > 0 else "purple"
            message = f"神秘事件：你{'获得了' if mystery_reward > 0 else '失去了'} {abs(mystery_reward)} 金币！"
            self.result_label.config(text=message, fg=color)

        self.update_status()

    def update_status(self):
        """更新状态标签"""
        self.status_label.config(text=f"关卡: {self.level} | 生命值: {self.player_hp} | 金币: {self.player_gold}")

# 启动游戏
if __name__ == "__main__":
    root = tk.Tk()
    app = DemonRouletteGame(root)
    root.mainloop()

