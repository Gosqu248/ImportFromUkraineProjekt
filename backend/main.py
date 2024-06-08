import tkinter as tk
from tkinter import messagebox
import prediction

def on_button_click():
    method = selected_method.get()
    year = int(selected_end_year.get())
    prediction.plot_predictions(2026, method)

root = tk.Tk()
root.title("Prediction app")
root.geometry("800x800")

label = tk.Label(root, text="Wybierz metode predykcji!")
label.pack(pady=10)

selected_method = tk.StringVar(root)
selected_method.set("Linear")

# Lista opcji do wyboru
options_method = ["DecisionTree", "RandomForest", "KNeighbors", "Linear"]

selected_end_year = tk.StringVar(root)
selected_end_year.set("2026")

options_end_year = ["2023", "2024", "2025", "2026"]

# Dodanie rozwijanego menu wyboru
option_method_menu = tk.OptionMenu(root, selected_method, *options_method)
option_method_menu.pack(pady=10)

option_year_menu = tk.OptionMenu(root, selected_end_year, *options_end_year)
option_year_menu.pack(pady=10)

# Dodanie przycisku
button = tk.Button(root, text="Predict", command=on_button_click)
button.pack(pady=10)

# Uruchomienie pętli głównej
root.mainloop()
