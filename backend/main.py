import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure

import sum_prediction
import sum_data
import fav_item_data
from backend import fav_items_all_year, fav_item_predictions
import ware_sum_prediction

# Actual data button click
def on_actual_data_button_click():
    fig = sum_data.plot_year_values()
    if fig is not None:
        canvas = FigureCanvasTkAgg(fig, master=root)
        fig.tight_layout()
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")


# Prediction button click
def on_button_click():
    trend = int(selected_trend.get())
    months_prediction = int(selected_months_number.get())

    if trend > 50:
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
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")

# Add your list of names here
names = ['Meble do siedzenia (inne niż te objęte pozycją 872.4), nawet przekształcalne w miejsca do spania, i ich części', 'Artykuły z masy papierniczej, papieru lub tektury lub waty celulozowej, gdzie indziej niewymienione ani niewłączone', 'Olej z nasion słonecznika lub z krokosza balwierskiego i ich frakcje', 'Nasiona rzepaku, rzepiku lub gorczycy', 'Olej sojowy i jego frakcje', 'Kukurydza (z wyłączeniem kukurydzy cukrowej), niezmielona, inna niż nasiona', 'Owoce i orzechy, niegotowane lub gotowane na parze, lub w wodzie, zamrożone, nawet zawierające dodatek cukru lub innej substancji słodzącej', 'Energia elektryczna', 'Drewno utwardzone i płyta wiórowa, płyta o wiórach zorientowanych oriented strand board (OSB) itp. płyty, z drewna lub pozostałych zdrewniałych materiałów', 'Rudy i koncentraty żelaza, nieaglomerowane', 'Wyroby walcowane płaskie z żeliwa lub stali niestopowej, nieplaterowane, niepokryte ani niepowleczone, nieobrobione więcej niż walcowane na gorąco', 'Makuchy i in. pozostałości stałe (bez osadów), nawet zmielone lub w granulk., z ekstrakcji tłuszczów lub olejów z nasion lub owoców oleistych i zarodków zbóż', 'Olej z nasion słonecznika lub z krokosza balwierskiego i ich frakcje', 'Nasiona rzepaku, rzepiku lub gorczycy', 'Półprodukty z żeliwa lub stali niestopowej, zawierające mniej niż 0,25\xa0% masy węgla', 'Pozostałe żelazostopy (z wyłączeniem żelazostopów radioaktywnych)', 'Drut izol., kable itp. izol. przew. el., nawet wypos. w złączki; przew. z włók. opt., z osłoniętych włók., nawet poł. z przewod. prądu el. l. wypos. w złączki', 'Rudy żelaza aglomerowane (spieki, granulki, brykiety, itp.)', 'Materiały pochodzenia roślinnego, gdzie indziej niewymienione ani niewłączone', 'Wyroby walcowane płaskie z żeliwa lub stali niestopowej, powleczone lub pokryte cynkiem', 'Wyroby walcowane płaskie z żeliwa lub stali niestopowej, nieplaterowane, niepokryte ani niepowleczone, nieobrobione więcej niż walcowane na zimno', 'Wyroby stolarskie i ciesielskie dla budownictwa, z drewna, włącznie z drewnianymi płytami komórkowymi, połączone płyty parkietowe, dachówki i gonty', 'Pozostałe rury, przewody rurowe i profile drążone, z żeliwa lub stali (na przykład z otwartym szwem lub spawane, nitowane lub zamykane w podobny sposób)', 'Meble do siedzenia (inne niż te objęte pozycją 872.4), nawet przekształcalne w miejsca do spania, i ich części', 'Sztaby i pręty, walcowane na gorąco, w nieregularnie zwijanych kręgach, z żeliwa lub stali', 'Węglowodory alifatyczne', 'Drewno z d. liściast. z poz. 247.5, przetarte l. strugane wzdłużnie, skrawane warstwami l. okorowane, też strug., szlifow. l. łączone stykowo, o grubości > 6 mm', 'Arkusze na forniry, na sklejkę l. itp. drewno warstw. i inne, przetarte wzdł., skraw. warstw. l. okorow., też strugane, szlifowane, łączone, o grub. <= 6 mm', 'Artykuły z masy papierniczej, papieru lub tektury lub waty celulozowej, gdzie indziej niewymienione ani niewłączone', 'Drewno opałowe (z wyłączeniem odpadów drewnianych) i węgiel drzewny', 'Węgiel (włącznie z sadzą), gdzie indziej niewymieniony ani niewłączony', 'Substancje białkowe, skrobie modyfikowane i kleje', 'Miód naturalny', 'Sok z dowolnego pojedynczego owocu (innego niż owoce cytrusowe) lub warzywa; mieszanki soków owocowych lub warzywnych']

