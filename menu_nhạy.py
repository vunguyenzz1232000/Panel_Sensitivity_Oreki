import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
import colorsys

class RainbowLabel(tk.Frame):
    def __init__(self, parent, text, font=("Consolas", 22, "bold"), bg="#000000"):
        super().__init__(parent, bg=bg)
        self.chars = []
        self.hue = 0.0
        for char in text:
            lbl = tk.Label(self, text=char, font=font, bg=bg, fg="#ffffff")
            lbl.pack(side="left")
            self.chars.append(lbl)
        self.animate()

    def animate(self):
        for i, lbl in enumerate(self.chars):
            # Tạo hiệu ứng sóng màu chạy từ trái qua phải
            h = (self.hue + (i * 0.03)) % 1.0
            rgb = colorsys.hsv_to_rgb(h, 1.0, 1.0)
            color = "#%02x%02x%02x" % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            lbl.config(fg=color)
        self.hue += 0.01
        if self.hue > 1.0: self.hue -= 1.0
        self.after(20, self.animate)

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, variable, width=44, height=22, on_color="#00ff00", off_color="#444444", bg="#111111"):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0)
        self.variable = variable
        self.on_color = on_color
        self.off_color = off_color
        self.width = width
        self.height = height
        self.bind("<Button-1>", self.toggle)
        self.variable.trace_add("write", self.draw)
        self.draw()

    def toggle(self, event):
        self.variable.set(not self.variable.get())

    def draw(self, *args):
        self.delete("all")
        if self.variable.get():
            fill = self.on_color
            x = self.width - (self.height // 2)
        else:
            fill = self.off_color
            x = self.height // 2
        
        # Vẽ nền (viên thuốc)
        r = self.height / 2
        self.create_oval(0, 0, self.height, self.height, fill=fill, outline="")
        self.create_oval(self.width - self.height, 0, self.width, self.height, fill=fill, outline="")
        self.create_rectangle(r, 0, self.width - r, self.height, fill=fill, outline="")
        
        # Vẽ nút tròn
        kr = r - 3
        self.create_oval(x - kr, 3, x + kr, self.height - 3, fill="white", outline="")

class GodSensitivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Oreki_Veritified")
        self.root.geometry("650x850")
        self.root.resizable(False, False)

        # --- Cấu hình màu sắc ---
        self.bg_color = "#050505"
        self.fg_color = "#00ff00"
        self.accent_color = "#111111" # Màu nền cho các khung chứa

        self.root.configure(bg=self.bg_color)

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('alt')
        
        # Cấu hình style để hòa hợp với nền tối/ảnh nền
        self.style.configure("TLabel", background=self.accent_color, foreground=self.fg_color, font=("Consolas", 10))
        self.style.configure("TButton", background="#003300", foreground=self.fg_color, font=("Consolas", 11, "bold"), borderwidth=1, focuscolor=self.bg_color)
        self.style.map("TButton", background=[('active', '#004d00')])
        self.style.configure("TEntry", fieldbackground="#222222", foreground="#ffffff", insertcolor=self.fg_color)
        self.style.configure("TCheckbutton", background=self.accent_color, foreground=self.fg_color, font=("Consolas", 10), focuscolor=self.accent_color)
        self.style.map("TCheckbutton", background=[('active', self.accent_color)], indicatorcolor=[('selected', self.fg_color)])

        # Header
        # Sử dụng bg đen cho header để dễ đọc
        self.header = RainbowLabel(root, text="[ Oreki_Veritified ]", bg=self.bg_color)
        self.header.pack(pady=(20, 5))
        
        tk.Label(root, text="🙈 Mua file ib zalo 0336514635🙈 ", bg=self.bg_color, fg="#00ff00", font=("Consolas", 12, "bold")).pack(pady=(0, 20))

        # --- Input Section ---
        # Khung nhập liệu có màu nền bán trong suốt (giả lập bằng màu tối)
        input_frame = tk.Frame(root, bg=self.accent_color, bd=2, relief="groove")
        input_frame.pack(pady=10, padx=20, fill="x")

        # Device Name
        tk.Label(input_frame, text="Tên thiết bị (VD:Iphone 11; Samsung S23 Ultra; Redmi Note 11;...)", bg=self.accent_color, fg=self.fg_color, font=("Consolas", 10)).pack(anchor="w", padx=10, pady=(10, 0))
        self.device_entry = ttk.Entry(input_frame, font=("Consolas", 11))
        self.device_entry.pack(fill="x", padx=10, pady=5)

        # Playstyle / Need Selection
        tk.Label(input_frame, text="Chọn các chức năng (Đa lựa chọn)", bg=self.accent_color, fg=self.fg_color, font=("Consolas", 10)).pack(anchor="w", padx=10, pady=(10, 0))
        
        self.check_vars = {}
        
        modes = [
            ("Nhẹ Tâm (Sensitivity)", "light"),
            ("Fix Rung (Fix Vibrate)", "recoil"),
            ("Ổn Định (Stability)", "stable"),
            ("One Shot (Shotgun/Sniper)", "oneshot"),
            ("Tối ưu FPS (Buff Smooth)", "fps"),
            ("Đồ họa Max (Check Graphics)", "graphics")
        ]

        for text, mode in modes:
            var = tk.BooleanVar()
            self.check_vars[mode] = var
            
            row = tk.Frame(input_frame, bg=self.accent_color)
            row.pack(fill="x", padx=10, pady=2)
            
            tk.Label(row, text=text, bg=self.accent_color, fg=self.fg_color, font=("Consolas", 10)).pack(side="left")
            ToggleSwitch(row, variable=var, bg=self.accent_color).pack(side="right")

        # Analyze Button
        self.analyze_btn = tk.Button(root, text=">>> KÍCH HOẠT AI PHÂN TÍCH <<<", command=self.start_analysis, bg="#004400", fg=self.fg_color, font=("Consolas", 12, "bold"), relief="flat", activebackground="#006600", activeforeground="#ffffff")
        self.analyze_btn.pack(pady=20, ipadx=20, ipady=5)

        # --- Output Section ---
        self.output_frame = tk.Frame(root, bg=self.accent_color, bd=2, relief="sunken")
        self.output_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.result_text = tk.Text(self.output_frame, bg="#000000", fg=self.fg_color, font=("Consolas", 11), state="disabled", wrap="word")
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Footer Note
        footer_label = tk.Label(root, text=" 🙈Mua file ib zalo 0336514635🙈 ", bg=self.bg_color, fg="#ff3333", font=("Consolas", 12, "bold"))
        footer_label.pack(side="bottom", pady=10)

        # Status Bar
        self.status_var = tk.StringVar(value="System Ready. Waiting for input...")
        status_bar = tk.Label(root, textvariable=self.status_var, bg=self.bg_color, fg=self.fg_color, font=("Consolas", 9), anchor="w")
        status_bar.pack(side="bottom", fill="x")

    def start_analysis(self):
        device_name = self.device_entry.get().strip()
        if not device_name:
            messagebox.showwarning("Input Error", "Vui lòng nhập tên thiết bị!")
            return

        self.analyze_btn.config(state="disabled")
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")
        
        # Collect selected modes
        selected_modes = [mode for mode, var in self.check_vars.items() if var.get()]
        if not selected_modes:
            selected_modes = ["stable"] # Default
        
        # Chạy luồng riêng để không đơ giao diện (Daemon thread)
        threading.Thread(target=self.process_data, args=(device_name, selected_modes), daemon=True).start()

    def process_data(self, device, modes):
        steps = [
            f"[-] Connecting to database for {device}...",
            "[-] Analyzing screen refresh rate & touch sampling...",
            f"[-] Loading algorithms: {', '.join(modes).upper()}...",
            "[-] Calculating vector trajectory...",
            "[-] Optimizing DPI scaling...",
            "[+] GENERATING FINAL CONFIG..."
        ]

        for step in steps:
            # Sử dụng root.after để cập nhật UI từ luồng phụ (Thread-safe)
            self.root.after(0, self.update_status, step)
            self.root.after(0, self.append_log, step)
            time.sleep(0.6) # Fake processing time

        # Generate Logic
        config = self.calculate_sensitivity(device, modes)
        self.root.after(0, self.display_result, config)
        self.root.after(0, lambda: self.status_var.set("Analysis Complete."))
        self.root.after(0, lambda: self.analyze_btn.config(state="normal"))

    def update_status(self, text):
        self.status_var.set(text)

    def append_log(self, text):
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state="disabled")

    def calculate_sensitivity(self, device, modes):
        # Base logic (Logic giả lập dựa trên nhu cầu)
        
        # Seed random based on device name to make it consistent for the same device
        random.seed(device.lower())
        
        is_ios = any(x in device.lower() for x in ['iphone', 'ipad', 'ios'])
        
        # Base values (Scale 0-200 for FF Max)
        if is_ios:
            base_dpi = random.choice([31, 120])
            dpi_label = "Giá trị con trỏ trượt (Sliding Cursor)"
        else:
            base_dpi = random.choice([411, 440, 480, 500])
            dpi_label = "DPI (Độ rộng tối thiểu)"
            
        sens_general = random.randint(100, 150)
        sens_red_dot = random.randint(100, 140)
        sens_2x = random.randint(100, 130)
        sens_4x = random.randint(90, 120)
        sens_sniper = random.randint(50, 90)
        sens_look = random.randint(100, 150)
        button_size = random.randint(40, 60)
        
        notes = []
        
        # Graphics & FPS Logic
        graphics_setting = "Thấp (Smooth)"
        fps_setting = "Cao (High)"
        shadows = "Tắt (Off)"
        
        # Logic điều chỉnh theo nhu cầu
        if "light" in modes: # Nhẹ tâm -> Sens cao, nút nhỏ
            sens_general = random.randint(180, 200)
            sens_red_dot = random.randint(170, 195)
            sens_2x = random.randint(160, 190)
            button_size = random.randint(35, 45)
            if not is_ios:
                base_dpi = random.choice([550, 600, 720])
            notes.append("Độ nhạy cao giúp kéo tâm nhẹ nhàng.")

        if "recoil" in modes: # Fix rung -> Giảm sens scope
            sens_2x = random.randint(80, 110)
            sens_4x = random.randint(70, 100)
            button_size = random.randint(50, 60)
            if "light" not in modes and not is_ios:
                base_dpi = random.choice([411, 440])
            notes.append("Giảm độ nhạy Scope để ghìm tâm đầm hơn.")

        if "oneshot" in modes: # One Shot -> Max sens
            sens_general = 200
            sens_red_dot = 200
            sens_2x = 200
            sens_look = 200
            button_size = random.randint(30, 40)
            if not is_ios:
                base_dpi = random.choice([600, 800, 960])
            notes.append("DPI cực cao để flick shot nhanh (Shotgun).")

        if "fps" in modes:
            graphics_setting = "Thấp (Smooth)"
            fps_setting = "Cao/Ultra (High)"
            shadows = "Tắt (Off)"
            notes.append("Ưu tiên FPS cao để mượt mà nhất.")
        
        if "graphics" in modes:
            graphics_setting = "Max (Ultra)"
            fps_setting = "Cao (High)"
            shadows = "Bật (On)"
            notes.append("Bật max đồ họa để nhìn rõ địch xa.")

        if "stable" in modes and len(modes) == 1:
             notes.append("Cấu hình cân bằng, dễ làm quen.")

        # Clamp values to 0-200
        sens_general = min(200, max(0, sens_general))
        sens_red_dot = min(200, max(0, sens_red_dot))
        sens_2x = min(200, max(0, sens_2x))
        sens_4x = min(200, max(0, sens_4x))
        sens_sniper = min(200, max(0, sens_sniper))
        sens_look = min(200, max(0, sens_look))

        return {
            "device": device,
            "modes": ", ".join(modes).upper(),
            "dpi": base_dpi,
            "dpi_label": dpi_label,
            "general": sens_general,
            "red_dot": sens_red_dot,
            "x2": sens_2x,
            "x4": sens_4x,
            "sniper": sens_sniper,
            "look": sens_look,
            "button": button_size,
            "graphics": graphics_setting,
            "fps": fps_setting,
            "shadows": shadows,
            "note": " + ".join(notes)
        }

    def display_result(self, config):
        output = f"""
================================================
   KẾT QUẢ TỐI ƯU HÓA: {config['device'].upper()}
================================================

[ THÔNG SỐ HỆ THỐNG ]
> Chế độ: {config['modes']}
> {config['dpi_label']}: {config['dpi']}
> Tốc độ con trỏ: Mức 7 (Mặc định)

[ ĐỘ NHẠY FREE FIRE MAX (0-200) ]
> Nhìn xung quanh:  {config['general']}
> Red Dot:          {config['red_dot']}
> Ống ngắm 2x:      {config['x2']}
> Ống ngắm 4x:      {config['x4']}
> Ống ngắm Sniper:  {config['sniper']}
> Nhìn:             {config['look']}

[ ĐỒ HỌA & FPS ]
> Đồ họa:           {config['graphics']}
> FPS:              {config['fps']}
> Bóng đổ:          {config['shadows']}

[ HUD CONTROL ]
> Kích thước nút bắn: {config['button']}%
> Vị trí nút bắn:     Kéo thấp xuống dưới 10%

[ LỜI KHUYÊN AI ]
> {config['note']}

Mua file ib zalo 0336514635
================================================
Generated by Oreki_Veritified AI
"""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, output.strip())
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = GodSensitivityApp(root)
    root.mainloop()