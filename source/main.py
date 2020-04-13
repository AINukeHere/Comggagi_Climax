from eudplib import *
from GiveMeSCV import *
import util
from AttackThis import AttackThisArea
import Setting
import TerranBuild
import eudplib

# import TileManager
# import JobManager
# import unitLoop
# import BuildingInfo

# TileManager.init()
# p1_spX = None
# p1_spY = None


group = EUDVariable(0)
entrance = EUDVariable(0)
def onPluginStart():
    # DoActions([
    #     CreateUnit(1, "Terran Civilian", "GiveMeSCV_Destination", P8),
    #     Order("Terran Civilian", P8, "Anywhere", Move, "Anywhere"),
    #     # 시민의 생산크기 0 0 설정
    #     SetMemory(0x66289C, SetTo, 0),
    # ])
    global group, entrance
    entrance = AttackThisArea.alloc(2,3)
    entrance.addAttackPlayer(6)
    entrance.addAttackPlayer(7)
    entrance.addTargetPlayer(0)
    entrance.addTargetPlayer(1)
    entrance.addTargetPlayer(2)
    entrance.SetArea(EncodeLocation('EntranceLoc1') - 1)
    group = StrategyGroup.alloc()
    
    f_randomize()
    TerranAvailable = EPD(0x005821D4)
    TerranMax = EPD(0x00582234)
    ZergAvailable = EPD(0x00582144)
    ZergMax = EPD(0x005821A4)
    ProtossAvailable = EPD(0x00582264)
    ProtossMax = EPD(0x005822C4)
    DoActions([
        #인구수
        SetMemoryEPD(TerranAvailable     + 0, SetTo, 400), # P1 Terran Available
        SetMemoryEPD(TerranMax           + 0, SetTo, 400), # P1 Terran Max
        SetMemoryEPD(ZergAvailable       + 0, SetTo, 400), # P1 Zerg Available
        SetMemoryEPD(ZergMax             + 0, SetTo, 400), # P1 Zerg Max
        SetMemoryEPD(ProtossAvailable    + 0, SetTo, 400), # P1 Protoss Available
        SetMemoryEPD(ProtossMax          + 0, SetTo, 400), # P1 Protoss Max
        SetMemoryEPD(TerranAvailable     + 1, SetTo, 400), # P2 Terran Available
        SetMemoryEPD(TerranMax           + 1, SetTo, 400), # P2 Terran Max
        SetMemoryEPD(ZergAvailable       + 1, SetTo, 400), # P2 Zerg Available
        SetMemoryEPD(ZergMax             + 1, SetTo, 400), # P2 Zerg Max
        SetMemoryEPD(ProtossAvailable    + 1, SetTo, 400), # P2 Protoss Available
        SetMemoryEPD(ProtossMax          + 1, SetTo, 400), # P2 Protoss Max
        SetMemoryEPD(TerranAvailable     + 2, SetTo, 400), # P3 Terran Available
        SetMemoryEPD(TerranMax           + 2, SetTo, 400), # P3 Terran Max
        SetMemoryEPD(ZergAvailable       + 2, SetTo, 400), # P3 Zerg Available
        SetMemoryEPD(ZergMax             + 2, SetTo, 400), # P3 Zerg Max
        SetMemoryEPD(ProtossAvailable    + 2, SetTo, 400), # P3 Protoss Available
        SetMemoryEPD(ProtossMax          + 2, SetTo, 400), # P3 Protoss Max
        #컴퓨터
        SetMemoryEPD(TerranAvailable     + 6, SetTo, 600), # P7 Terran Available
        SetMemoryEPD(TerranMax           + 6, SetTo, 600), # P7 Terran Max
        SetMemoryEPD(ZergAvailable       + 6, SetTo, 600), # P7 Zerg Available
        SetMemoryEPD(ZergMax             + 6, SetTo, 600), # P7 Zerg Max
        SetMemoryEPD(ProtossAvailable    + 6, SetTo, 600), # P7 Protoss Available
        SetMemoryEPD(ProtossMax          + 6, SetTo, 600), # P7 Protoss Max
        SetMemoryEPD(TerranAvailable     + 7, SetTo, 600), # P8 Terran Available
        SetMemoryEPD(TerranMax           + 7, SetTo, 600), # P8 Terran Max
        SetMemoryEPD(ZergAvailable       + 7, SetTo, 600), # P8 Zerg Available
        SetMemoryEPD(ZergMax             + 7, SetTo, 600), # P8 Zerg Max
        SetMemoryEPD(ProtossAvailable    + 7, SetTo, 600), # P8 Protoss Available
        SetMemoryEPD(ProtossMax          + 7, SetTo, 600), # P8 Protoss Max
    ])

def CUnit(idx):
    if idx == 0:
        return 0x59CCA8
    else:
        return 0x628298 - 0x150*(idx-1)
def beforeTriggerExec():    
    global group, entrance

    # GiveMeSCV 시작할 지 결정
    flag = EUDVariable(0)
    if EUDIf()(EUDSCAnd()
        (ElapsedTime(AtLeast, 5))
        (flag == 0)
        ()):
        flag << 1
        if EUDIf()(Command(AllPlayers, AtLeast, 1, "Terran SCV")):
            group.groupState = GROUP_STATE_0FIND_MEMBER
        if EUDElse()():
            DoActions(CreateUnit(1, "Ragnasaur (Ashworld Critter)", "7pBase", P7))
        EUDEndIf()
    EUDEndIf()

    ### UnitLoop ###
    group.beforeUnitLoop() # SCV 가져오는 그룹
    entrance.beforeUnitLoop() # 입구건물때리기
    TerranBuild.beforeUnitLoop() # 테란하자
    if EUDIf()(EUDSCAnd()
    (ElapsedTime(AtMost, 450))
    #(Bring(Force1, AtMost, 0, "Any unit", "EntranceLoc1"))
    (Bring(Force1, AtMost, 0, "Men", "EntranceLoc1"))
    ()):
        for ptr,epd in EUDLoopUnit():
            util.ReaverScarabFixing(epd) # 스캐럽 1개로 고정
            util.IrradiateOut(epd) # 이레디 맞은 유닛 빼기
            group.UnitLoopUpdate(ptr, epd)
            entrance.onUnitLoop(ptr, epd)
            TerranBuild.onUnitLoop(epd)
    if EUDElse()():
        for ptr,epd in EUDLoopUnit():
            util.ReaverScarabFixing(epd) # 스캐럽 1개로 고정
            util.IrradiateOut(epd) # 이레디 맞은 유닛 빼기
            group.UnitLoopUpdate(ptr, epd)
            #entrance.onUnitLoop(ptr, epd)
            TerranBuild.onUnitLoop(epd)
    EUDEndIf()
    group.afterUnitLoop()
    TerranBuild.afterUnitLoop()
    if EUDIf()(Deaths(P7, Exactly, 1, "Time 3")):
        entrance.changeRandomTarget()
        #f_simpleprint("random target set")
    EUDEndIf()
    if Setting.ENTRANCE_ATTACKER_PRINT:
        f_simpleprint("attacker : ", entrance.currentFrameTargetInfo[2])
        entrance.currentFrameTargetInfo[2] = 0
    ### UnitLoop ###

    #util.ShowSupplies() # 인구수 출력
    util.LocationResizing() # 각종 로케이션 위치갱신

leaderboardTime = EUDVariable(0)
def afterTriggerExec():
    global leaderboardTime
    leaderboardTime += 1
    if EUDIf()(leaderboardTime == 24):
        leaderboardTime << 0
        util.UpdateResourceUsed()
    EUDEndIf()