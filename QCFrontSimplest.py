import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
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

class IntM(db.Model):
    __table__ = db.Model.metadata.tables['correctedintmetrics']

    def __init__(self, LaneID, TileID, CycleID, MiSeqRunID, AverageIntensity, AverageCorrectedIntensity_A,
                 AverageCorrectedIntensity_C, AverageCorrectedIntensity_G, AverageCorrectedIntensity_T,
                 AverageCorrectedIntensityCalledClusters_A, AverageCorrectedIntensityCalledClusters_C,
                 AverageCorrectedIntensityCalledClusters_G, AverageCorrectedIntensityCalledClusters_T,
                 NumNoCalls, NUM_A, NUM_C, NUM_G, NUM_T, Signal2NoiseRatio):
        self.LaneID = LaneID
        self.TileID = TileID
        self.CycleID = CycleID
        self.MiSeqRunID = MiSeqRunID
        self.AverageIntensity = AverageIntensity
        self.AverageCorrectedIntensity_A = AverageCorrectedIntensity_A
        self.AverageCorrectedIntensity_C = AverageCorrectedIntensity_C
        self.AverageCorrectedIntensity_G = AverageCorrectedIntensity_G
        self.AverageCorrectedIntensity_T = AverageCorrectedIntensity_T
        self.AverageCorrectedIntensityCalledClusters_A = AverageCorrectedIntensityCalledClusters_A
        self.AverageCorrectedIntensityCalledClusters_C = AverageCorrectedIntensityCalledClusters_C
        self.AverageCorrectedIntensityCalledClusters_G = AverageCorrectedIntensityCalledClusters_G
        self.AverageCorrectedIntensityCalledClusters_T = AverageCorrectedIntensityCalledClusters_T
        self.NumNoCalls = NumNoCalls
        self.NUM_A = NUM_A
        self.NUM_C = NUM_C
        self.NUM_G = NUM_G
        self.NUM_T = NUM_T
        self.Signal2NoiseRatio = Signal2NoiseRatio

    def __repr__(self):
        return "<CorrectedIntMetrics(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)>" \
               % (self.LaneID, self.TileID, self.CycleID, self.MiSeqRunID, self.AverageIntensity,
                  self.AverageCorrectedIntensity_A, self.AverageCorrectedIntensity_C, self.AverageCorrectedIntensity_G,
                  self.AverageCorrectedIntensity_T, self.AverageCorrectedIntensityCalledClusters_A,
                  self.AverageCorrectedIntensityCalledClusters_C, self.AverageCorrectedIntensityCalledClusters_G,
                  self.AverageCorrectedIntensityCalledClusters_T, self.NumNoCalls, self.NUM_A, self.NUM_C, self.NUM_G,
                  self.NUM_T, self.Signal2NoiseRatio)


class ExtM(db.Model):
    __table__ = db.Model.metadata.tables['extractionmetrics']

    def __init__(self, LaneID, TileID, CycleID, MiSeqRunID, FWHM_A, FWHM_C, FWHM_G, FWHM_T, Intensity_A, Intensity_C,
                 Intensity_G, Intensity_T, Date, Time):
        self.LaneID = LaneID
        self.TileID = TileID
        self.CycleID = CycleID
        self.MiSeqRunID = MiSeqRunID
        self.FWHM_A = FWHM_A
        self.FWHM_C = FWHM_C
        self.FWHM_G = FWHM_G
        self.FWHM_T = FWHM_T
        self.Intensity_A = Intensity_A
        self.Intensity_C = Intensity_C
        self.Intensity_G = Intensity_G
        self.Intensity_T = Intensity_T
        self.Date = Date
        self.Time = Time

    def __repr__(self):
        return "<ExtractionMetrics(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)>" \
               % (self.LaneID, self.TileID, self.CycleID, self.MiSeqRunID, self.FWHM_A, self.FWHM_C, self.FWHM_G,
                  self.FWHM_T, self.Intensity_A, self.Intensity_C, self.Intensity_G, self.Intensity_T, self.Date,
                  self.Time)


class ErrM(db.Model):
    __table__ = db.Model.metadata.tables['errormetrics']

    def __init__(self, LaneID, TileID, CycleID, MiSeqRunID, ErrorRate, NumPerfectRds, NumSingleError, NumDoubleError,
                 NumTripleError, NumQuadrupleError):
        self.LaneID = LaneID
        self.TileID = TileID
        self.CycleID = CycleID
        self.MiSeqRunID = MiSeqRunID
        self.ErrorRate = ErrorRate
        self.NumPerfectRds = NumPerfectRds
        self.NumSingleError = NumSingleError
        self.NumDoubleError = NumDoubleError
        self.NumTripleError = NumTripleError
        self.NumQuadrupleError = NumQuadrupleError

def __repr__(self):
    return "<ErrorMetrics(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)>" \
           % (self.LaneID, self.TileID, self.CycleID, self.MiSeqRunID, self.ErrorRate, self.NumPerfectRds,
              self.NumSingleError, self.NumDoubleError, self.NumTripleError, self.NumQuadrupleError)


