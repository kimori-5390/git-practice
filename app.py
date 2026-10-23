from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select
from tabulate import tabulate
from sqlalchemy import or_
import sys

engine = create_engine('sqlite:///core_users2.db')

meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String),
    Column('lastname', String),
)

addresses = Table(
    'addresses', meta,
    Column('id', Integer, primary_key = True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('postal_add', String),
    Column('email_add', String)
)

meta.create_all(engine)

print("アカウントを作るか、アカウントを検索するか選択してください。")
print("1: アカウントを作る, 2: アカウントを検索")
num = int(input("半角数字で入力してください:"))

if num == 1:
    name = input("名前を入力してください:")
    lastname = input("苗字を入力してください:")
    postal_add = input("住所を入力してください:")
    email_add = input("メールアドレスを入力してください:")
    user_values = {'name': name, 'lastname': lastname}
    with engine.connect() as connection:
        connection.execute(users.insert(), user_values)
        connection.commit()
    print("アカウントが作成されました。")
    sys.exit()
elif num == 2:
    search_name = input("検索したい名前を入力してください:")
    search_lastname = input("検索したい苗字を入力してください:")
    search_values = {'name': search_name, 'lastname': search_lastname}
    with engine.connect() as connection:
        query = select(users).where(users.c.name == search_name and users.c.lastname == search_lastname)
        result = connection.execute(query)
        print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))