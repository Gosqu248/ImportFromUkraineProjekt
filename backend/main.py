import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sum_prediction
import sum_data
import fav_item_data  # Importuj plik fav_item_data
from backend import xd, fav_items_all_year, xd2


def on_actual_data_button_click():
    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()
    fig = sum_data.plot_year_values()  # Ensure this function returns a figure
    if fig is not None:  # Only create a new canvas if a figure was returned
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_button_click():

    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()
    fig = sum_prediction.plot_year_values_with_forecast(trend=12, months_prediction=60)  # Ensure this function returns a figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def on_top_items_button_click():
    year = int(select_year.get())

    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()
    fig = fav_item_data.plot_top_items(year=year)  # Wywołanie plot_top_items z fav_item_data
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_top_items_predictions_button_click():

    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()
    fig = fav_items_all_year.plot_top_items_with_year()  # Wywołanie plot_top_items z fav_item_data
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

selected_end_year = tk.StringVar(root)
selected_end_year.set("2026")

options_end_year = ["2024", "2025", "2026", "2027", "2028", "2029", "2030"]

# Dodanie rozwijanego menu wyboru dla roku końcowego
option_end_year_menu = tk.OptionMenu(root, selected_end_year, *options_end_year)
option_end_year_menu.pack(pady=10)

# Dodanie przycisku
button = tk.Button(root, text="Predict", command=on_button_click)
button.pack(pady=10)


options_year = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]

select_year = tk.StringVar(root)
select_year.set("2020")

# Dodanie rozwijanego menu wyboru
option_year_menu = tk.OptionMenu(root, select_year, *options_year)
option_year_menu.pack(pady=10)

top_items_button = tk.Button(root, text="Show top 5 items", command=on_top_items_button_click)  # Dodanie przycisku
top_items_button.pack(pady=10)



selected_end_year_top = tk.StringVar(root)
selected_end_year_top.set("2026")

options_end_year = ["2024", "2025", "2026", "2027", "2028", "2029", "2030"]

# Dodanie rozwijanego menu wyboru dla roku końcowego
option_end_year_menu = tk.OptionMenu(root, selected_end_year_top, *options_end_year)
option_end_year_menu.pack(pady=10)


# Dodanie przycisku
button = tk.Button(root, text="Show top items from all year", command=on_top_items_predictions_button_click)
button.pack(pady=10)


# Uruchomienie pętli głównej
root.mainloop()
