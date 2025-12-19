#!/usr/bin/env python3
"""Управление ARQ сайтом"""
import sys
import os

# Настраиваем пути
prj_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, prj_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        print("Commands: test, admin, runserver, initdb")
        return
    
    command = sys.argv[1]
    
    if command == "test":
        import pytest
        pytest.main(["-v", "tests/"])
    elif command == "admin":
        from scripts.admin_manager import main as admin_main
        admin_main()
    elif command == "runserver":
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    elif command == "initdb":
        from scripts.init_db import create_test_data
        create_test_data()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
