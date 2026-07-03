import tkinter as tk
from tkinter import ttk
from config import APP_NAME

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("420x260")
        self.resizable(False, False)
        ttk.Label(self, text=APP_NAME, font=("Segoe UI", 18, "bold")).pack(pady=16)
        frame = ttk.Frame(self)
        frame.pack(pady=8)
        ttk.Label(frame, text="City:").grid(row=0, column=0, padx=6, pady=6)
        self.city = ttk.Entry(frame, width=28)
        self.city.grid(row=0, column=1, padx=6, pady=6)
        self.city.insert(0, "Melbourne")
        ttk.Button(self, text="Check Weather", command=self.check_weather).pack(pady=10)
        self.output = ttk.Label(self, text="Enter a city and click Check Weather.", wraplength=360)
        self.output.pack(pady=10)

    def check_weather(self):
        city = self.city.get().strip() or "your city"
        self.output.config(text=f"Weather lookup scaffold for {city}. Add an API provider next.")

if __name__ == "__main__":
    WeatherApp().mainloop()
