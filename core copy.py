from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from tabulate import tabulate
from sqlalchemy.sql import join, select

engine = create_engine('sqlite:///core_users.db')
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
    Column(' user _id', Integer, ForeignKey('users.id')),
    Column('postal_add', String),
    Column('email_add', String)
)

meta.create_all(engine)

users_values=[
    {'name':'Masahiro', 'lastname':'Yamamoto'},
    {'name':'Midori', 'lastname' : 'Sato'},
    {'name':'Etsuko','lastname' : 'Kobayashi'},
    {'name':'Ken','lastname' : 'Saito'},
    {'name':'Taro','lastname' : 'Yamada'},
    {'name':'Kentaro','lastname' : 'Tanaka'}
]

connection = engine.connect()
connection.execute(users.insert(), users_values)
connection.commit()
result = connection.execute(select(users))
print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

addr_values = [
    {'user _id':1, 'postal_add':'Tokyo Minato-ku', 'email_add':'masahiro@gmail.com'},
    {'user _id':1, 'postal_add':'Nagoya Tempaku-ku', 'email_add':'masahiro@gmail.com'},
    {'user _id':3, 'postal_add':'Nagoya Mizuho-ku', 'email_add':'etsuko@gmail.com'},
    {'user _id':5, 'postal_add':'Kyouto Minami-ku', 'email_add':'taro@gmail.com'},
    {'user _id':2, 'postal_add':'Osaka Kita-ku', 'email_add':'midori@gmail.com'},
]

connection.execute(addresses.insert(), addr_values)
connection.commit()
result = connection.execute(select(addresses))
print(tabulate(result, headers=addresses.columns.keys(), tablefmt='pretty'))