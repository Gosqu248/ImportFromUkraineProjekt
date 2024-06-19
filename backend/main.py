import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure

import sum_prediction
import sum_data
import fav_item_data
from backend import fav_items_all_year, fav_item_predictions


# Actual data button click
def on_actual_data_button_click():
    fig = sum_data.plot_year_values()
    if fig is not None:
        canvas = FigureCanvasTkAgg(fig, master=root)
        fig.tight_layout()
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky="nsew")


# Prediction button click
def on_button_click():
    trend = int(selected_trend.get())
    months_prediction = int(selected_months_number.get())

    if trend > 30:
        messagebox.showerror("Error", "Trend should be less than 30 due to lack of earlier data for proper prediction")
        return
    elif trend < 2:
        messagebox.showerror("Error", "Trend should be greater than 1 in order to make proper prediction")
        return

    if months_prediction == 0:
        messagebox.showerror("Error", "Months prediction should be greater than 0 in order to make proper prediction")
        return
    elif months_prediction > 120:
        months_prediction = 120

    fig = sum_prediction.plot_year_values_with_forecast(trend=trend, months_prediction=months_prediction)
    canvas = FigureCanvasTkAgg(fig, master=root)
    fig.tight_layout()
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky="nsew")


# Top items button click
def on_top_items_for_year_button_click():
    options_year = [str(year) for year in range(2010, 2024)]

    year = int(selected_year.get())
    if year not in options_year:
        messagebox.showerror("Error", "Year should be in range 2010-2023")
        return

    fig = fav_item_data.plot_top_items(year=year)
    canvas = FigureCanvasTkAgg(fig, master=root)
    fig.tight_layout()
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky="nsew")


# Top items predictions button click
def on_top_items_predictions_button_click():
    options_year = [str(year) for year in range(2024, 2035)]

    year = int(selected_year.get())
    if year not in options_year:
        messagebox.showerror("Error", "Year should be in range 2024-2034 i order to make prediction")
        return
    fig = fav_item_predictions.plot_top_items_with_year(selected_year=year)
    canvas = FigureCanvasTkAgg(fig, master=root)
    fig.tight_layout()
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_top_items_all_time_button_click():
    fig = fav_items_all_year.plot_top_items_with_year()
    canvas = FigureCanvasTkAgg(fig, master=root)
    fig.tight_layout()
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky="nsew")

# Validate input
def validate_input(input):
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False


# App window settings
root = tk.Tk()
root.title("Prediction app")
root.geometry("1200x1000")
root.configure(bg='#2b2d30')
validate_command = root.register(validate_input)

frame1 = tk.Frame(root, bd=2, relief="groove", bg='#2b2d30')
frame2 = tk.Frame(root, bd=2, relief="groove", bg='#2b2d30')
frame3 = tk.Frame(root, bd=2, relief="groove", bg='#2b2d30')
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
frame3.grid(row=0, column=2, sticky="nsew")


# Actual data button
label = tk.Label(frame1, text="Show real data", bg='#2b2d30', fg='white', font=('Arial', 18))
label.pack(pady=10)
actual_data_button = tk.Button(frame1, text="Show", command=on_actual_data_button_click, bg='#afb1b3', font=('Arial', 10, 'bold'))
actual_data_button.place(relx=0.5, rely=0.5, anchor='center')

# Prediction settings
label = tk.Label(frame2, text="Choose prediction settings!", bg='#2b2d30', fg='white', font=('Arial', 18))
label.pack(pady=10)

label = tk.Label(frame2, text="Number of months for prediction", bg='#2b2d30', fg='white', font=('Arial', 10))
label.pack()
selected_months_number = tk.Entry(frame2, validate="key", validatecommand=(validate_command, '%P'),)
selected_months_number.pack(pady=10)

label = tk.Label(frame2, text="Number of months in trend for prediction", bg='#2b2d30', fg='white', font=('Arial', 10))
label.pack()
selected_trend = tk.Entry(frame2, validate="key", validatecommand=(validate_command, '%P'))
selected_trend.pack(pady=10)

button = tk.Button(frame2, text="Predict", command=on_button_click, bg='#afb1b3', font=('Arial', 10, 'bold'))
button.pack(pady=10)

# Top items prediction settings
label = tk.Label(frame3, text="Choose year to show top 5 items", bg='#2b2d30', fg='white', font=('Arial', 18))
label.pack(pady=10)

selected_year = tk.Entry(frame3, validate="key", validatecommand=(validate_command, '%P'))
selected_year.pack(pady=10)


button_frame = tk.Frame(frame3, bg='#2b2d30')
button_frame.pack()

top_items_button = tk.Button(button_frame, text="Show real for year", command=on_top_items_for_year_button_click, bg='#afb1b3', font=('Arial', 10, 'bold'))
top_items_button.grid(row=0, column=0, padx=10)

button2 = tk.Button(button_frame, text="Show prediction for year", command=on_top_items_predictions_button_click, bg='#afb1b3', font=('Arial', 10, 'bold'))
button2.grid(row=0, column=1, padx=10)

button3 = tk.Button(button_frame, text="Show all time data", command=on_top_items_all_time_button_click, bg='#afb1b3', font=('Arial', 10, 'bold'))
button3.grid(row=0, column=2, padx=10)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

# Graph with top items predictions
canvas = tk.Canvas(root)
canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
fig = figure(facecolor='#2b2d30')
canvas = FigureCanvasTkAgg(fig, master=root)
fig.tight_layout()
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky="nsew")

#
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=15)

root.mainloop()
