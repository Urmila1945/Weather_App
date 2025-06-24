
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
from weather_fetcher import fetch_weather_data, get_icon, fetch_5_day_forecast, fetch_hourly_forecast
from gps_locator import detect_location
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import os
import datetime

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌤️ Advanced Weather App")
        self.theme = "light"
        self.recent_cities = []
        self.refresh_interval_map = {
            "1 min": 60000,
            "5 min": 300000,
            "10 min": 600000
        }
        self.selected_interval = tk.StringVar(value="5 min")


        win_width, win_height = 400, 650
        x = (root.winfo_screenwidth() // 2) - (win_width // 2)
        y = (root.winfo_screenheight() // 2) - (win_height // 2)
        root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        root.configure(bg="#e0f7fa")

        self.canvas = tk.Canvas(root, bg="#e0f7fa", borderwidth=0, highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="#e0f7fa")
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        v_scroll = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        h_scroll = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mousewheel)

        self.content_frame = tk.Frame(self.scroll_frame, bg="#e0f7fa")
        self.content_frame.pack(anchor="center", pady=10)

        self.build_ui()
        self.city_entry.bind("<Return>", lambda event: self.get_weather())
        
        self.zip_entry = tk.Entry(root, font=("Helvetica", 12), width=35, bd=3, relief="groove", justify="center")
        self.zip_entry.insert(0, "Enter ZIP/Pin Code (optional)")
        self.zip_entry.pack(pady=4)


    # In your get_weather() function:
# Add this line after setting the result_label:
# self.result_label.config(text=..., justify="center")
# tk.Label(root, text=f"Last Updated: {get_current_time()}", font=("Helvetica", 10), bg="#e0f7fa").pack()

# --------------- 2. Animated Weather Icons (optional GIF support) ---------------
    def get_icon(icon_code, animated=False):
        path = f"icons/{icon_code}.gif" if animated else f"icons/{icon_code}.png"
        return path if os.path.exists(path) else "icons/default.png"

# Use with:
# icon_path = get_icon(data["icon"], animated=True)

# --------------- 3. Error Logging ---------------
    def log_error(message):
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"[{get_current_time()}] {message}\n")

# Usage:
# try: ... except Exception as e: log_error(str(e))

# --------------- 4. Settings Persistence ---------------
    SETTINGS_FILE = "settings.json"

    def load_settings():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_settings(settings):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)

# Use load_settings() on startup, and save_settings({...}) before exit.

# --------------- 5. Offline Mode ---------------
    CACHE_FILE = "weather_cache.json"

    def cache_weather_data(data):
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)

    def load_cached_weather():
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return None

# If API fails, use:
# cached = load_cached_weather()
# if cached: display(cached)

# --------------- 6. Multi-language Support (basic) ---------------
    translations = {
    "en": {"Temp": "Temperature", "Humidity": "Humidity"},
    "hi": {"Temp": "तापमान", "Humidity": "नमी"},
    "mr": {"Temp": "तापमान", "Humidity": "आर्द्रता"}
    }

    current_lang = "en"

    def t(label):
        return translations[current_lang].get(label, label)

# Use like: tk.Label(..., text=t("Temp"))

# --------------- 7. Accessibility: High Contrast / Large Text ---------------
    def apply_accessibility(mode="normal"):
        if mode == "high_contrast":
            bg = "black"; fg = "yellow"; font = ("Arial", 14, "bold")
        else:
            bg = "#e0f7fa"; fg = "#006064"; font = ("Helvetica", 12)
        return bg, fg, font

# Call this on a toggle event and apply to all widgets.

# --------------- 8. Weather Alerts (API-based) ---------------
    def fetch_weather_alerts(city):
    # Requires One Call API subscription (or similar)
    # Placeholder for illustration
        try:
        # You would need lat/lon from weather API
            return ["Heavy Rain Warning"]
        except:
            return []

# Show via messagebox if alerts:
# for alert in alerts: messagebox.showwarning("Alert", alert)

# --------------- 9. Sunrise & Sunset Time ---------------
# Already in fetch_weather_data() as:
# datetime.fromtimestamp(data['sys']['sunrise']).strftime("%I:%M %p")

