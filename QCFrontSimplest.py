import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_accepted,\
login_user, logout_user
#from flask_socketio import SocketIO, emit
from flask import render_template, request, session, redirect, url_for, flash

##Create the app
app = Flask(__name__)

app.config.from_object('config')
#socketio = SocketIO(app)

##Create the database connection object
db = SQLAlchemy(app)

##Models
##Define models for the user authentication
roles_users = db.Table('roles_users',
                           db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                           db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                                backref=db.backref('users', lazy='dynamic'))

##Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore) #I needed a decorator @login_required and then to html override the template


#Existing models
db.Model.metadata.reflect(db.engine) #database is bound to an engine here

class LinkMsrRds(db.Model):
    __table__ = db.Model.metadata.tables['linkmiseqrunrds']

    def __init__(self, LinkMiSeqRunRdsID, MiSeqRunID, ReadID):
        self.LinkMiSeqRunRdsID = LinkMiSeqRunRdsID
        self.MiSeqRunID = MiSeqRunID
        self.ReadID = ReadID

    def __repr__(self):
        return "<LinkMSRRds(%s,%s,%s)>" % (self.LinkMiSeqRunRdsID, self.MiSeqRunID, self.ReadID)

class Msr(db.Model):
    __table__ = db.Model.metadata.tables['miseqrun'] #case sensitive

    def __init__(self,MiSeqRunID,RunStartDate,RunNumber,Instrument,FPGAVersion,MCSVersion,
                    RTAVersion,KitVersionNumber,OnboardAnalysis,ExperimentName,Operator,Chemistry,
                    Pipeline,FlowCell,FlowCellPartID,FlowCellExpiry,PR2Bottle,PR2BottlePartID,
                 PR2BottleExpiry,ReagentKit,ReagentKitPartID,ReagentKitExpiry,NumTiles,NumSwaths,
                    NumLanes,NumSurfaces):
        self.MiSeqRunID = MiSeqRunID
        self.RunStartDate = RunStartDate
        self.RunNumber = RunNumber
        self.Instrument = Instrument
        self.FPGAVersion = FPGAVersion
        self.MCSVersion = MCSVersion
        self.RTAVersion = RTAVersion
        self.KitVersionNumber = KitVersionNumber
        self.OnboardAnalysis = OnboardAnalysis
        self.ExperimentName = ExperimentName
        self.Operator = Operator
        self.Chemistry = Chemistry
        self.Pipeline = Pipeline
        self.FlowCell = FlowCell
        self.FlowCellPartID = FlowCellPartID
        self.FlowCellExpiry = FlowCellExpiry
        self.PR2Bottle = PR2Bottle
        self.PR2BottlePartID = PR2BottlePartID
        self.PR2BottleExpiry = PR2BottleExpiry
        self.ReagentKit = ReagentKit
        self.ReagentKitPartID = ReagentKitPartID
        self.ReagentKitExpiry = ReagentKitExpiry
        self.NumTiles = NumTiles
        self.NumSwaths = NumSwaths
        self.NumLanes = NumLanes
        self.NumSurfaces = NumSurfaces

    def __repr__(self):
        return"<MiSeqRun(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)>" \
              % (self.MiSeqRunID,self.RunStartDate,self.RunNumber,self.Instrument,self.FPGAVersion,self.MCSVersion,
                 self.RTAVersion,self.KitVersionNumber,self.OnboardAnalysis,self.ExperimentName,self.Operator,
                 self.Chemistry,self.Pipeline,self.FlowCell,self.FlowCellPartID,self.FlowCellExpiry,self.PR2Bottle,
                 self.PR2BottlePartID,self.PR2BottleExpiry,self.ReagentKit,self.ReagentKitPartID,self.ReagentKitExpiry,
                 self.NumTiles,self.NumSwaths,self.NumLanes,self.NumSurfaces)

class Rds(db.Model):
    __table__ = db.Model.metadata.tables['rds']

    def __init__(self,ReadID,ReadNumber,Indexed,NumberOfCycles):
        self.ReadID = ReadID
        self.ReadNumber = ReadNumber
        self.Indexed = Indexed
        self.NumberOfCycles = NumberOfCycles #Can have a different variable name here and it doesn't break for the queries used

    def __repr__(self):
        return"<Reads(%s,%s,%s,%s)>" % (self.ReadID,self.ReadNumber,self.Indexed,self.NumberOfCycles)


