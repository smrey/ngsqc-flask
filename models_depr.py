from QCFrontSimplest import mysql_db as db

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

    ''' Dunno yet why this differs from __repr__ (although repr demands a string returned)
    def __str__(self):
        return dict([('MiSeqRunID',self.MiSeqRunID),('RunStartDate',self.RunStartDate),('RunNumber',self.RunNumber),
                     ('Instrument',self.Instrument)])
    '''

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


    '''
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    email = mysql_db.Column(mysql_db.String(255), unique=True)
    password = mysql_db.Column(mysql_db.String(255))
    active = mysql_db.Column(mysql_db.Boolean())
    confirmed_at = mysql_db.Column(mysql_db.DateTime())
    roles = mysql_db.relationship('Role', secondary=roles_users,
                                  backref=mysql_db.backref('users', lazy='dynamic'))
    '''

class RolesUsers(db.Model):
    __table__ = db.Model.metadata.tables['rolesusers']

    def __init__(self, rolesusersid ,userid, roleid):
        self.rolesusersid = rolesusersid
        self.userid = userid
        self.roleid = roleid

    def __repr__(self):
        return "<RolesUsers(%s,%s,%s)>" \
               % (self.rolesusersid, self.userid, self.roleid)

class Role(db.Model, RoleMixin):
    __table__ = db.Model.metadata.tables['role']

    def __init__(self, name, description):
        #self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Role(%s,%s,%s)>" \
                % (self.id, self.name, self.description)

class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['user']

    def __init__(self, email, password, active, confirmed_at):
        #self.id = id
        self.email = email
        self.password = password
        self.active = active
        self.confirmed_at = confirmed_at

    def __repr__(self):
        return "<User(%s,%s,%s,%s,%s)>" \
                % (self.id, self.email, self.password, self.active, self.confirmed_at)


__table_args__ = {"useexisting": True}