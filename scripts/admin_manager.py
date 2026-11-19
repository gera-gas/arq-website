#!/usr/bin/env python3
"""ARQ Admin Manager Utility"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import AdminUser
from app.auth import get_password_hash, verify_password
from getpass import getpass

def display_menu():
    """Отображает меню"""
    print("\n" + "=" * 40)
    print("👑 ARQ Admin Manager")
    print("=" * 40)
    print("1. 📋 List administrators")
    print("2. ➕ Add administrator")
    print("3. ❌ Delete administrator")
    print("4. ✏️  Change password")
    print("5. 🔍 Verify password")
    print("6. 🚪 Exit")
    print("-" * 40)

def list_admins(db):
    """Выводит список всех администраторов"""
    admins = db.query(AdminUser).order_by(AdminUser.created_at).all()
    
    if not admins:
        print("📭 No administrators in database")
        return []
    
    print(f"\n📋 Found {len(admins)} administrator(s):")
    print("-" * 60)
    print(f"{'#':<3} {'ID':<5} {'Username':<20} {'Created at':<25}")
    print("-" * 60)
    
    for idx, admin in enumerate(admins, 1):
        print(f"{idx:<3} {admin.id:<5} {admin.username:<20} {admin.created_at:<25}")
    
    return admins

def create_admin(db):
    """Создаёт нового администратора"""
    print("\n➕ Create new administrator")
    print("-" * 30)
    
    username = input("Username: ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return
    
    # Проверяем, существует ли уже
    existing = db.query(AdminUser).filter_by(username=username).first()
    if existing:
        print(f"❌ Administrator '{username}' already exists!")
        print(f"   ID: {existing.id}, Created: {existing.created_at}")
        return
    
    password = getpass("Password: ")
    if len(password) < 6:
        print("❌ Password must be at least 6 characters")
        return
    
    confirm = getpass("Confirm password: ")
    if password != confirm:
        print("❌ Passwords do not match!")
        return
    
    # Создаём нового
    admin = AdminUser(
        username=username,
        hashed_password=get_password_hash(password)
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"\n✅ Administrator '{username}' created successfully!")
    print(f"   ID: {admin.id}")
    print(f"   Created: {admin.created_at}")
    return admin

def delete_admin(db):
    """Удаляет администратора"""
    admins = list_admins(db)
    if not admins:
        return
    
    try:
        choice = input(f"\nEnter administrator number to delete (1-{len(admins)}): ").strip()
        if not choice.isdigit():
            print("❌ Please enter a number!")
            return
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(admins):
            print(f"❌ Number must be between 1 and {len(admins)}")
            return
        
        admin = admins[idx]
        
        # Подтверждение
        confirm = input(f"Are you sure you want to delete '{admin.username}' (ID: {admin.id})? [y/N]: ").strip().lower()
        if confirm != 'y':
            print("❌ Deletion cancelled")
            return
        
        # Удаляем
        username = admin.username
        db.delete(admin)
        db.commit()
        
        print(f"✅ Administrator '{username}' deleted")
        
    except (ValueError, IndexError):
        print("❌ Invalid number")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during deletion: {e}")

def change_password(db):
    """Смена пароля администратора"""
    admins = list_admins(db)
    if not admins:
        return
    
    try:
        choice = input(f"\nEnter administrator number to change password (1-{len(admins)}): ").strip()
        if not choice.isdigit():
            print("❌ Please enter a number!")
            return
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(admins):
            print(f"❌ Number must be between 1 and {len(admins)}")
            return
        
        admin = admins[idx]
        
        print(f"\n✏️  Change password for '{admin.username}'")
        print("-" * 30)
        
        # Запрос текущего пароля для подтверждения
        current = getpass("Current password (for verification): ")
        if not verify_password(current, admin.hashed_password):
            print("❌ Incorrect current password!")
            return
        
        new_password = getpass("New password: ")
        if len(new_password) < 6:
            print("❌ Password must be at least 6 characters")
            return
        
        confirm = getpass("Confirm new password: ")
        if new_password != confirm:
            print("❌ Passwords do not match!")
            return
        
        # Обновляем пароль
        admin.hashed_password = get_password_hash(new_password)
        db.commit()
        
        print(f"✅ Password for '{admin.username}' changed successfully!")
        
    except (ValueError, IndexError):
        print("❌ Invalid number")
    except Exception as e:
        db.rollback()
        print(f"❌ Error changing password: {e}")

def check_password(db):
    """Проверка пароля администратора"""
    admins = list_admins(db)
    if not admins:
        return
    
    try:
        choice = input(f"\nEnter administrator number to verify (1-{len(admins)}): ").strip()
        if not choice.isdigit():
            print("❌ Please enter a number!")
            return
        
        idx = int(choice) - 1
        if idx < 0 or idx >= len(admins):
            print(f"❌ Number must be between 1 and {len(admins)}")
            return
        
        admin = admins[idx]
        
        print(f"\n🔍 Verify password for '{admin.username}'")
        print("-" * 30)
        
        password = getpass("Password: ")
        
        if verify_password(password, admin.hashed_password):
            print("✅ Password is correct!")
        else:
            print("❌ Incorrect password!")
        
    except (ValueError, IndexError):
        print("❌ Invalid number")

def main():
    """Главная функция"""
    db = SessionLocal()
    
    try:
        while True:
            display_menu()
            
            choice = input("\nSelect action (1-6): ").strip()
            
            if choice == '1':
                list_admins(db)
            elif choice == '2':
                create_admin(db)
            elif choice == '3':
                delete_admin(db)
            elif choice == '4':
                change_password(db)
            elif choice == '5':
                check_password(db)
            elif choice == '6':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Enter number 1-6.")
            
            input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
