from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select, join
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
    Column('user_id', Integer, ForeignKey('users.id')),
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

with engine.connect() as connection:
    connection.execute(users.insert(), users_values)
    connection.commit()
    result = connection.execute(select(users))
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

addr_values = [
    {'user_id':1, 'postal_add':'Tokyo Minato-ku', 'email_add':'masahiro@gmail.com'},
    {'user_id':1, 'postal_add':'Nagoya Tempaku-ku', 'email_add':'masahiro@gmail.com'},
    {'user_id':3, 'postal_add':'Nagoya Mizuho-ku', 'email_add':'etsuko@gmail.com'},
    {'user_id':5, 'postal_add':'Kyouto Minami-ku', 'email_add':'taro@gmail.com'},
    {'user_id':2, 'postal_add':'Osaka Kita-ku', 'email_add':'midori@gmail.com'},
]

with engine.connect() as connection:
    connection.execute(addresses.insert(), addr_values)
    connection.commit()
    result = connection.execute(select(addresses))
    print(tabulate(result, headers=addresses.columns.keys(), tablefmt='pretty'))


# 特定の列を選択
with engine.connect() as connection:
    result = connection.execute(select(users.c.lastname, users.c.name))
    print(tabulate(result, headers=['lastname', 'name'], tablefmt='pretty'))

    query = select(users).where(users.c.name == 'Masahiro')
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

    query = select(users).where(or_(users.c.name == 'Masahiro', users.c.name == 'Midori'))
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

    query=select(users).where(users.c.name.like('Ken%')) # 大文字小文字を区別する検索
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

    query = select(users).where(users.c.name.ilike('ken%')) # 大文字小文字を区別しない検索
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

    patterns = ['K%', 'T%']
    query=select(users).where(or_(*[users.c.name.like(p) for p in patterns]))
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))
 
    query=select(users).order_by(users.c.name) # 昇順で並び替え
    result = connection.execute(query)
    print(tabulate(result, headers=users.columns.keys(), tablefmt='pretty'))

    # 降順で並び替え
    query=select(addresses).order_by(addresses.c.postal_add.desc())
    result = connection.execute(query)
    print(tabulate(result, headers=addresses.columns.keys(), tablefmt='pretty'))

    # 複数の列で並び替え
    query=select(addresses).order_by(addresses.c.email_add.asc(), addresses.c.postal_add.asc())
    result = connection.execute(query)
    print(tabulate(result, headers=addresses.columns.keys(), tablefmt='pretty'))

    query = select(users, addresses).where(users.c.id == addresses.c.user_id)
    result = connection.execute(query)
    for row in result:
        print(row)


    print("結合の例")
    query = select(users, addresses).where(users.c.id == addresses.c.user_id)
    result = connection.execute(query)
    for row in result:
        print(row)

    print("\n\n結合の例2")
    stmt1 = select(users, addresses).select_from(users.join(addresses))
    result1 = connection.execute(stmt1)
    for row in result1:
        print(row)


    stmt2 = select(users, addresses).select_from(join(users,addresses))
    result2 = connection.execute(stmt2)
    for row in result2:
        print(row)

    stmt3 = select(users, addresses).select_from(users.join(addresses,users.c.id == addresses.c.user_id))
    result3 = connection.execute(stmt3)
    for row in result3:
        print(row)

    print('\n\n次は結合したテーブルから特定の列を取り出す。')
    stmt4 = select(users.c.name, addresses.c.postal_add).select_from(users.join(addresses))
    result4 = connection.execute(stmt4)
    print(tabulate(result4, headers=['name', 'postal_add'], tablefmt='pretty'))

    stmt5 = select(users.c.name, addresses.c.postal_add).select_from(users.join(addresses)).where(users.c.name == 'Masahiro')
    result5 = connection.execute(stmt5)
    print(tabulate(result5, headers=['name', 'postal_add'], tablefmt='pretty'))

    subq2 = select(users.c.id).where(users.c.name == 'Masahiro').subquery()
    stmt2 = select(users.c.name, addresses.c.postal_add).select_from(users.join(addresses)).where(users.c.id == subq2.c.id)
    result = connection.execute(stmt2)
    print(tabulate(result, headers=['name', 'postal_add'], tablefmt='pretty'))