from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from dotenv import load_dotenv
import os
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('issue', type=str)
parser.add_argument('user_id', type=int)
# not the type=dict


app = Flask(__name__)
api = Api(app)
    
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100),nullable=False)
    tickets_issued = db.relationship('Ticket',backref='ticket')
    last_issued_at = db.Column(db.DateTime)

    def __init__(self,name,last_issued_at):
        self.name = name
        self.last_issued_at = last_issued_at
    

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    issue_description = db.Column(db.String(150), nullable=False)
    raised_by_id = db.Column(db.Integer,nullable=False)
    tickets_issued_id = db.Column(db.Integer,db.ForeignKey('person.id'))
    def raised_by(self, person):
        self.raised_by_id = person.id

    def raised_by(self):
        return Person.query.filter_by(id=self.raised_by_id).first()

    def __init__(self,issue_description,raised_by_id,tickets_issued_id):
        self.issue_description = issue_description
        self.raised_by_id = raised_by_id
        self.tickets_issued_id = tickets_issued_id 

with app.app_context():
    db.create_all()
    f = '%Y-%m-%d %H:%M:%S'
    timeNow = datetime.now()
    last_issued = timeNow.strftime(f)
    db.session.add(Person(name='Muhammad',last_issued_at=last_issued))
    timeNow = datetime.now()
    last_issued = timeNow.strftime(f)
    db.session.add(Person(name='Piyush',last_issued_at=last_issued))
    timeNow = datetime.now()
    last_issued = timeNow.strftime(f)
    db.session.add(Person(name='Kajal',last_issued_at=last_issued))
    timeNow = datetime.now()
    last_issued = timeNow.strftime(f)
    db.session.add(Person(name='Huda',last_issued_at=last_issued))
    timeNow = datetime.now()
    last_issued = timeNow.strftime(f)
    db.session.add(Person(name='Rajesh',last_issued_at=last_issued))
    db.session.commit()

class TicketBooking(Resource):
    def post(self):
        try:
            
            args = parser.parse_args()
            json_data = request.get_json(force=True)
            # print(json_data)
            raised_by_user_id = args['user_id']
            issue_given = args['issue']            
            print("issued to",issue_given,raised_by_user_id,issued_to.id)
            issued_to = Person.query.order_by(asc(Person.last_issued_at)).first()
            try:

                ticket_created = Ticket(issue_description=issue_given,raised_by_id=raised_by_user_id,tickets_issued_id=issued_to.id)            
                
                print('ticket here')
                db.session.add(ticket_created)
                from datetime import datetime
                issued_to.last_issued_at = datetime.now()
                                
                db.session.commit()
                
                return ({'message':'ticket assigned','success':True,'data':{'ticket_id':ticket_created.id,'assigned_to':ticket_created.tickets_issued_id}}), 201
            
            except:
                return ({'message':'Generation of ticket failed. Try again later','success':False,'data':{'ticket_id':None,'assigned_to':None}}), 500
            
        except:
            return {'message':'Required parameters missing. Try again','success':False,'data':{'ticket_id':None,'assigned_to':None}},400


api.add_resource(TicketBooking,'/ticket')