import tkinter as tk
from datetime import datetime
import math
import os

class AnalogAlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Analog Clock with Alarm")
        self.root.geometry("400x550")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # Alarm Variables
        self.alarm_time = None
        self.alarm_active = False
        self.is_ringing = False

        # Build UI Elements
        self.create_clock_face()
        self.create_alarm_inputs()

        # Start the clock loop
        self.update_clock()

    def create_clock_face(self):
        # Canvas for Drawing the Analog Clock
        self.canvas = tk.Canvas(self.root, width=350, height=350, bg="#2c3e50", bd=0, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        self.center_x = 175
        self.center_y = 175
        self.radius = 150

    def draw_clock_components(self, now):
        self.canvas.delete("all")

        # Outer Rim
        self.canvas.create_oval(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            fill="#ecf0f1", outline="#34495e", width=8
        )

        # Center Dial Pin
        self.canvas.create_oval(
            self.center_x - 6, self.center_y - 6,
            self.center_x + 6, self.center_y + 6,
            fill="#2c3e50", outline=""
        )

        # Hour Markings / Numbers
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = self.center_x + (self.radius - 25) * math.cos(angle)
            y = self.center_y + (self.radius - 25) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), font=("Helvetica", 14, "bold"), fill="#2c3e50")

        # Extract Time Components
        hour = now.hour % 12
        minute = now.minute
        second = now.second

        # Calculate Angles (adjusted by -90 degrees so 0 points straight up at 12 o'clock)
        sec_angle = math.radians((second * 6) - 90)
        min_angle = math.radians((minute * 6) + (second * 0.1) - 90)
        hour_angle = math.radians((hour * 30) + (minute * 0.5) - 90)

        # Draw Hour Hand (Short & Thick)
        hx = self.center_x + (self.radius - 60) * math.cos(hour_angle)
        hy = self.center_y + (self.radius - 60) * math.sin(hour_angle)
        self.canvas.create_line(self.center_x, self.center_y, hx, hy, fill="#2c3e50", width=6, capstyle=tk.ROUND)

        # Draw Minute Hand (Long & Medium Thick)
        mx = self.center_x + (self.radius - 35) * math.cos(min_angle)
        my = self.center_y + (self.radius - 35) * math.sin(min_angle)
        self.canvas.create_line(self.center_x, self.center_y, mx, my, fill="#34495e", width=4, capstyle=tk.ROUND)

        # Draw Second Hand (Thin & Red)
        sx = self.center_x + (self.radius - 20) * math.cos(sec_angle)
        sy = self.center_y + (self.radius - 20) * math.sin(sec_angle)
        self.canvas.create_line(self.center_x, self.center_y, sx, sy, fill="#e74c3c", width=2)

    def create_alarm_inputs(self):
        # Entry Frame
        input_frame = tk.Frame(self.root, bg="#2c3e50")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="HH :", font=("Helvetica", 12, "bold"), fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=0, padx=2)
        self.hour_entry = tk.Entry(input_frame, width=3, font=("Helvetica", 14), justify="center")
        self.hour_entry.insert(0, "07")
        self.hour_entry.grid(row=0, column=1, padx=2)

        tk.Label(input_frame, text="MM :", font=("Helvetica", 12, "bold"), fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=2, padx=2)
        self.min_entry = tk.Entry(input_frame, width=3, font=("Helvetica", 14), justify="center")
        self.min_entry.insert(0, "00")
        self.min_entry.grid(row=0, column=3, padx=2)

        tk.Label(input_frame, text="SS", font=("Helvetica", 12, "bold"), fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=4, padx=2)
        self.sec_entry = tk.Entry(input_frame, width=3, font=("Helvetica", 14), justify="center")
        self.sec_entry.insert(0, "00")
        self.sec_entry.grid(row=0, column=5, padx=2)

        # Control Button
        self.btn_control = tk.Button(self.root, text="Set Alarm", font=("Helvetica", 12, "bold"), 
                                     bg="#2ecc71", fg="white", width=15, command=self.toggle_alarm)
        self.btn_control.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="No Alarm Set", font=("Helvetica", 11, "italic"), fg="#bdc3c7", bg="#2c3e50")
        self.status_label.pack(pady=5)

    def toggle_alarm(self):
        if not self.alarm_active and not self.is_ringing:
            # Set the Alarm
            try:
                h = int(self.hour_entry.get())
                m = int(self.min_entry.get())
                s = int(self.sec_entry.get())
                
                if 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60:
                    self.alarm_time = f"{h:02d}:{m:02d}:{s:02d}"
                    self.alarm_active = True
                    self.status_label.config(text=f"Alarm set for {self.alarm_time}", fg="#2ecc71")
                    self.btn_control.config(text="Cancel Alarm", bg="#e74c3c")
                else:
                    self.status_label.config(text="Invalid time ranges!", fg="#e74c3c")
            except ValueError:
                self.status_label.config(text="Please enter numbers!", fg="#e74c3c")
        else:
            # Cancel / Stop the Alarm
            self.alarm_active = False
            self.is_ringing = False
            self.alarm_time = None
            self.root.configure(bg="#2c3e50")
            self.canvas.configure(bg="#2c3e50")
            self.status_label.config(text="Alarm Off", fg="#bdc3c7")
            self.btn_control.config(text="Set Alarm", bg="#2ecc71")

    def trigger_alarm(self):
        self.is_ringing = True
        self.alarm_active = False
        self.status_label.config(text="🚨 WAKE UP!!! 🚨", fg="#e74c3c")
        self.btn_control.config(text="Stop Alarm", bg="#e74c3c")
        self.flash_screen()

    def flash_screen(self):
        if self.is_ringing:
            # Alternate colors for standard visual alert flashing
            current_color = self.root.cget("bg")
            next_color = "#e74c3c" if current_color == "#2c3e50" else "#2c3e50"
            
            self.root.configure(bg=next_color)
            self.canvas.configure(bg=next_color)
            
            # Cross-platform internal system speaker beep 
            if os.name == 'nt':
                import winsound
                winsound.Beep(1000, 200)
            else:
                print('\a', end='', flush=True)

            self.root.after(400, self.flash_screen)

    def update_clock(self):
        now = datetime.now()
        
        # Redraw the UI canvas elements
        self.draw_clock_components(now)

        # Check Alarm Condition
        current_time_str = now.strftime("%H:%M:%S")
        if self.alarm_active and current_time_str == self.alarm_time:
            self.trigger_alarm()

        # Force iteration loop every 200ms for accurate secondhand sweeping
        self.root.after(200, self.update_clock)

if __name__ == "__main__":
    main_window = tk.Tk()
    app = AnalogAlarmClock(main_window)
    main_window.mainloop()
