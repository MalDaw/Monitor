import tkinter as tk

root = tk.Tk()
root.geometry("300x200")
root.title("Test okna")
label = tk.Label(root, text="Jeśli to widzisz, tkinter działa!")
label.pack()
root.mainloop()