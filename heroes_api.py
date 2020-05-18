import flask
from flask import request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

app = flask.Flask(__name__)
app.config["DEBUG"] = True
eng = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=eng))
Base = declarative_base()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Marvel Heroes</p>"


@app.route('/api/v1/heroes/all', methods=['GET'])
def heroes():
    heroes = []
    rs = ses.query(Heroes).all()
    for hero in rs:
        one_hero = {'HID': hero.HID, 'Hero_name': hero.Hero_name, 'About': hero.About, 'SuperPower': hero.SuperPower}
        heroes.append(one_hero)
    return jsonify(heroes)


@app.route('/api/v1/heroes', methods=['GET'])
def hero_id():
    if 'HID' in request.args:
        try:
            hid = int(request.args['HID'])
        except ValueError:
            return jsonify('Pateikta bloga reiksme')
    results = []
    heroes = []
    rs = ses.query(Heroes).all()
    for hero in rs:
        one_hero = {'HID': hero.HID, 'Hero_name': hero.Hero_name, 'About': hero.About, 'SuperPower': hero.SuperPower}
        heroes.append(one_hero)
    for he in heroes:
        if he['HID'] == hid:
            results.append(he)
    return jsonify(results)


@app.route('/api/v1/heroes/add', methods=['POST'])
def add_hero():
    heroes = []
    content = request.json
    res = ses.query(Heroes).all()
    for hero in res:
        one_hero = {'HID': hero.HID, 'Hero_name': hero.Hero_name, 'About': hero.About, 'SuperPower': hero.SuperPower}
        heroes.append(one_hero)
    if 'HID' in content and 'Hero_name' in content and 'About'in content and 'SuperPower' in content:
        ses.add_all([Heroes(HID=content['HID'], Hero_name=content['Hero_name'], About=content['About'],
                            SuperPower=content['SuperPower'])])
    else:
        return jsonify('Blogai nurodytas vienas is parametru')
    # Tikrinam ar jau egzistuoja toks irasas
    for hero in heroes:
        if hero['HID'] == content['HID']:
            return jsonify('Toks HID jau egzistuoja')
    ifaila = ses.query(Heroes).all()
    f = open('data.txt', 'w')
    for hero in ifaila:
        listas = (str(hero.HID), hero.Hero_name, hero.About, hero.SuperPower)
        f.write(';'.join(listas) + '\n')
    f.close()
    '''res = ses.query(Heroes).all()
    for hero in res:
        print(hero.HID, hero.Hero_name, hero.About, hero.SuperPower)'''
    return jsonify('Herojus pridetas sekmingai')


class Heroes(Base):
    __tablename__ = "Heroes"

    HID = Column(Integer, primary_key=True)
    Hero_name = Column(String)
    About = Column(String)
    SuperPower = Column(String)


Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()

# Reading from file and filling in DB
with open('data.txt', 'r') as failas:
    for line in failas:
        ses.add_all([Heroes(HID=int(line.split(';')[0]), Hero_name=line.split(';')[1], About=line.split(';')[2],
                            SuperPower=line.split(';')[3])])
failas.close()
ses.commit()

rs = ses.query(Heroes).all()

app.run()