# --------------- 10. Feels Like Temperature ---------------
# Also from data['main']['feels_like']
# Show as: "Feels Like: {feels_like}°"

# --------------- 11. Weather by Zip Code ---------------
    def fetch_weather_by_zip(zip_code, country_code="in", unit="metric"):
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={API_KEY}&units={unit}"
    # Rest similar to fetch_weather_data()

# --------------- 12. Wind Direction Compass ---------------
    def get_wind_direction(degree):
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        idx = int((degree + 22.5) / 45) % 8
        return directions[idx]

     
       

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            bg_color = "#070707"
            fg_color = "white"
            button_bg = "#030608"
            entry_bg = "#455A64"
        else:
            self.theme = "light"
            bg_color = "#e0f7fa"
            fg_color = "#006064"
            button_bg = "#26c6da"
            entry_bg = "white"

        self.root.configure(bg=bg_color)
        self.canvas.configure(bg=bg_color)
        self.scroll_frame.configure(bg=bg_color)
        self.content_frame.configure(bg=bg_color)

        for widget in self.content_frame.winfo_children():
            if isinstance(widget, (tk.Label, tk.Frame)):
                widget.configure(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Button):
                widget.configure(bg=button_bg, fg="white")
            elif isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
                widget.configure(background=entry_bg)

        for child in self.forecast_frame.winfo_children():
            child.configure(bg=bg_color)
            for sub in child.winfo_children():
                sub.configure(bg=bg_color, fg=fg_color)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def build_ui(self):
        root = self.content_frame

        tk.Label(root, text="🌦 Weather Forecast", font=("Helvetica", 20, "bold"),
                 bg="#e0f7fa", fg="#006064").pack(pady=10)

        self.city_entry = tk.Entry(root, font=("Helvetica", 14), width=35, bd=3, relief="groove", justify="center")
        self.city_entry.insert(0, "Enter city name or click Detect")
        self.city_entry.pack(pady=5)
        
        # 🔽 Add this line:
        self.city_entry.bind("<Return>", lambda event: self.get_weather())

        self.recent_combo = ttk.Combobox(root, values=self.recent_cities, font=("Helvetica", 11))
        self.recent_combo.pack(pady=2)
        self.recent_combo.bind("<<ComboboxSelected>>", self.select_recent)

        self.unit_var = tk.StringVar(value="metric")
        unit_frame = tk.Frame(root, bg="#e0f7fa")
        unit_frame.pack()
        tk.Radiobutton(unit_frame, text="Celsius", variable=self.unit_var, value="metric", bg="#e0f7fa").pack(side=tk.LEFT)
        tk.Radiobutton(unit_frame, text="Fahrenheit", variable=self.unit_var, value="imperial", bg="#e0f7fa").pack(side=tk.LEFT)

        tk.Button(root, text="📍 Detect Location", font=("Helvetica", 11), command=self.detect_location,
                  bg="#26c6da", fg="white", padx=10, pady=5).pack(pady=6)

        tk.Button(root, text="🔍 Get Weather", font=("Helvetica", 12, "bold"), command=self.get_weather,
                  bg="#00796b", fg="white", padx=10, pady=6).pack(pady=6)

        self.icon_label = tk.Label(root, bg="#e0f7fa")
        self.icon_label.pack(pady=8)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 12), justify="center", bg="#e0f7fa")
        self.result_label.pack(pady=10)

        tk.Label(root, text="🗓 5-Day Forecast", font=("Helvetica", 14, "bold"), bg="#e0f7fa", fg="#006064").pack(pady=5)

        self.forecast_frame = tk.Frame(root, bg="#e0f7fa")
        self.forecast_frame.pack()

        self.chart_button = tk.Button(root, text="📈 Show Chart", font=("Helvetica", 11),
                                      command=self.show_chart_popup,
                                      bg="#004d40", fg="white", padx=8, pady=4)
        self.chart_button.pack(pady=5)

        self.save_chart_button = tk.Button(root, text="📸 Export Chart", font=("Helvetica", 11),
                                           command=self.export_chart_image,
                                           bg="#455a64", fg="white", padx=8, pady=4)
        self.save_chart_button.pack(pady=5)

        self.hourly_button = tk.Button(root, text="🕒 Hourly Forecast", font=("Helvetica", 11),
                                       command=self.show_hourly_forecast,
                                       bg="#5c6bc0", fg="white", padx=8, pady=4)
        self.hourly_button.pack(pady=5)

        self.save_button = tk.Button(root, text="💾 Save Report", font=("Helvetica", 11),
                                     command=self.save_report,
                                     bg="#455a64", fg="white", padx=8, pady=4)
        self.save_button.pack(pady=5)

        self.theme_button = tk.Button(root, text="🌓 Toggle Theme", font=("Helvetica", 11),
                                      command=self.toggle_theme,
                                      bg="#757575", fg="white", padx=8, pady=4)
        self.theme_button.pack(pady=8)
