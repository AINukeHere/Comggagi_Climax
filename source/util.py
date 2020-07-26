from eudplib import *
import Setting
import EntranceAttack
def GetLocOffset(locString):
    return EPD(0x58DC60) + (EncodeLocation(locString) - 1)*5
def ReaverScarabFixing(epd):
    orderID = epd + 0x4D // 4 # byte
    unitType = epd + 0x64 // 4 # dword
    hangarCount = epd + 0xC8 // 4 # byte

    if EUDIf()(EUDSCAnd()
    (MemoryEPD(unitType, Exactly, EncodeUnit("Protoss Reaver"))) # 리버인경우
    (EUDNot(MemoryXEPD(orderID, Exactly, 0x0000, 0xFF00))) # 죽은상태가 아니고
    (EUDNot(MemoryXEPD(orderID, Exactly, 0x1700, 0xFF00))) # 생산중인 상태가 아니고
    ()):
        if EUDIf()(MemoryXEPD(hangarCount, AtLeast, 2, 0xFF)):
            lastScarabPtr = f_dwread_epd(epd + 0xC0 //4)
            if EUDIf()(lastScarabPtr != 0):
                lastScarabEPD = EPD(lastScarabPtr)
                lastScarab_removeTimer = lastScarabEPD + 0x110 // 4
                DoActions(SetMemoryXEPD(lastScarab_removeTimer, SetTo, 0x0001,0xFFFF))
                if Setting._DEBUG:
                    f_simpleprint("removeTimer Set 1", lastScarabPtr, lastScarabEPD, lastScarab_removeTimer)
            EUDEndIf()
        EUDEndIf()
        if EUDIf()(MemoryXEPD(hangarCount, Exactly, 0, 0xFF)):
            reaverPosVal = f_dwread_epd(epd + 0x28 // 4)
            connected_unit = epd + 0x80 // 4
            if EUDIf()(MemoryEPD(connected_unit, Exactly, 0)): # 셔틀엘 탄 상태는 제외
                temp = f_dwbreak(reaverPosVal)
                reaverPosX = temp[0]
                reaverPosY = temp[1]
                locOffset = GetLocOffset("EUDControlLoc")
                if Setting._DEBUG:
                    f_simpleprint('AddhangarCount', reaverPosX-32, reaverPosY-32, reaverPosX+32, reaverPosY+32)
                DoActions([
                    SetMemoryEPD(locOffset, SetTo, reaverPosX-32),
                    SetMemoryEPD(locOffset + 1, SetTo, reaverPosY-32),
                    SetMemoryEPD(locOffset + 2, SetTo, reaverPosX+32),
                    SetMemoryEPD(locOffset + 3, SetTo, reaverPosY+32),
                    ModifyUnitHangarCount(1, All, "Protoss Reaver", P1, "EUDControlLoc"),
                    ModifyUnitHangarCount(1, All, "Protoss Reaver", P2, "EUDControlLoc"),
                    ModifyUnitHangarCount(1, All, "Protoss Reaver", P3, "EUDControlLoc"),
                    ModifyUnitHangarCount(1, All, "Protoss Reaver", P7, "EUDControlLoc")
                ])
                if Setting._DEBUG:
                    SetCurrentPlayer(0)
                    DoActions([
                        MinimapPing("EUDControlLoc"),
                        CreateUnit(1, "Terran Wraith", "EUDControlLoc", P7),
                        KillUnit("Terran Wraith", P7)
                    ])
            EUDEndIf()
        EUDEndIf()
    EUDEndIf()

IRRADIATE_AIR_UNIT_MAX = 200
IRRADIATE_LARVA_MAX = 300
irradiateOutUnits_airUnit = EUDArray(IRRADIATE_AIR_UNIT_MAX)
irradiateOutUnits_larva = EUDArray(IRRADIATE_LARVA_MAX)
def IrradiateOut_OnNewUnitLoop(epd):
    global irradiateOutUnits_larva
    playerID = epd + 0x4C // 4
    unitType = epd + 0x64 // 4
    if EUDIf()(EUDSCAnd()
    (MemoryXEPD(playerID, Exactly, 7, 0xFF)) # 8p이고
    (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Larva"))) # Zerg Larva이면
    ()):
        for i in EUDLoopRange(0, IRRADIATE_LARVA_MAX):
            if EUDIf()(irradiateOutUnits_larva[i] == 0):
                irradiateOutUnits_larva[i] = epd
                EUDBreak()
            EUDEndIf()
    EUDEndIf()
def IrradiateOut_Update():
    global irradiateOutUnits_airUnit, irradiateOutUnits_larva
    epd = EUDVariable(0)
    for i in EUDLoopRange(0, IRRADIATE_LARVA_MAX):
        if EUDIf()(irradiateOutUnits_larva[i] != 0):
            epd << irradiateOutUnits_larva[i]

            # 죽은 라바면 배열에서 제외
            orderID = epd + 0x4D // 4
            if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0xFF00)):
                irradiateOutUnits_larva[i] = 0
                EUDContinue()
            EUDEndIf()

            unitType = epd + 0x64 // 4
            if EUDIf()(EUDSCAnd()
            ((EUDNot(MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Larva")))))
            ((EUDNot(MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Egg")))))
            ()):
                irradiateOutUnits_larva[i] = 0
                if EUDIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Mutalisk"))): # 뮤탈이면
                    for i in EUDLoopRange(0, IRRADIATE_AIR_UNIT_MAX):
                        if EUDIf()(irradiateOutUnits_airUnit[i] == 0):
                            irradiateOutUnits_airUnit[i] = epd
                            EUDBreak()
                        EUDEndIf()
                if EUDElseIf()(EUDSCOr()
                (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Zergling")))
                (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Hydralisk")))
                ()):
                    EntranceAttack.AddAttacker(epd)
                EUDEndIf()
            EUDEndIf()
        EUDEndIf()




    for i in EUDLoopRange(0, IRRADIATE_AIR_UNIT_MAX):
        if EUDIf()(irradiateOutUnits_airUnit[i] != 0):
            epd << irradiateOutUnits_airUnit[i]
            orderID = epd + 0x4D // 4
            if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0xFF00)): # 죽었으면
                irradiateOutUnits_airUnit[i] = 0
                EUDContinue()
            EUDEndIf()

            irradiateTimer = epd + 0x118 // 4
            if EUDIf()(MemoryXEPD(irradiateTimer, AtLeast, 1, 0xFF)): # 이레데이트가 걸린놈이고
                orderTargetPos = epd+0x5C // 4
                orderTargetPtr = epd+0x58 // 4
                DoActions([
                    SetMemoryXEPD(orderID, SetTo, 0x0600, 0xFF00),
                    SetMemoryEPD(orderTargetPos,SetTo,0),
                    SetMemoryEPD(orderTargetPtr,SetTo,0)
                ])
            EUDEndIf()
        EUDEndIf()
def IrradiateOut(epd):
    playerID = epd + 0x4C // 4
    irradiateTimer = epd + 0x118 // 4
    orderID = epd + 0x4D // 4
    if EUDIf()(EUDSCAnd()
    (MemoryXEPD(irradiateTimer, AtLeast, 1, 0xFF)) # 이레데이트가 걸린놈이고
    (MemoryXEPD(playerID, Exactly, 7, 0xFF)) # 8p이고
    (EUDNot(MemoryXEPD(orderID, Exactly, 0, 0xFF00))) # 죽는놈은 아니고
    ()):
        orderTargetPos = epd+0x5C // 4
        orderTargetPtr = epd+0x58 // 4
        DoActions([
            SetMemoryXEPD(orderID, SetTo, 0x0600, 0xFF00),
            SetMemoryEPD(orderTargetPos,SetTo,0),
            SetMemoryEPD(orderTargetPtr,SetTo,0)
        ])
    EUDEndIf()
initScores = EUDArray(5)
def UpdateResourceUsed():
    global initScores
    curMineral = EPD(0x57F0F0)
    curGas = EPD(0x57F120)
    allMiningMineral = EPD(0x57F180)
    allMiningGas = EPD(0x57F150)
    if EUDIf()(initScores[4] == 0): # 초기자원 = 현재 미네랄 + 현재 가스
        initScores[0] << f_dwread_epd(curMineral+0) + f_dwread_epd(curGas+0)
        initScores[1] << f_dwread_epd(curMineral+1) + f_dwread_epd(curGas+1)
        initScores[2] << f_dwread_epd(curMineral+2) + f_dwread_epd(curGas+2)
        initScores[3] << f_dwread_epd(curMineral+6) + f_dwread_epd(curGas+6)
        initScores[4] << f_dwread_epd(curMineral+7) + f_dwread_epd(curGas+7)
    EUDEndIf()
    # Score = 초기자원 + 총 채취 미네랄 + 총 채취 가스 - 현재 미네랄 - 현재 가스
    P1Score = initScores[0] + f_dwread_epd(allMiningMineral+0) + f_dwread_epd(allMiningGas+0)- (f_dwread_epd(curMineral+0) + f_dwread_epd(curGas+0))
    P2Score = initScores[1] + f_dwread_epd(allMiningMineral+1) + f_dwread_epd(allMiningGas+1)- (f_dwread_epd(curMineral+1) + f_dwread_epd(curGas+1))
    P3Score = initScores[2] + f_dwread_epd(allMiningMineral+2) + f_dwread_epd(allMiningGas+2)- (f_dwread_epd(curMineral+2) + f_dwread_epd(curGas+2))
    P7Score = initScores[3] + f_dwread_epd(allMiningMineral+6) + f_dwread_epd(allMiningGas+6)- (f_dwread_epd(curMineral+6) + f_dwread_epd(curGas+6))
    P8Score = initScores[4] + f_dwread_epd(allMiningMineral+7) + f_dwread_epd(allMiningGas+7)- (f_dwread_epd(curMineral+7) + f_dwread_epd(curGas+7))
    DoActions([
        SetScore(P1, SetTo, P1Score, Custom),
        SetScore(P2, SetTo, P2Score, Custom),
        SetScore(P3, SetTo, P3Score, Custom),
        SetScore(P7, SetTo, P7Score, Custom),
        SetScore(P8, SetTo, P8Score, Custom)
    ])

recallDropTargetResetTime = EUDVariable(0)
def LocationResizing():
    global recallDropTargetResetTime
    ### 20 Overlord ###
    locOffset_Only20Overlord = GetLocOffset("Only20Overlord")
    overlordNum = 20
    if EUDIf()(Bring(P8, AtLeast, overlordNum+1, "Zerg Overlord", "Only20Overlord")):
        if EUDIf()(MemoryEPD(locOffset_Only20Overlord+2, AtLeast, 2144 + 32)):
            DoActions(SetMemoryEPD(locOffset_Only20Overlord + 2, Subtract, 32)) # xmax 를 한칸 줄임
        EUDEndIf()
    if EUDElseIf()(Bring(P8, AtMost, overlordNum - 1, "Zerg Overlord", "Only20Overlord")):
        if EUDIf()(MemoryEPD(locOffset_Only20Overlord+2, AtMost, 4096 - 32)):
            DoActions(SetMemoryEPD(locOffset_Only20Overlord + 2, Add, 32)) # xmax 를 한칸 늘림
        EUDEndIf()
    EUDEndIf()
    ### 20 Overlord ###


    ###RecallDropTarget###
    recallDropTargetResetTime += 1
    if EUDIf()(EUDSCAnd()
    (Switch("ZergOverlordDrop",Cleared))
    #(Switch("ProtossRecallTerror",Cleared))
    ()):
        locOffset_RecallDropTarget = GetLocOffset("RecallDropTarget")
        if EUDIf()(recallDropTargetResetTime > 720):
            recallDropTargetResetTime << 0
            DoActions([
                SetSwitch("RecallDropTargetRandom1",Random),
                SetSwitch("RecallDropTargetRandom2",Random)
            ])
            if EUDIf()(EUDSCAnd()
            (Switch("RecallDropTargetRandom1",Cleared))
            (Switch("RecallDropTargetRandom2",Cleared))
            ()):
                DoActions(MoveLocation("RecallDropTarget", "Xel'Naga Temple",P7,"1p"))
            if EUDElseIf()(EUDSCAnd()
            (Switch("RecallDropTargetRandom1",Cleared))
            (Switch("RecallDropTargetRandom2",Set))
            ()):
                DoActions(MoveLocation("RecallDropTarget", "Xel'Naga Temple",P7,"2pLeft"))
            if EUDElseIf()(EUDSCAnd()
            (Switch("RecallDropTargetRandom1",Set))
            (Switch("RecallDropTargetRandom2",Cleared))
            ()):
                DoActions(MoveLocation("RecallDropTarget", "Xel'Naga Temple",P7,"2pRight"))
            if EUDElse()():
                DoActions(MoveLocation("RecallDropTarget", "Xel'Naga Temple",P7,"3p"))
            EUDEndIf()
        EUDEndIf()
        if EUDIf()(Bring(Force1, AtMost, 4, "Buildings", "RecallDropTarget")):
            if EUDIf()(Switch("RecallDropTargetMoveDir", Cleared)):
                if EUDIf()(MemoryEPD(locOffset_RecallDropTarget + 2, AtMost, 4096 - 32)):
                    DoActions([
                        SetMemoryEPD(locOffset_RecallDropTarget, Add, 32),
                        SetMemoryEPD(locOffset_RecallDropTarget+2, Add, 32)
                    ])
                if EUDElse()():
                    DoActions(SetSwitch("RecallDropTargetMoveDir",Toggle))
                EUDEndIf()
            if EUDElse()():
                if EUDIf()(MemoryEPD(locOffset_RecallDropTarget, AtLeast, 0 + 32)):
                    DoActions([
                        SetMemoryEPD(locOffset_RecallDropTarget, Subtract, 32),
                        SetMemoryEPD(locOffset_RecallDropTarget+2, Subtract, 32)
                    ])
                if EUDElse()():
                    DoActions(SetSwitch("RecallDropTargetMoveDir",Toggle))
                EUDEndIf()
            EUDEndIf()
        EUDEndIf()
    EUDEndIf()
    ###RecallDropTarget###

    ###OverlordGatheringPoints###
    locOffset_OverlordGatheringPoint1 = GetLocOffset("OverlordGatheringPoint1")
    locOffset_OverlordGatheringPoint2 = GetLocOffset("OverlordGatheringPoint2")
    targetPosXmin = f_dwread_epd(locOffset_RecallDropTarget)
    gatheringPoint_X2 = targetPosXmin + 416
    DoActions([
        SetMemoryEPD(locOffset_OverlordGatheringPoint1, SetTo, targetPosXmin),
        SetMemoryEPD(locOffset_OverlordGatheringPoint1+2, SetTo, gatheringPoint_X2),
        SetMemoryEPD(locOffset_OverlordGatheringPoint2, SetTo, targetPosXmin),
        SetMemoryEPD(locOffset_OverlordGatheringPoint2+2, SetTo, gatheringPoint_X2)
    ])
    ###OverlordGatheringPoints###


    ###ArbiterPathFindingLocations###
    locOffset_ArbiterPathFindingLeft = GetLocOffset("ArbiterPathFindingLeft")
    locOffset_ArbiterPathFindingCenter = GetLocOffset("ArbiterPathFindingCenter")
    locOffset_ArbiterPathFindingRight = GetLocOffset("ArbiterPathFindingRight")
    locOffset_ArbiterLoc = GetLocOffset("ArbiterLoc")
    targetPosCenterX = targetPosXmin + 208
    targetPosYmin = f_dwread_epd(locOffset_RecallDropTarget + 1)
    targetPosCenterY = targetPosYmin + 224
    curArbiterXmin = f_dwread_epd(locOffset_ArbiterLoc)
    curArbiterCenterX = curArbiterXmin + 160
    curArbiterYmin = f_dwread_epd(locOffset_ArbiterLoc + 1)
    curArbiterCenterY = curArbiterYmin + 160
    distX,distY,centerSensorX = EUDCreateVariables(3)
    distY << curArbiterCenterY - targetPosCenterY
    if EUDIf()(curArbiterCenterX < targetPosCenterX):
        distX << targetPosCenterX - curArbiterCenterX
        centerSensorX << curArbiterCenterX + (320*distX) // distY
    if EUDElse()():
        distX << curArbiterCenterX - targetPosCenterX
        centerSensorX << curArbiterCenterX - (320*distX) // distY
    EUDEndIf()
    DoActions([
        SetMemoryEPD(locOffset_ArbiterPathFindingCenter,SetTo,centerSensorX-160),
        SetMemoryEPD(locOffset_ArbiterPathFindingCenter+1,SetTo,curArbiterYmin-320),
        SetMemoryEPD(locOffset_ArbiterPathFindingCenter+2,SetTo,centerSensorX+160),
        SetMemoryEPD(locOffset_ArbiterPathFindingCenter+3,SetTo,curArbiterYmin),

        SetMemoryEPD(locOffset_ArbiterPathFindingLeft,SetTo,centerSensorX-480),
        SetMemoryEPD(locOffset_ArbiterPathFindingLeft+1,SetTo,curArbiterYmin-320),
        SetMemoryEPD(locOffset_ArbiterPathFindingLeft+2,SetTo,centerSensorX-160),
        SetMemoryEPD(locOffset_ArbiterPathFindingLeft+3,SetTo,curArbiterYmin),

        SetMemoryEPD(locOffset_ArbiterPathFindingRight,SetTo,centerSensorX+160),
        SetMemoryEPD(locOffset_ArbiterPathFindingRight+1,SetTo,curArbiterYmin-320),
        SetMemoryEPD(locOffset_ArbiterPathFindingRight+2,SetTo,centerSensorX+480),
        SetMemoryEPD(locOffset_ArbiterPathFindingRight+3,SetTo,curArbiterYmin),
    ])


    DoActions([
        MoveLocation("ArbiterSmallLoc","Terran Marker", P12, "ArbiterLoc"),
        MoveLocation("FollowArbiterOnlyGround","Terran Marker", P12, "FollowArbiter"),
        MoveLocation("FollowArbiter","Protoss Arbiter", P7, "FollowArbiter"),
    ])
    ###ArbiterPathFindingLocations###


    ### Detect Enemy Arbiter ###
    DoActions([
        MoveLocation("EnemyArbiter","Protoss Arbiter", Force1, "EnemyArbiterDetectArea"),
        MoveLocation("EnemyArbiterGround","Terran Marker", P12, "EnemyArbiter")
    ])
    if EUDIf()(EUDSCAnd()
    (Bring(Force1, AtLeast, 1, "Protoss Arbiter","EnemyArbiter"))
    (Bring(Force1, AtMost, 0, "Men","EnemyArbiterGround"))
    ()):
        locOffset_EnemyArbiter = GetLocOffset("EnemyArbiter")
        enemyArbiterLeft = f_dwread_epd(locOffset_EnemyArbiter) # x1(left)
        enemyArbiterRight = f_dwread_epd(locOffset_EnemyArbiter + 2) # x2(right)
        locOffset_DefenseRecallTerror = GetLocOffset("DefenseRecallTerror")
        DoActions([
            SetMemoryEPD(locOffset_DefenseRecallTerror, SetTo, enemyArbiterLeft),
            SetMemoryEPD(locOffset_DefenseRecallTerror + 2, SetTo, enemyArbiterRight),
        ])
    EUDEndIf()
    ### Detect Enemy Arbiter ###

    # Location Visualize
    DoActions([
        # CreateUnit(1, "Zerg Mutalisk", "Only20Overlord", P7),
        # KillUnit("Zerg Mutalisk", P7),
        # CreateUnit(1, "Zerg Mutalisk", "RecallDropTarget", P7),
        # KillUnit("Zerg Mutalisk", P7),
        # CreateUnit(1, "Zerg Guardian", "OverlordGatheringPoint1", P7),
        # KillUnit("Zerg Guardian", P7),
        # CreateUnit(1, "Zerg Devourer", "OverlordGatheringPoint2", P7),
        # KillUnit("Zerg Devourer", P7),
        # CreateUnit(1, "Zerg Scourge", "FollowOverlord", P7),
        # KillUnit("Zerg Scourge", P7),
        # CreateUnit(1, "Zerg Overlord", "ArbiterLoc", P7),
        # KillUnit("Zerg Overlord", P7),
        # CreateUnit(1, "Zerg Overlord", "ArbiterPathFindingLeft", P7),
        # KillUnit("Zerg Overlord", P7),
        # CreateUnit(1, "Zerg Overlord", "ArbiterPathFindingCenter", P7),
        # KillUnit("Zerg Overlord", P7),
        # CreateUnit(1, "Zerg Overlord", "ArbiterPathFindingRight", P7),
        # KillUnit("Zerg Overlord", P7),
        # CreateUnit(1, "Zerg Overlord", "EnemyArbiter", P7),
        # KillUnit("Zerg Overlord", P7),
        # CreateUnit(1, "Zerg Mutalisk", "DefenseRecallTerror", P7),
        # KillUnit("Zerg Mutalisk", P7),
    ])




def CUnit(idx):
    if idx == 0:
        return 0x59CCA8
    else:
        return 0x628298 - 0x150*(idx-1)
def ShowSupplies():
    suppliesTimer = EUDVariable(0)
    suppliesTimer += 1
    if EUDIf()(suppliesTimer == 48):
        suppliesTimer << 0
        f_simpleprint('P7 use(P)',f_dwread_epd(EPD(0x00582294) + 6))
        f_simpleprint('P7 use(T)',f_dwread_epd(EPD(0x00582204) + 6))
        f_simpleprint('P8 use(Z)',f_dwread_epd(EPD(0x00582174) + 7))
    EUDEndIf()