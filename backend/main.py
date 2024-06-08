import tkinter as tk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import prediction
import plot_data

def on_button_click():
    method = selected_method.get()
    year = int(selected_end_year.get())

    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()
    fig = prediction.plot_predictions(end_year=year, model_type=method)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_actual_data_button_click():
    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()
    fig = plot_data.plot_year_values()  # Ensure this function returns a figure
    if fig is not None:  # Only create a new canvas if a figure was returned
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root = tk.Tk()
root.title("Prediction app")
root.geometry("800x800")

actual_data_button = tk.Button(root, text="Show Actual Data", command=on_actual_data_button_click)
actual_data_button.pack(pady=10)

label = tk.Label(root, text="Wybierz metode predykcji!")
label.pack(pady=10)

selected_method = tk.StringVar(root)
selected_method.set("Linear")

# Lista opcji do wyboru
options_method = ["DecisionTree", "RandomForest", "KNeighbors", "Linear"]

selected_end_year = tk.StringVar(root)
selected_end_year.set("2026")

options_end_year = [ "2024", "2025", "2026", "2027", "2028", "2029", "2030"]

# Dodanie rozwijanego menu wyboru
option_method_menu = tk.OptionMenu(root, selected_method, *options_method)
option_method_menu.pack(pady=10)

option_year_menu = tk.OptionMenu(root, selected_end_year, *options_end_year)
option_year_menu.pack(pady=10)

# Dodanie przycisku
button = tk.Button(root, text="Predict", command=on_button_click)
button.pack(pady=10)

# Add button for displaying actual data


# Uruchomienie pętli głównej
root.mainloop()