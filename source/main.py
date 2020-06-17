from eudplib import *
from GiveMeSCV import *
import util
import Setting
import TerranBuild
import DefenseSystem
import FxingReaverScarab
group = EUDVariable(0)
def onPluginStart():
    if Setting.CHEAT_DEBUG:
        DoActions([
            CreateUnit(1, "Terran Civilian", "CheatBeaconMove", P4),
            SetInvincibility(Enable, "Terran Civilian", P4, "Anywhere"),
            CreateUnit(1, "Terran Beacon", "CheatBeacon", P4),
            # 시민의 생산크기 0 0 설정
            #SetMemory(0x66289C, SetTo, 0),
        ])
    global group
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

def beforeTriggerExec():    
    global group

    # GiveMeSCV 시작할 지 결정
    flag = EUDVariable(0)
    if EUDIf()(EUDSCAnd()
        (ElapsedTime(AtLeast, 5))
        (flag == 0)
        ()):
        
        if EUDIf()(Command(AllPlayers, AtLeast, 1, "Terran SCV")):
            group.groupState = GROUP_STATE_0FIND_MEMBER
            flag << 1
        if EUDElse()():
            DoActions(CreateUnit(1, "Ragnasaur (Ashworld Critter)", "7pBase", P7))
            flag << 2
        EUDEndIf()
    EUDEndIf()

    ### NewUnitLoop ###
    for ptr,epd in LoopNewUnit():
        FxingReaverScarab.onNewUnitLoop(epd)
        util.IrradiateOut_OnNewUnitLoop(epd)
        TerranBuild.onNewUnitLoop(epd) # 테란건물짓기
    FxingReaverScarab.beforeTriggerExec() # 스캐럽 1개로 고정
    util.IrradiateOut_Update() # 이레디 맞은 유닛 빼기

    ### UnitLoop ###
    if EUDIf()(flag == 1):
        TerranBuild.Update() # 테란건물짓기
        group.beforeUnitLoop() # SCV 가져오는 그룹
        if EUDIf()(EUDSCOr()
        (group.groupState == GROUP_STATE_0FIND_MEMBER)
        (group.groupState == GROUP_STATE_2FIND_SCV)
        ()):
            for ptr,epd in EUDLoopUnit():
                group.UnitLoopUpdate(ptr, epd)
        EUDEndIf()
        group.afterUnitLoop()
    EUDEndIf()
    

    util.LocationResizing() # 각종 로케이션 위치갱신
    DefenseSystem.detectTimingRush() # 적 병력 움직임 체크

    #######################################
    ###           DEBUG CODE            ###
    #######################################
    
    #util.ShowSupplies() # 인구수 출력
    # 클릭한 유닛 정보 표시
    if Setting._DEBUG:
        P1_Select_ptr = f_dwread_epd(EPD(0x6284E8))
        if EUDIf()(P1_Select_ptr != 0):
            select_epd = EPD(P1_Select_ptr)
            orderID = select_epd + 0x4D // 4
            curSpeed1 = select_epd + 0x38 // 4
            curSpeed2 = select_epd + 0x3C // 4
            orderState = select_epd + 0x4E // 4
            movementFlags = select_epd + 0x20 // 4
            f_simpleprint(select_epd, 
                f_bread_epd(orderID, 0x4D % 4), 
                f_bread_epd(orderState, 0x4E % 4), 
                f_bread_epd(movementFlags, 0x20 % 4),
                TerranBuild.idleSCV_epd
                )
        EUDEndIf()
    if Setting.CHEAT_DEBUG:
        bCheatOn = EUDVariable(0)
        if EUDIf()(Bring(P4, AtLeast, 1, "Terran Civilian", "CheatBeacon")):
            cheatFlag = EPD(0x6D5A6C)
            if EUDIf()(bCheatOn == 0):
                bCheatOn << 1
                f_simpleprint("무적이 켜졌습니다.")
                DoActions(SetMemoryXEPD(cheatFlag, SetTo, 0x4, 0x4))
            if EUDElse()():
                bCheatOn << 0
                f_simpleprint("무적이 꺼졌습니다.")
                DoActions(SetMemoryXEPD(cheatFlag, SetTo, 0x0, 0x4))
            EUDEndIf()
            DoActions(MoveUnit(1, "Terran Civilian", P4, "CheatBeacon", "CheatBeaconMove"))
        EUDEndIf()

leaderboardTime = EUDVariable(0)
def afterTriggerExec():
    global leaderboardTime
    leaderboardTime += 1
    if EUDIf()(leaderboardTime == 24):
        leaderboardTime << 0
        util.UpdateResourceUsed()
    EUDEndIf()


newCUnit = EUDArray(1700 * 336)
epd2newCUnit = EPD(newCUnit) - EPD(0x59CCA8)
def LoopNewUnit(allowance=2):
    firstUnitPtr = EPD(0x628430)
    EUDCreateBlock("newunitloop", "newlo")
    tos0 = EUDLightVariable()
    tos0 << 0

    ptr, epd = f_cunitepdread_epd(firstUnitPtr)
    if EUDWhile()(ptr >= 1):
        tos1 = f_bread_epd(epd + 0xA5 // 4, 1)
        global epd2newCUnit
        tos2 = epd + epd2newCUnit
        if EUDIfNot()(MemoryEPD(tos2, Exactly, tos1)):
            DoActions(SetMemoryEPD(tos2, SetTo, tos1))
            yield ptr, epd
        if EUDElse()():
            DoActions(tos0.AddNumber(1))
            EUDBreakIf(tos0.AtLeast(allowance))
        EUDEndIf()
        EUDSetContinuePoint()
        f_cunitepdread_epd(epd + 1, ret=[ptr, epd])
    EUDEndWhile()

    EUDPopBlock("newunitloop")