class IndMMsr(db.Model):
    __table__ = db.Model.metadata.tables['indexmetricsmsr']

    def __init__(self, LaneID, TileID, ReadNum, MiSeqRunID, IndexName, NumControlClusters, SampleName, ProjectName):
        self.LaneID = LaneID
        self.TileID = TileID
        self.ReadNum = ReadNum
        self.MiSeqRunID = MiSeqRunID
        self.IndexName = IndexName
        self.NumControlClusters = NumControlClusters
        self.SampleName = SampleName
        self.ProjectName = ProjectName

    def __repr__(self):
        return "<IndexMetricsMiSeqRun(%s,%s,%s,%s,%s,%s,%s,%s)>" \
            % (self.LaneID, self.TileID, self.ReadNum, self.MiSeqRunID, self.IndexName, self.NumControlClusters,
               self.SampleName,self.ProjectName)


class QualM(db.Model):
    __table__ = db.Model.metadata.tables['qualitymetrics']

    def __init__(self, LaneID, TileID, CycleID,MiSeqRunID,Q01,Q02,Q03,Q04,Q05,Q06,Q07,Q08,Q09,Q10,Q11,Q12,Q13,Q14,
                    Q15,Q16,Q17,Q18,Q19,Q20,Q21,Q22,Q23,Q24,Q25,Q26,Q27,Q28,Q29,Q30,Q31,Q32,Q33,Q34,Q35,Q36,Q37,Q38,
                    Q39,Q40,Q41,Q42,Q43,Q44,Q45,Q46,Q47,Q48,Q49,Q50):
        self.LaneID = LaneID
        self.TileID = TileID
        self.CycleID = CycleID
        self.MiSeqRunID = MiSeqRunID
        self.Q01 = Q01
        self.Q02 = Q02
        self.Q03 = Q03
        self.Q04 = Q04
        self.Q05 = Q05
        self.Q06 = Q06
        self.Q07 = Q07
        self.Q08 = Q08
        self.Q09 = Q09
        self.Q10 = Q10
        self.Q11 = Q11
        self.Q12 = Q12
        self.Q13 = Q13
        self.Q14 = Q14
        self.Q15 = Q15
        self.Q16 = Q16
        self.Q17 = Q17
        self.Q18 = Q18
        self.Q19 = Q19
        self.Q20 = Q20
        self.Q21 = Q21
        self.Q22 = Q22
        self.Q23 = Q23
        self.Q24 = Q24
        self.Q25 = Q25
        self.Q26 = Q26
        self.Q27 = Q27
        self.Q28 = Q28
        self.Q29 = Q29
        self.Q30 = Q30
        self.Q31 = Q31
        self.Q32 = Q32
        self.Q33 = Q33
        self.Q34 = Q34
        self.Q35 = Q35
        self.Q36 = Q36
        self.Q37 = Q37
        self.Q38 = Q38
        self.Q39 = Q39
        self.Q40 = Q40
        self.Q41 = Q41
        self.Q42 = Q42
        self.Q43 = Q43
        self.Q44 = Q44
        self.Q45 = Q45
        self.Q46 = Q46
        self.Q47 = Q47
        self.Q48 = Q48
        self.Q49 = Q49
        self.Q50 = Q50

    def __repr__(self):
        return "<QualityMetrics(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
               "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)>" \
               % (self.LaneID, self.TileID, self.CycleID,self.MiSeqRunID,self.Q01,self.Q02,self.Q03,self.Q04,self.Q05,
                  self.Q06,self.Q07,self.Q08,self.Q09,self.Q10,self.Q11,self.Q12,self.Q13,self.Q14,self.Q15,self.Q16,
                  self.Q17,self.Q18,self.Q19,self.Q20,self.Q21,self.Q22,self.Q23,self.Q24,self.Q25,self.Q26,self.Q27,
                  self.Q28,self.Q29,self.Q30,self.Q31,self.Q32,self.Q33,self.Q34,self.Q35,self.Q36,self.Q37,self.Q38,
                    self.Q39,self.Q40,self.Q41,self.Q42,self.Q43,self.Q44,self.Q45,self.Q46,self.Q47,self.Q48,self.Q49,
                    self.Q50)


class TileM(db.Model):
    __table__ = db.Model.metadata.tables['tilemetrics']

    def __init__(self, LaneID, TileID, CodeID, MiSeqRunID, Value):
        self.LaneID = LaneID
        self.TileID = TileID
        self.CodeID = CodeID
        self.MiSeqRunID = MiSeqRunID
        self.Value = Value

    def __repr__(self):
        return "<IndexMetricsMiSeqRun(%s,%s,%s,%s,%s)>" \
               % (self.LaneID, self.TileID, self.CodeID, self.MiSeqRunID, self.Value)


## Add a new user
#@app.before_first_request
def create_user():
    user_datastore.create_user(email='matt@notface.net', password='passbags')
    db.session.commit()
    flash('User added')


'''
@socketio.on('disconnect')
def disconnect_user():
    #Disconnects the user when the browser is closed
    #Annoyingly this is now not working as expected
    return logout()
'''

@app.route('/', methods=['GET', 'POST'])
def base_screen():
    #print session #Use to debug log in and log out auto later
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None) #This only pops the most recent session- need to use session.pop('yourkey',None)
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
        if not identifier:  # '150820_M02641_0017_000000000-AGJJA':
                # print 'triggering' #testing that this syntax worked if there was no entry in the query field
            flash('No data entered')
            return redirect(url_for('query_page'))
        else:
            #from models_depr import Msr  # Previously had import * but this gave a warning
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