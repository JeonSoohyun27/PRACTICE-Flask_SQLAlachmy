#데이터베이스랑 flask-sqlachemy 연결해주는 과정
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#데이터베이스랑 연결하기 위해서는 데이터베이스 url 이 필요
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/flask'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False) #80글자까지
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    
#ipython 에서 from application import db
# db.create_all() 로 테이블 생성 
#재실행시 service mysql start 켜주기
#source venv/bin/activate 로 가상환경 켜주기

# -----------------------CREATE-----------------------------
# ipython

# In [2]: from application import User
# User 불러와주기

# In [3]: spring = User(username='spring',email='spring@mail.com')
# spring이라는 객체 생성

# In [4]: spring
# Out[4]: <User 'spring'>
#     def __repr__(self):
#        return '<User %r>' % self.username
# 이부분때매 저렇게 나옴

# In [5]: db.session.add(spring)
# db에 만들어진 spring을 추가

# In [6]: db.session.commit()
# db에 추가한 spring을 저장

# 밑에처럼 결과가 생기게 됨. 
# mysql> select * from user;
# +----+----------+-----------------+
# | id | username | email           |
# +----+----------+-----------------+
# |  1 | spring   | spring@mail.com |
# +----+----------+-----------------+


# -----------------------READ----------------------------------
# In [2]: from application import db,User

# In [3]: User.query.all()
# Out[3]: [<User 'spring'>]
# 모든 쿼리를 불러옴

# In [4]: spring = User.query.first()
# spring이라는 객체에 User 쿼리중 첫번째를 담아줌

# In [5]: spring
# Out[5]: <User 'spring'>
# list가 벗겨진 모습을 확인 할 수 있음


# -------------------------UPDATE---------------------------
# 데이터 변경 전 내용
# mysql> select * from user;
# +----+----------+-----------------+
# | id | username | email           |
# +----+----------+-----------------+
# |  1 | spring   | spring@mail.com |
# +----+----------+-----------------+

#ipython
# In [1]: from application import db,User
# db랑 User 불러와주기

# In [2]: spring = User.query.first()
# 아까처럼 spring에 첫번째 데이터를 담아준다

# In [4]: spring
# Out[4]: <User 'spring'>

# In [5]: spring.email
# Out[5]: 'spring@mail.com'
# 데이터의 email을 확인했을때 변경 전 데이터가 나오는 모습


# In [6]: spring.email = 'spring@gmail.com'
# 데이터 변경 과정

# In [7]: spring.email
# Out[7]: 'spring@gmail.com'
# 변경 후 찍히는 모습 mail -> gmail


# In [8]: db.session.commit()
# db에 저장하기

# db 들어가서 확인해보면 변경되어있는 걸 확인할 수 있음.    
# mysql> select * from user;
# +----+----------+------------------+
# | id | username | email            |
# +----+----------+------------------+
# |  1 | spring   | spring@gmail.com |
# +----+----------+------------------+

# --------------------DELETE------------------------- 

# UPDATE 로 변경된 데이터 
# mysql> select * from user;
# +----+----------+------------------+
# | id | username | email            |
# +----+----------+------------------+
# |  1 | spring   | spring@gmail.com |
# +----+----------+------------------+


# ipython
# In [1]: from application import db,User
# db,User 불러와주고

# In [2]: User.query.get(1)
# Out[2]: <User 'spring'>
# query.get()에 pk번호를 넣어서 해당 데이터를 불러올 수있음

# In [3]: spring = User.query.get(1)
# pk id = 1 인 데이터를 spring에 넣어준다.

# In [5]: db.session.delete(spring)
# session.delete()를 통해 지워주기

# In [6]: User.query.all()
# Out[6]: []
# query.all() 로 확인했을 떄 빈 리스트가 반환되는 걸 확인.    

# In [7]: db.session.commit()
# db에 저장해주기
    
# mysql db상에 삭제된 모습 확인
# mysql> select * from user;
# Empty set (0.00 sec)

# -----------------------query-------------------------
#EQUAL / NOT EQUAL
# filter 를 사용해야함.
# EQUAL
# In [2]: User.query.filter(User.id == 1).first()
# Out[2]: <User 'spring'>

# In [3]: user_id_1 = User.query.filter(User.id == 1).first()

# In [4]: user_id_1
# Out[4]: <User 'spring'>

# In [5]: user_id_1.username
# Out[5]: 'spring'

# NOT EQUAL

# In [6]: user_id_not_1 = User.query.filter(User.id != 1).all()
    
# In [7]: user_id_not_1
# Out[7]:
# [<User 'summer'>,
#  <User 'fall'>,
#  <User 'winter'>,
#  <User 'seoul'>,
#  <User 'tokyo'>]

# In [8]: summer = User.query.filter(User.username == 'summer').first()

# In [9]: summer
# Out[9]: <User 'summer'>

# In [10]: summer.email
# Out[10]: 'summer@mail.com'

# -----------------------queryt-like-------------------------

# gmail이 있는지 알아보는 명령어
# In [4]: User.query.filter(User.email.like('%gmail%')).all()
# Out[4]: [<User 'winter'>]

#like는 '% 심볼을 가지고 검색어를 찾는기능

# -----------------------queryt-in/not in-------------------------

# in을 사용시에는 in_ 의 형태로 사용 
# In [6]: User.query.filter(User.username.in_(['spring','fall'])).all()
# Out[6]: [<User 'spring'>, <User 'fall'>]

# not in 사용시에는 해당클래스 앞에 ~ 표시 붙혀서 사용    
# In [7]: User.query.filter(~User.username.in_(['spring','fall'])).all()
# Out[7]: [<User 'summer'>, <User 'winter'>, <User 'seoul'>, <User 'tokyo'>]
