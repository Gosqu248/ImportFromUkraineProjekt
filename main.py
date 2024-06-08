import tkinter as tk
from tkinter import messagebox
import backend.sum_prediction


# Funkcja wywoływana po naciśnięciu przycisku
def on_button_click():
    backend.prediction.plot_predictions(2026, 'Linear')

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Predictions App")
root.geometry("800x800")

# Dodanie etykiety
label = tk.Label(root, text="Witaj w mojej aplikacji!")
label.pack(pady=10)

# Dodanie przycisku
button = tk.Button(root, text="Kliknij mnie", command=on_button_click)
button.pack(pady=10)

# Uruchomienie pętli głównej
root.mainloop()