# Auto-refresh toggle
        self.auto_refresh_var = tk.BooleanVar()
        self.auto_refresh_checkbox = tk.Checkbutton(
        root,
        text="🔄 Auto Refresh (2 mins)",
        variable=self.auto_refresh_var,
        bg="#e0f7fa",
        command=self.toggle_auto_refresh
    )
        self.auto_refresh_checkbox.pack(pady=5)

    def toggle_auto_refresh(self):
        if self.auto_refresh_var.get():
            self.schedule_auto_refresh()
        else:
            if hasattr(self, "refresh_after_id"):
                self.root.after_cancel(self.refresh_after_id)
                
    def schedule_auto_refresh(self):
        self.get_weather()
        interval = self.refresh_interval_map.get(self.selected_interval.get(), 300000)
        self.refresh_after_id = self.root.after(interval, self.schedule_auto_refresh)

    def select_recent(self, event):
        selected_city = self.recent_combo.get()
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, selected_city)
        

    # ... your toggle_theme, mousewheel handlers, and build_ui remain unchanged

    def get_weather(self):
      
        zip_code = self.zip_entry.get().strip()
        city = self.city_entry.get().strip()
        unit = self.unit_var.get()

        if zip_code.isdigit():
            data = fetch_weather_by_zip(zip_code, unit)
        elif city:
            data = fetch_weather_data(city, unit)
        else:
            messagebox.showwarning("Warning", "Enter city or valid PIN code.")
            return

        if not data:
            messagebox.showerror("Error", "Failed to fetch weather data.")
            return
        city = self.city_entry.get().strip()
        unit = self.unit_var.get()

        if not city:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return

        if city not in self.recent_cities:
            self.recent_cities.insert(0, city)
            self.recent_combo["values"] = self.recent_cities[:10]

        data = fetch_weather_data(city, unit)
        if data:
            icon_path = get_icon(data["icon"])
            icon_img = ImageTk.PhotoImage(Image.open(icon_path).resize((100, 100)))
            self.icon_label.config(image=icon_img)
            self.icon_label.image = icon_img

            self.result_label.config(
                text=(
                    f"{data['city']}\n"
                    f"🌡 Temp: {data['temp']}° {'C' if unit == 'metric' else 'F'}\n"
                    f"💧 Humidity: {data['humidity']}%\n"
                    f"🌬 Wind: {data['wind']} {'m/s' if unit == 'metric' else 'mph'}\n"
                    f"☁ Condition: {data['desc']}"
                )
            )

            # Weather Alerts (simple version)
            if any(alert in data["desc"].lower() for alert in ["storm", "rain", "heat", "snow", "fog"]):
                messagebox.showwarning("Weather Alert!", f"⚠ {data['desc']} warning in {data['city']}!")

        else:
            messagebox.showerror("Error", "Failed to retrieve weather data.")
            return

        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        forecast_data = fetch_5_day_forecast(city, unit)
        for day in forecast_data:
            icon_path = get_icon(day["icon"])
            icon_img = ImageTk.PhotoImage(Image.open(icon_path).resize((40, 40)))
            frame = tk.Frame(self.forecast_frame, bg="#e0f7fa")
            frame.pack(pady=2)
            tk.Label(frame, text=day["date"], width=12, anchor="w", font=("Helvetica", 10), bg="#e0f7fa").pack(side=tk.LEFT)
            tk.Label(frame, image=icon_img, bg="#e0f7fa").pack(side=tk.LEFT)
            tk.Label(frame, text=f"{day['temp']}°  {day['desc']}", anchor="w", font=("Helvetica", 10), bg="#e0f7fa").pack(side=tk.LEFT)
            frame.image = icon_img
            
            
            # 4. Weather Alerts
            if any(alert in data["desc"].lower() for alert in ["storm", "rain", "heat", "snow"]):
                messagebox.showwarning("Weather Alert!", f"⚠ {data['desc']} warning in {data['city']}!")

            else:
                messagebox.showerror("Error", "Failed to retrieve weather data.")
                return

        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        forecast_data = fetch_5_day_forecast(city, unit)
        for day in forecast_data:
            icon_path = get_icon(day["icon"])
            icon_img = ImageTk.PhotoImage(Image.open(icon_path).resize((40, 40)))
            frame = tk.Frame(self.forecast_frame, bg="#e0f7fa")
            frame.pack(pady=2)
            tk.Label(frame, text=day["date"], width=12, anchor="w", font=("Helvetica", 10), bg="#e0f7fa").pack(side=tk.LEFT)
            tk.Label(frame, image=icon_img, bg="#e0f7fa").pack(side=tk.LEFT)
            tk.Label(frame, text=f"{day['temp']}°  {day['desc']}", anchor="w", font=("Helvetica", 10), bg="#e0f7fa").pack(side=tk.LEFT)
            frame.image = icon_img
            
            
    
    def fetch_weather_data(city, unit="metric"):
        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?q={city}"
                f"&appid={API_KEY}&units={unit}"
            )
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

        # Extract main weather data
            weather = data["weather"][0]
            main = data["main"]
            wind = data["wind"]
            sys = data["sys"]

        # Convert UNIX timestamps to local time strings
            sunrise = datetime.fromtimestamp(sys["sunrise"]).strftime("%I:%M %p")
            sunset = datetime.fromtimestamp(sys["sunset"]).strftime("%I:%M %p")

            return {
                "city": data["name"],
                "temp": round(main["temp"]),
                "humidity": main["humidity"],
                "wind": wind["speed"],
                "desc": weather["description"].title(),
                "icon": weather["icon"],
                "sunrise": sunrise,
                "sunset": sunset
            }
        except Exception as e:
            print("Error fetching weather data:", e)
            return None 

    def detect_location(self):
        city = detect_location()
        if city:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)
        else:
            messagebox.showerror("Error", "Unable to detect location.")

    def show_chart_popup(self):
        city = self.city_entry.get().strip()
        unit = self.unit_var.get()
        forecast_data = fetch_5_day_forecast(city, unit)
        if forecast_data:
            self.show_temperature_chart(forecast_data, unit)
        else:
            messagebox.showerror("Error", "Unable to fetch forecast data.")

    def show_temperature_chart(self, forecast_data, unit):
        self.fig, ax = plt.subplots(figsize=(5, 3.5), dpi=100)
        dates = [d["date"] for d in forecast_data]
        temps = [d["temp"] for d in forecast_data]

        ax.plot(dates, temps, marker="o", linestyle="-", color="#00796b")
        ax.set_title("5-Day Temperature Forecast")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Temperature (°{'C' if unit == 'metric' else 'F'})")
        ax.grid(True)

        self.chart_win = tk.Toplevel(self.root)
        self.chart_win.title("📊 Temperature Trend")
        win_width, win_height = 650, 500
        x = (self.chart_win.winfo_screenwidth() // 2) - (win_width // 2)
        y = (self.chart_win.winfo_screenheight() // 2) - (win_height // 2)
        self.chart_win.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.chart_win.configure(bg="#e0f7fa")

        canvas = FigureCanvasTkAgg(self.fig, master=self.chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(self.fig)

    def export_chart_image(self):
        if hasattr(self, "fig"):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png")],
                title="Save Chart As"
            )
            if file_path:
                self.fig.savefig(file_path)
                messagebox.showinfo("Success", f"Chart saved to:\n{file_path}")
        else:
            messagebox.showwarning("Warning", "Please generate the chart first.")


    def show_hourly_forecast(self):
        city = self.city_entry.get().strip()
        unit = self.unit_var.get()

        if not city:
            messagebox.showwarning("Warning", "Please enter or detect a city first.")
            return

        hourly_data = fetch_hourly_forecast(city, unit)
        if not hourly_data:
            messagebox.showerror("Error", "Failed to fetch hourly forecast.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Hourly Forecast")
        popup_width, popup_height = 600, 400
        x = (popup.winfo_screenwidth() // 2) - (popup_width // 2)
        y = (popup.winfo_screenheight() // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.configure(bg="#e0f7fa")

        canvas = tk.Canvas(popup, bg="#e0f7fa")
        frame = tk.Frame(canvas, bg="#e0f7fa")
        scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for hour in hourly_data:
            time = hour["time"]
            temp = hour["temp"]
            desc = hour["desc"]
            icon = ImageTk.PhotoImage(Image.open(get_icon(hour["icon"])).resize((30, 30)))
            row = tk.Frame(frame, bg="#e0f7fa")
            row.pack(pady=2, fill="x")
            tk.Label(row, text=time, width=10, anchor="w", font=("Helvetica", 10), bg="#e0f7fa").pack(side=tk.LEFT)
            tk.Label(row, image=icon, bg="#e0f7fa").pack(side=tk.LEFT)
            tk.Label(row, text=f"{temp} °{'C' if unit == 'metric' else 'F'} - {desc}", anchor="w",
                     font=("Helvetica", 10), bg="#e0f7fa").pack(side=tk.LEFT)
            row.image = icon

    def save_report(self):
        city = self.city_entry.get().strip()
        unit = self.unit_var.get()
        if not city:
            messagebox.showwarning("Warning", "Please enter or detect a city first.")
            return
        weather_data = fetch_weather_data(city, unit)
        forecast_data = fetch_5_day_forecast(city, unit)
        if not weather_data or not forecast_data:
            messagebox.showerror("Error", "Cannot fetch weather data to save.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("CSV File", "*.csv")],
            title="Save Weather Report As"
        )
        if not file_path:
            return
        try:
            if file_path.endswith(".csv"):
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["City", "Temperature", "Humidity", "Wind", "Condition"])
                    
                    writer.writerow([
                    weather_data['city'],
                    f"{weather_data['temp']}°{'C' if unit == 'metric' else 'F'}",
                    f"{weather_data['humidity']}%",
                    f"{weather_data['wind']} {'m/s' if unit == 'metric' else 'mph'}",
                    weather_data['desc']
                ])

                   
                    writer.writerow([])
                    writer.writerow(["Date", "Temp", "Description"])
                    for day in forecast_data:
                        writer.writerow([day["date"], f"{day['temp']}°", day["desc"]])


            else:
                with open(file_path, mode='w', encoding='utf-8') as file:
                    file.write("📍 Weather Report\n\n")
                    file.write(f"City: {weather_data['city']}\n")
                    file.write(f"Temperature: {weather_data['temp']}° {'C' if unit == 'metric' else 'F'}\n")
                    file.write(f"Humidity: {weather_data['humidity']}%\n")
                    file.write(f"Wind: {weather_data['wind']} {'m/s' if unit == 'metric' else 'mph'}\n")
                    file.write(f"Condition: {weather_data['desc']}\n\n")
                    file.write(f"{day['date']}: {day['temp']}°, {day['desc']}\n")

                    
                    for day in forecast_data:
                        file.write(f"{day['date']}: {day['temp']}°, {day['desc']}\n")

            messagebox.showinfo("Success", f"Report saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)

    def on_closing():
        if hasattr(app, "refresh_after_id"):
            root.after_cancel(app.refresh_after_id)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