def on_ware_sum_prediction_button(year=2010):

    global start_year
    start_year = 2010

    name = selected_name.get()
    trend = int(selected_trend2.get())
    months_prediction = int(selected_months_number2.get())

    if trend > 50:
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

    fig = ware_sum_prediction.plot_year_values_with_forecast(name, trend=trend, months_prediction=months_prediction, start_year=year)
    canvas = FigureCanvasTkAgg(fig, master=root)
    fig.tight_layout()
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")




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
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")


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
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")

def on_top_items_all_time_button_click():
    fig = fav_items_all_year.plot_top_items_with_year()
    canvas = FigureCanvasTkAgg(fig, master=root)
    fig.tight_layout()
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")

# Validate input
def validate_input(input):
    if input.isdigit():
        return True
    elif input == "":
        return True
    else:
        return False


def change_start_year():
    global start_year
    if start_year == 2020:
        start_year = 2010
    else:
        start_year = 2020
    on_ware_sum_prediction_button(year=start_year)

# App window settings
root = tk.Tk()
root.title("Prediction app")
root.geometry("1200x1000")
root.configure(bg='#2b2d30')
validate_command = root.register(validate_input)

frame1 = tk.Frame(root, bd=2, relief="groove", bg='#2b2d30')
frame2 = tk.Frame(root, bd=2, relief="groove", bg='#2b2d30')
frame3 = tk.Frame(root, bd=2, relief="groove", bg='#2b2d30')
frame4 = tk.Frame(root, bd=2, relief="groove", bg='#2b2d30')
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
frame4.grid(row=0, column=2, sticky="nsew")
frame3.grid(row=0, column=3, sticky="nsew")

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

label = tk.Label(frame4, text="Choose name and prediction settings!", bg='#2b2d30', fg='white', font=('Arial', 18))
label.pack(pady=10)

label = tk.Label(frame4, text="Name", bg='#2b2d30', fg='white', font=('Arial', 10))
label.pack()
selected_name = ttk.Combobox(frame4, values=names)
selected_name.pack(pady=10)

label = tk.Label(frame4, text="Number of months for prediction", bg='#2b2d30', fg='white', font=('Arial', 10))
label.pack()
selected_months_number2 = tk.Entry(frame4, validate="key", validatecommand=(validate_command, '%P'),)
selected_months_number2.pack(pady=10)

label = tk.Label(frame4, text="Number of months in trend for prediction", bg='#2b2d30', fg='white', font=('Arial', 10))
label.pack()
selected_trend2 = tk.Entry(frame4, validate="key", validatecommand=(validate_command, '%P'))
selected_trend2.pack(pady=10)

button = tk.Button(frame4, text="Predict", command=on_ware_sum_prediction_button, bg='#afb1b3', font=('Arial', 10, 'bold'))
button.pack(pady=10)

change_start_year_button = tk.Button(frame4, text="Change start_year", command=change_start_year, bg='#afb1b3', font=('Arial', 10, 'bold'))
change_start_year_button.pack(pady=10)


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
canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")
fig = figure(facecolor='#2b2d30')
canvas = FigureCanvasTkAgg(fig, master=root)
fig.tight_layout()
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=15)

root.mainloop()