## Add a new user
@app.route('/register_user')
#@roles_accepted('admin') #Just for testing have commented out
def create_user():
    create_user(email='nop', password='yep')
    #user_datastore.create_user(email='matt@notface.net', password='passbags')
    #db.session.commit()
    flash('User added')
    return render_template('home.html')

''' #This approach is still not working 17/06/16
@socketio.on('disconnect')
def disconnect_user():
    #Disconnects the user when the browser is closed
    #Annoyingly this is now not working as expected
    return logout()
'''

@app.route('/', methods=['GET', 'POST'])
def base_screen():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_user()
    flash('You were logged in')
    return redirect(url_for('base_screen'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('base_screen'))

@app.route('/query', methods=['GET', 'POST'])
@login_required
def query_page():
    func_dict = dict([('run identifier','MiSeqRunID'),('run date', 'RunStartDate'),
                      ('reagent kit part id', 'ReagentKit'),('miseq', 'Instrument')])
    miseq_dict = dict([('nemo','M00766'),('dory','M02641')])
    searchfor_dict = dict([('msrid','MiSeqRunID'),('rundt','RunStartDate'),('ins','Instrument'),
                           ('ktver','KitVersionNumber'),('op','Operator'),('numrds','<fix_me>')])
    non_checkbox_inputs = ['search_term','button','seq_op']
    if request.method == 'POST':
        button = request.form['button'] # could differentiate here by changing name in html
        searcher = func_dict.get(button,None)
        identifier = request.form['search_term']
        if (button == 'miseq') and ((identifier.lower()) in miseq_dict.keys()):
            identifier = miseq_dict.get(identifier.lower(),None)
        search_dict = dict([(searcher,identifier)])
        if not identifier:
            flash('No data entered')
            return redirect(url_for('query_page'))
        else:
            # Returns all of the results as an object, which will will take attributes from later
            subset_records_MSR = Msr.query.filter_by(**search_dict).all()
            # Identify the subset of data required by the request
            requesters = request.form
            desired_output = []
            for k in requesters.keys():
                if k not in non_checkbox_inputs:
                    desired_output.append(searchfor_dict.get(k, None))

            # Handle where no checkboxes have been ticked
            if desired_output == []:
                flash('No checkboxes selected for data to return')
                return redirect(url_for('query_page'))

            # To aid understanding, 'results' is used here, which is the result of the query
            results = subset_records_MSR
            if not results:
                message_to_flash = 'Identifier not found in the database for "%s". Please try again.' % button
                flash(message_to_flash)
                return redirect(url_for('query_page'))

            ## I'm not really happy with the below code- need to fix it later ##
            all_entries = []
            for entry in results:
                this_entry = []
                headers = [] #This is a bit inefficient, it re-sets the headers every time-- FIX
                if "MiSeqRunID" in desired_output:
                    msrid = entry.MiSeqRunID
                    this_entry.append(str(msrid)) #Convert to a string so that the format of display is not weird
                    headers.append('MiSeq run identifier')
                if "RunStartDate" in desired_output:
                    rsd = entry.RunStartDate
                    this_entry.append(str(rsd))
                    headers.append('Date of run')
                if "Instrument" in desired_output:
                    ins = entry.Instrument
                    this_entry.append(str(ins))
                    headers.append('MiSeq used')
                if "KitVersionNumber" in desired_output:
                    ktv = entry.KitVersionNumber
                    this_entry.append(str(ktv))
                    headers.append('Kit version number')
                if "Operator" in desired_output:
                    ope = entry.Operator
                    this_entry.append(str(ope).strip('\n')) #Required as a \n in at the end of the operator name
                    headers.append('Operator')
                this_entry = tuple(this_entry)
                all_entries.append(this_entry)
        return render_template('query_result.html', entries=all_entries, headers=headers)
    return render_template('query.html')



if __name__ == '__main__':
    app.run()