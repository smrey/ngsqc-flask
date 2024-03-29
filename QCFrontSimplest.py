from datetime import timedelta
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_accepted,\
login_user, logout_user, current_user
from flask.ext.security.utils import encrypt_password
from flask import render_template, request, session, redirect, url_for, flash
from flask_wtf.csrf import CsrfProtect

##Create the app
app = Flask(__name__)

##Import the configuration specified in the config.py file
app.config.from_pyfile('config.py')

##Create the database connection object
db = SQLAlchemy(app)

#Include csrf protection
csrf = CsrfProtect(app)

##Models
##Define models for the user authentication
'''
These models were created as relations in the database using the command db.createall() the first time the application
is run.
'''
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
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(20))
    current_login_ip = db.Column(db.String(20))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                                backref=db.backref('users', lazy='dynamic'))


##Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


#Existing models
'''
These relations already existed in the database prior to development of the front end. The reflect command from
flask-sql alchemy has been used to create a model of the relations and tuples, so these are not defined explicitly.
The __repr__ function defines how the data within the class object is returned.
'''
db.Model.metadata.reflect(db.engine) #database is bound to an engine here

class LinkMsrRds(db.Model):
    __table__ = db.Model.metadata.tables['linkmiseqrunrds']

    def __init__(self, MiSeqRunID, ReadID):
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

    def __init__(self,ReadNumber,Indexed,NumberOfCycles):
        self.ReadNumber = ReadNumber
        self.Indexed = Indexed
        self.NumberOfCycles = NumberOfCycles #Can have a different variable name here and it doesn't break for the queries used

    def __repr__(self):
        return"<Reads(%s,%s,%s,%s)>" % (self.ReadID,self.ReadNumber,self.Indexed,self.NumberOfCycles)


##Beginning of the application code
@app.before_first_request
def make_roles():
    '''
    Checks that the required roles exist in the database and if not adds them.
    More roles could be added from this function using the same syntax as below.
    :return: None
    '''
    user_datastore.find_or_create_role(name='admin', description='database administrator')
    user_datastore.find_or_create_role(name='user', description='standard user')
    db.session.commit()

@app.before_request
def session_management():
    '''
    Makes the app timeout after 5 minutes of inactivity
    :return: None
    '''
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

## Add a new user
# Only available to users logged in with admin permissions
@app.route('/register', methods=['GET', 'POST'])
@roles_accepted('admin')
def create_user():
    '''
    Requires users with administrative privileges
    Allows new users of the web application to be added
    :return: returns the administrator to the user registration screen
    '''
    error = None
    if request.method == 'POST':
        un = request.form['username']
        if user_datastore.get_user(un) != None:
            flash('Username already in database')
            return redirect(url_for('create_user'))
        pa = request.form['password']
        if pa == '':
            flash('Please enter a password for the user')
            return redirect(url_for('create_user'))
        cl = request.form['userclass']
        if (cl != "admin") and (cl != "user"):
            flash('A user must belong to either the "admin" or "user" user class')
            return redirect(url_for('create_user'))
        user_datastore.create_user(email=un, password=encrypt_password(pa))
        user_datastore.add_role_to_user(un,cl)
        db.session.commit()
        flash('User added')
    return render_template('register.html', error=error)

#Delete a user
@app.route('/delete_user', methods=['GET', 'POST'])
@roles_accepted('admin')
def delete_user():
    '''
    Requires users with administrative privileges
    Allows users of the web application to be removed
    :return: returns the administrator to the remove user screen
    '''
    error = None
    if request.method == 'POST':
        user_for_deletion = request.form['to_delete']
        to_delete = User.query.filter_by(email=user_for_deletion).first()
        if to_delete == None:
            flash('This user does not exist')
            return redirect(url_for('delete_user'))
        user_datastore.delete_user(to_delete)
        db.session.commit()
        flash('User "%s" deleted' % user_for_deletion)
    return render_template('remove_user.html', error=error)


@app.route('/', methods=['GET', 'POST'])
def base_screen():
    '''
    Displays the home screen and a popup indicating whether the user is logged in or not
    :return: home screen
    '''
    admin = False
    loggedin = current_user.is_authenticated
    if loggedin:
        flash('You are logged in as "%s"' % current_user.email )
        admin = current_user.has_role('admin')
    if not loggedin:
        flash('You are logged out')
    return render_template('home.html', loggedin=loggedin, admin=admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Allows the user to log in to the web application
    :return: returns the user to the home screen
    '''
    login_user()
    return redirect(url_for('base_screen'))

@app.route('/logout')
def logout():
    '''
    Allows the user to log out of the web application
    :return: returns the user to the home screen
    '''
    logout_user()
    return redirect(url_for('base_screen'))

@app.route('/query', methods=['GET', 'POST'])
@login_required
def query_page():
    '''
    Allows a logged in user to make queries by Run identifier, Run date, Reagent kit or Operator.
    Informs the user if no data was entered, if no checkboxes were selected indicating the subset of data to retrieve,
    or if no data matching the criteria was found in the database and returns the user to the query statement
    :return: Returns the subset of data requested in a table format
    '''
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

            # To aid readability, 'results' is used here, which is the result of the query
            results = subset_records_MSR
            if not results:
                message_to_flash = 'Identifier not found in the database for "%s". Please try again.' % button
                flash(message_to_flash)
                return redirect(url_for('query_page'))

            ## I'm not really happy with the below code- need to fix it later ##
            all_entries = []
            headers = []
            for entry in results:
                this_entry = []
                headers = [] #This is a bit inefficient, it re-sets the headers every time-- FIX
                if "MiSeqRunID" in desired_output:
                    msrid = entry.MiSeqRunID
                    this_entry.append(str(msrid)) #Convert to a string so that the format of display is as required
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


#Run the application, but only if the script is run directly
if __name__ == '__main__':
    app.run()