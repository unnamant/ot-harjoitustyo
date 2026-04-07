from tkinter import Tk
from src.ui.ui import UI

def main():
    window = Tk()
    window.title("Budget-app")
    ui = UI(window)
    ui.start()
    window.mainloop()

if __name__ == "__main__":
    main()