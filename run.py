#!/usr/bin/env python3
"""
IlluminAI Document Reader - Run Script

This script is a convenience wrapper to start the application from the project root.
Usage: python run.py [--help] [--version]

Options:
  --help      Show this help message and exit
  --version   Show version information and exit
"""

import os
import sys
import traceback


def show_help():
    """Show help message."""
    print(__doc__)
    sys.exit(0)


def show_version():
    """Show version information."""
    print("IlluminAI Document Reader v0.1.0")
    print("An open-source document reader with AI-powered interaction.")
    print("MIT License - Copyright (c) 2023 IlluminAI Contributors")
    sys.exit(0)


def main():
    """Run the IlluminAI Document Reader application."""
    # Process command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            show_help()
        elif sys.argv[1] in ["--version", "-v"]:
            show_version()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            show_help()

    # Add src directory to path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.insert(0, src_path)

    try:
        # Import and run the main function
        from src.main import main
        main()
    except ImportError as e:
        print("\nError: Could not import required modules.")
        print(f"Details: {e}")
        print("\nPlease ensure you have installed all dependencies:")
        print("    pip install -r requirements.txt\n")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print("\nError: An unexpected error occurred while starting the application.")
        print(f"Details: {e}")
        print("\nPlease check the troubleshooting section in the README.md file.")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
