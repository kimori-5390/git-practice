from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select
from tabulate import tabulate
from sqlalchemy import or_

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

engine = create_engine('sqlite:///core_users.db')
meta.create_all(engine)

users_values=[
    {'name':'Masahiro', 'lastname':'Yamamoto'},
    {'name':'Midori', 'lastname' : 'Sato'},
    {'name':'Etsuko','lastname' : 'Kobayashi'},
    {'name':'Ken','lastname' : 'Saito'},
    {'name':'Taro','lastname' : 'Yamada'},
    {'name':'Kentaro','lastname' : 'Tanaka'}
]

with engine.connect() as connection:
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

with engine.connect() as connection:
    connection.execute(addresses.insert(), addr_values)
    connection.commit()
    result = connection.execute(select(addresses))
    print(tabulate(result, headers=addresses.columns.keys(), tablefmt='pretty'))

with engine.connect() as connection:
    result = connection.execute(select(users.c.lastname, users.c.name))
    print(tabulate(result, headers=['lastname', 'name'], tablefmt='pretty'))

    query = select(users).where(users.c.name == 'Masahiro')
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

    query = select(users).where(or_(users.c.name == 'Masahiro', users.c.name == 'Midori'))
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))