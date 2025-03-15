#!/usr/bin/env python3
import sys
import os
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """
    Main entry point for the IlluminAI Document Reader application.
    """
    # Enable high DPI scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("IlluminAI")
    app.setOrganizationName("IlluminAI")

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
