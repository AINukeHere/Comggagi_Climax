from eudplib import *
import TileManager
from Job import *
import math
JOB_MAX = 50
#jobPool = ObjPool(JOB_MAX,CJob)
jobs = EUDArray(JOB_MAX)
jobIndex = EUDVariable()

def init():
    for i in EUDLoopRange(0,JOB_MAX):
        jobs[i] = CJob.alloc(0,0,0,0,JOB_STATE_EMPTY)
@EUDFunc
def CreateJob(buildType, searchStartPosX, searchStartPosY, playerID):
    global jobIndex
    buildPosX,buildPosY = TileManager.GetBuildPosition(buildType, searchStartPosX, searchStartPosY, 10)
    if EUDIf()(EUDSCOr()
    (buildPosX == -1)
    (buildPosY == -1)
    ()):
        EUDReturn()
    EUDEndIf()
    for i in EUDLoopRange(0,JOB_MAX):
        if EUDIf()(CJob.cast(jobs[i]).jobState == JOB_STATE_EMPTY):
            #f_simpleprint('find empty job index : ', i)
            CJob.cast(jobs[i]).updateJobInfo(EPD(0x59CCA8), buildType, buildPosX, buildPosY, playerID)
            EUDReturn()
        EUDEndIf()
    f_simpleprint('cannot found empty job')

def Update():
    for i in EUDLoopRange(0,JOB_MAX):
        CJob.cast(jobs[i]).update()

def OnUnitLooping(unitEPD):
    unitTypeEPD = unitEPD + 0x64 // 4
    if EUDIf()(MemoryEPD(unitTypeEPD,Exactly,EncodeUnit("Terran SCV"))):
        orderIDEPD = unitEPD + 0x4D // 4
        orderID = f_bread_epd(orderIDEPD,0x4D%4)
        assignedJobIndex = unitEPD + 0xE8 // 4
        #f_simpleprint(unitEPD, '0xE8 : ',f_dwread_epd(assignedJobIndex))
        if EUDIf()(orderID == 150):
            DoActions(SetMemoryEPD(assignedJobIndex,SetTo, -1))
            #f_simpleprint('assignedJobIndex reset')
        EUDEndIf()
        # Job이 배정되지 않은 모든 SCV에 대해 거리계산
        if EUDIf()(MemoryEPD(assignedJobIndex,Exactly,-1)):
            unitPosX_EPD = unitEPD + 0x28 //4
            unitPosY_EPD = unitEPD + 0x2A //4
            playerID_EPD = unitEPD + 0x4C // 4
            unitPosX = f_wread_epd(unitPosX_EPD, 0)
            unitPosY = f_wread_epd(unitPosY_EPD, 2)
            vecX,vecY = EUDCreateVariables(2)
            for i in EUDLoopRange(0,JOB_MAX):
                curJob = CJob.cast(jobs[i])
                f_simpleprint(curJob.jobState,curJob.playerID,f_bread_epd(playerID_EPD,0x4C % 4))
                if EUDIf()(EUDSCAnd()
                (curJob.jobState == JOB_STATE_FIND_SCV)
                (MemoryXEPD(playerID_EPD,Exactly,curJob.playerID,0xFF))
                ()):
                    vecX << curJob.buildPosX - unitPosX
                    vecY << curJob.buildPosY - unitPosY
                    curDist = f_sqrt(vecX*vecX+vecY*vecY)
                    if EUDIf()(curJob.minDist >= curDist):
                        curJob.minDist = curDist
                        curJob.builderEPD = unitEPD
                    EUDEndIf()
                EUDEndIf()
        EUDEndIf()
    EUDEndIf()
def OnUnitLoopEnd():
    for i in EUDLoopRange(0,JOB_MAX):
        curJob = CJob.cast(jobs[i])
        EUDContinueIfNot(curJob.jobState == JOB_STATE_FIND_SCV)
        assignedJobIndex = curJob.builderEPD + 0xE8 // 4
        # 작업이 배정되지 않은 경우
        #f_simpleprint(curJob.builderEPD, ' : ', f_dwread_epd(assignedJobIndex))
        if EUDIf()(MemoryEPD(assignedJobIndex, Exactly, -1)):
            # 현재작업으로 배정
            DoActions(SetMemoryEPD(assignedJobIndex, SetTo, i))
            curJob.jobState = JOB_STATE_BUILD
            #f_simpleprint('jobs[',i,'].jobState = JOB_STATE_BUILD')
        if EUDElse()():
            curJob.minDist = 0x7FFFFFFF
        EUDEndIf()


def GetJobCount():
    count = EUDVariable(0)
    count << 0
    for i in EUDLoopRange(0, JOB_MAX):
        curJob = CJob.cast(jobs[i])
        if EUDIf()(curJob.jobState != JOB_STATE_EMPTY):
            count += 1
        EUDEndIf()
    return count