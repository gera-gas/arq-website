import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Vacancy, AdminUser

db = SessionLocal()

print('👥 Admins:')
admins = db.query(AdminUser).all()
for admin in admins:
    print(f'  - {admin.username} (ID: {admin.id})')

print('\n💼 Vacancies:')
vacancies = db.query(Vacancy).all()
for vac in vacancies:
    status = 'Active' if vac.is_active else 'NoActive'
    print(f'  - {vac.title} ({status})')
    print(f'    Description: {vac.description[:50]}...')

db.close()
