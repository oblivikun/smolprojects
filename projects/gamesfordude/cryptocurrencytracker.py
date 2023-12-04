import requests
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import ticker

def get_crypto_price(coin):
    response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd')
    data = json.loads(response.text)
    return data[coin]['usd']

def get_historical_data(coin):
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=365')
    data = json.loads(response.text)
    dates = [datetime.fromtimestamp(x[0]/1000) for x in data['prices'][::24]]
    prices = [x[1] for x in data['prices'][::24]]
    return dates, prices

def plot_data(dates, prices):
    ax.clear()
    ax.plot(dates, prices)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(6))
    canvas.draw()

def search():
    coin = e.get()
    try:
        price = get_crypto_price(coin)
        dates, prices = get_historical_data(coin)
        plot_data(dates, prices)
        increase_day = ((prices[-1] - prices[-2]) / prices[-2]) * 100 if len(prices) > 2 else 0
        increase_month = ((prices[-1] - prices[-30]) / prices[-30]) * 100 if len(prices) > 30 else 0
        increase_year = ((prices[-1] - prices[0]) / prices[0]) * 100 if len(prices) > 0 else 0
        l.config(text = f'The current price of {coin} is: ${price}\n'
                        f'The price increase over the last day is: {increase_day:.2f}%\n'
                        f'The price increase over the last month is: {increase_month:.2f}%\n'
                        f'The price increase over the last year is: {increase_year:.2f}%')
    except KeyError:
        messagebox.showerror("Error", "Invalid cryptocurrency id")
    finally:
        b.config(state="normal")


def start_search():
    b.config(state="disabled")
    threading.Thread(target=search).start()

root = tk.Tk()
root.title("Cryptocurrency Tracker")

e = tk.Entry(root)
e.pack()

b = tk.Button(root, text = "Search", command = start_search)
b.pack()

l = tk.Label(root, text = "")
l.pack()

fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()