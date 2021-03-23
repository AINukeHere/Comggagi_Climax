from eudplib import *

import TileManager

JOB_STATE_EMPTY = 0 # 작업이 끝나서 비어있는 상태.
JOB_STATE_FIND_SCV = 1 # 건물건설요청을 받아 건설할 SCV를 찾는 상태
JOB_STATE_BUILD = 2 # 건설할SCV가 정해져 건물을 지으러가는 상태
class CJob(EUDStruct):
    _fields_ = [
        'builderEPD',
        'buildType',
        'buildPosX',
        'buildPosY',
        'jobState',
        'minDist',
        'playerID',
    ]
    # def __init__(self, builderEPD, buildType):
    #     if isinstance(builderEPD, int):
    #         super().__init__([
    #             builderEPD,buildType
    #         ])
    #     else:
    #         super().__init__(builderEPD)
    def constructor(self, builderEPD, buildType, buildPosX, buildPosY, jobState):
        self.builderEPD = builderEPD
        self.buildType = buildType
        self.buildPosX = buildPosX
        self.buildPosY = buildPosY
        self.jobState = jobState
        self.playerID = 6
        self.minDist = 0x7FFFFFFF
        #f_simpleprint('Created Job',builderEPD,buildType,buildPosX,buildPosY,self.jobState)
    @EUDMethod
    def updateJobInfo(self, builderEPD, buildType, buildPosX, buildPosY, playerID):
        self.builderEPD = builderEPD
        self.buildType = buildType
        self.buildPosX = buildPosX
        self.buildPosY = buildPosY
        self.jobState = JOB_STATE_FIND_SCV
        self.playerID = playerID
        self.minDist = 0x7FFFFFFF
        TileManager.requestBuildArea(buildType,buildPosX,buildPosY, True)
        #f_simpleprint('Updated Job',builderEPD, buildType, buildPosX, buildPosY)
    @EUDMethod
    def update(self):
        EUDSwitch(self.jobState)
        if EUDSwitchCase()(JOB_STATE_EMPTY):
            EUDReturn()
        if EUDSwitchCase()(JOB_STATE_FIND_SCV):
            EUDBreak()
        if EUDSwitchCase()(JOB_STATE_BUILD):
            if EUDIf()(self.jobState != 0):
                orderID = self.builderEPD + 0x4D // 4
                unitPosX_EPD = self.builderEPD + 0x28 //4
                unitPosY_EPD = self.builderEPD + 0x2A //4
                orderIDValue = f_bread_epd(orderID, 0x4D % 4)
                #f_simpleprint(unitPosX,unitPosY,orderIDValue)
                # orderID가 Stop인경우
                if EUDIf()(EUDSCOr()
                (orderIDValue == 3) # 사람전용 Stop
                (MemoryXEPD(orderID, Exactly, 0x9A00, 0xFF00)) # 컴퓨터전용 Stop
                (MemoryXEPD(orderID, Exactly, 0x5500, 0xFF00)) # 미네랄캐기
                ()):
                    #f_simpleprint('go work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    DoActions([
                        SetMemoryEPD(self.builderEPD+0x58 // 4, SetTo, self.buildPosX + self.buildPosY*65536),
                        SetMemoryEPD(self.builderEPD+0x98 // 4, SetTo, 14942208 + self.buildType),
                        SetMemoryEPD(self.builderEPD+0x4C // 4, SetTo, self.playerID + 30*256),
                    ])
                EUDEndIf()
                
                if EUDIf()(EUDSCOr()
                    (orderIDValue == 33) # SCV의 orderID가 isBuilding(SCV)인 경우
                    (orderIDValue == 0) # SCV의 orderID가 0인경우 (파괴된 경우)
                    ()):
                    f_simpleprint('Job Finished')
                    self.jobState = JOB_STATE_EMPTY
                    TileManager.requestBuildArea(self.buildType,self.buildPosX,self.buildPosY,False)
                EUDEndIf()
            EUDEndIf()
            EUDBreak()
        if EUDSwitchDefault()():
            f_simpleprint('warning! unknown jobState', self.jobState)
            EUDBreak()
        EUDEndSwitch()
        