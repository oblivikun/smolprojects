import tkinter as tk

def search():
    coin = e.get()
    l.config(text = f'The entered coin is: {coin}')

root = tk.Tk()
root.title("Cryptocurrency Tracker")

e = tk.Entry(root)
e.pack()

b = tk.Button(root, text = "Search", command = search)
b.pack()

l = tk.Label(root, text = "")
l.pack()

root.mainloop()