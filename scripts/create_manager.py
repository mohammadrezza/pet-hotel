import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pymongo import MongoClient
from app.user.model import Manager, UserRole
from app.utilities import gen_id, datetime_now

ADMIN_EMAIL = 'manager@gmail.com'
ADMIN_PASSWORD = '1qaz!QAZ'
DB_NAME = 'pet_hotel'

mongo = MongoClient(host="mongodb://localhost", port=27017)
db = mongo.get_database(DB_NAME)

res = db.users.delete_one({"email": ADMIN_EMAIL})
admin = Manager(identifier=gen_id(),
                fullname='manager',
                email=ADMIN_EMAIL,
                password='',
                role=UserRole.MANAGER,
                created_at=datetime_now(),
                updated_at=datetime_now())
admin.hash_password(ADMIN_PASSWORD)
res = db.users.insert_one(admin.dump())
if res.acknowledged and res.inserted_id != '':
    print(f"Successfully created manager user, credentials:")
    print('Email: ', ADMIN_EMAIL)
    print('Password: ', ADMIN_PASSWORD)
else:
    print("Failed to create manager user")
