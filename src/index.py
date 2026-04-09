from tkinter import Tk
from src.ui.ui import UI

def main():
    window = Tk()
    window.title("The Budget App")
    ui = UI(window)
    ui.start()
    window.mainloop()

if __name__ == "__main__":
    main()
