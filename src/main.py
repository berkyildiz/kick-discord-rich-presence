import sys

# Reconfigure stdout for UTF-8 on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from src.gui.app import App

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
