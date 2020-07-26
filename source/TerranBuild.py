from eudplib import *
import Setting
import util

SCV_ready = EUDVariable(0)
SCV_MAX = 20
scv_array = EUDArray(SCV_MAX)
idleSCV_epd = EUDVariable(0)
command_epd = EUDVariable(0)
bCommandCenterFinishSend = EUDVariable(0)
bFactoryFinishSend = EUDVariable(0)
bMachineShopFinishSend = EUDVariable(0)
bArmoryFinishSend = EUDVariable(0)
bEngineeringBayFinishSend = EUDVariable(0)
bSCVArrived = EUDVariable(0)
# 지어지고있거나 지어진 각 건물 수
commandCenterNum, barracksNum, factoryNum, armoryNum, starportNum, sciFacilityNum, academyNum, engineeringBayNum = EUDCreateVariables(8)
def BuildCommand(locString, buildingType):
    global idleSCV_epd
    locOffset = util.GetLocOffset(locString)
    if Setting._DEBUG:
        f_simpleprint("build" +locString )
    commandPosX = f_dwread_epd(locOffset)
    commandPosY = f_dwread_epd(locOffset+1)
    DoActions([
        SetMemoryEPD(idleSCV_epd+0x58 // 4, SetTo, commandPosX + commandPosY*65536),
        SetMemoryEPD(idleSCV_epd+0x5C // 4, SetTo, 0),
        SetMemoryEPD(idleSCV_epd+0x98 // 4, SetTo, 14942208 + buildingType),
        SetMemoryEPD(idleSCV_epd+0x4C // 4, SetTo, 6 + 30*256),
    ])
def AutoBuild():
    global SCV_ready, idleSCV_epd
    global bSCVArrived, command_epd
    orderID = idleSCV_epd + 0x4D // 4
    if EUDIf()(EUDSCOr()
    (MemoryXEPD(orderID, Exactly, 0, 0xFF00)) # 죽어버리거나
    #(MemoryXEPD(orderID, Exactly, 30*0x100, 0xFF00)) # 건설하러가거나
    (MemoryXEPD(orderID, Exactly, 33*0x100, 0xFF00)) # 건설중이거나
    (MemoryXEPD(orderID, Exactly, 83*0x100, 0xFF00)) # 가스통에 들어간 상태이거나
    ()):
        SCV_ready << 0
        idleSCV_epd << 0
    EUDEndIf()
    if EUDIf()(SCV_ready):
        if EUDIfNot()(MemoryXEPD(orderID, Exactly, 30*0x100, 0xFF00)):
            if EUDIf()(commandCenterNum == 0):
                if Setting._DEBUG:
                    f_simpleprint("build Command Center")
                BuildCommand("CommandCenter", EncodeUnit("Terran Command Center"))
            if EUDElseIf()(EUDSCAnd()
            (Command(P7, AtLeast, 1, "Terran Command Center"))
            (barracksNum == 0)
            ()):
                if EUDIf()(bCommandCenterFinishSend == 0):
                    bCommandCenterFinishSend << 1
                    DoActions(CreateUnit(1, "Fenix (Dragoon)","7pBase",P7))
                EUDEndIf()
                if Setting._DEBUG:
                    f_simpleprint("build Barracks")
                BuildCommand("Barracks", EncodeUnit("Terran Barracks"))
            if EUDElseIf()(Command(P7, AtLeast, 1, "Terran Barracks")):
                if EUDIf()(factoryNum < 5): # 펙토리를 늘려야 하는 상황
                    if EUDIf()(factoryNum == 0):
                        if Setting._DEBUG:
                            f_simpleprint("build Factory1")
                        BuildCommand("Factory1", EncodeUnit("Terran Factory"))
                    if EUDElseIf()(factoryNum == 1):
                        if Setting._DEBUG:
                            f_simpleprint("build Factory2")
                        BuildCommand("Factory2", EncodeUnit("Terran Factory"))
                    if EUDElseIf()(factoryNum == 2):
                        if Setting._DEBUG:
                            f_simpleprint("build Factory3")
                        BuildCommand("Factory3", EncodeUnit("Terran Factory"))
                    if EUDElseIf()(factoryNum == 3):
                        if Setting._DEBUG:
                            f_simpleprint("build Factory4")
                        BuildCommand("Factory4", EncodeUnit("Terran Factory"))
                    if EUDElseIf()(factoryNum == 4):
                        if Setting._DEBUG:
                            f_simpleprint("build Factory5")
                        BuildCommand("Factory5", EncodeUnit("Terran Factory"))
                    EUDEndIf()
                if EUDElse()():
                    if EUDIf()(Command(P7, AtLeast, 1, "Terran Factory")):
                        if EUDIf()(bFactoryFinishSend == 0):
                            bFactoryFinishSend << 1
                            DoActions(CreateUnit(1, "Artanis (Scout)", "7pBase", P7))
                        EUDEndIf()
                        if EUDIf()(academyNum == 0):
                            if Setting._DEBUG:
                                f_simpleprint("build Academy")
                            BuildCommand("Academy", EncodeUnit("Terran Academy"))
                        EUDEndIf()
                        if EUDIf()(engineeringBayNum == 0):
                            if Setting._DEBUG:
                                f_simpleprint("build Engineering Bay1")
                            BuildCommand("EngineeringBay1", EncodeUnit("Terran Engineering Bay"))
                        if EUDElseIf()(engineeringBayNum == 1):
                            if Setting._DEBUG:
                                f_simpleprint("build Engineering Bay2")
                            BuildCommand("EngineeringBay2", EncodeUnit("Terran Engineering Bay"))
                        EUDEndIf()
                        if EUDIf()(armoryNum == 0):
                            if Setting._DEBUG:
                                f_simpleprint("build Armory1")
                            BuildCommand("Armory1", EncodeUnit("Terran Armory"))
                        if EUDElseIf()(armoryNum == 1):
                            if Setting._DEBUG:
                                f_simpleprint("build Armory2")
                            BuildCommand("Armory2", EncodeUnit("Terran Armory"))
                        EUDEndIf()
                        if EUDIf()(starportNum == 0):
                            if Setting._DEBUG:
                                f_simpleprint("build Starport")
                            BuildCommand("Starport", EncodeUnit("Terran Starport"))
                        EUDEndIf()
                    EUDEndIf()
                    if EUDIf()(EUDSCAnd()
                    (Command(P7, AtLeast, 1, "Terran Machine Shop")) 
                    (bMachineShopFinishSend == 0)
                    ()):
                        bMachineShopFinishSend << 1
                        DoActions(CreateUnit(1, "Mojo (Scout)", "7pBase", P7))
                    EUDEndIf()
                    if EUDIf()(EUDSCAnd()
                    (Command(P7, AtLeast, 2, "Terran Armory")) 
                    (bArmoryFinishSend == 0)
                    ()):
                        bArmoryFinishSend << 1
                        DoActions(CreateUnit(1, "Gantrithor (Carrier)", "7pBase", P7))
                    EUDEndIf()
                    if EUDIf()(EUDSCAnd()
                    (Command(P7, AtLeast, 1, "Terran Starport"))
                    (sciFacilityNum == 0)
                    ()):
                        if Setting._DEBUG:
                            f_simpleprint("build Science Facility")
                        BuildCommand("Science Facility", EncodeUnit("Terran Science Facility"))
                    EUDEndIf()
                    if EUDIf()(Command(P7, AtLeast, 2, "Terran Engineering Bay")):
                        if EUDIf()(bEngineeringBayFinishSend == 0):
                            bEngineeringBayFinishSend << 1
                            DoActions(CreateUnit(1, "Bengalaas (Jungle Critter)", "7pBase", P7))
                        EUDEndIf()
                    EUDEndIf()
                    if EUDIf()(EUDSCAnd()
                    (Command(P7, AtLeast, 1, "Terran Science Facility"))
                    (Command(P7, AtMost, 10, "Terran Barracks"))
                    ()):
                        DoActions([
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks1")
                        ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks1")):
                            BuildCommand("OutsideBarracks1", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks2")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks2")):
                            BuildCommand("OutsideBarracks2", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks3")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks3")):
                            BuildCommand("OutsideBarracks3", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks4")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks4")):
                            BuildCommand("OutsideBarracks4", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks5")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks5")):
                            BuildCommand("OutsideBarracks5", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks6")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks6")):
                            BuildCommand("OutsideBarracks6", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks7")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks7")):
                            BuildCommand("OutsideBarracks7", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks8")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks8")):
                            BuildCommand("OutsideBarracks8", EncodeUnit("Terran Barracks"))
                        EUDEndIf()

                        DoActions([
                            RemoveUnit("Dark Templar (Hero)", P7),
                            CreateUnit(1, "Dark Templar (Hero)","7pBase", P7),
                            MoveUnit(All, "Dark Templar (Hero)", P7, "Anywhere", "OutsideBarracks9")
                            ])
                        if EUDIf()(Bring(P7, AtLeast, 1, "Dark Templar (Hero)", "OutsideBarracks9")):
                            BuildCommand("OutsideBarracks9", EncodeUnit("Terran Barracks"))
                        EUDEndIf()
                        DoActions(RemoveUnit("Dark Templar (Hero)", P7))
                    EUDEndIf()
                EUDEndIf()
            EUDEndIf()
        EUDEndIf()
    EUDEndIf()
def AIScriptMessageDispatcher():
    # 커맨드 센터 완료 확인
    if EUDIf()(Command(P7, AtLeast, 1, "Zeratul (Dark Templar)")):
        DoActions(RemoveUnit("Zeratul (Dark Templar)", P7))
        DoActions(RemoveUnit("Fenix (Dragoon)", P7))
    EUDEndIf()
    # 펙토리 완료 확인
    if EUDIf()(Command(P7, AtLeast, 1, "Tassadar (Templar)")):
        DoActions(RemoveUnit("Tassadar (Templar)", P7))
        DoActions(RemoveUnit("Artanis (Scout)", P7))
    EUDEndIf()
    # 머신샵 완료 확인
    if EUDIf()(Command(P7, AtLeast, 1, "Warbringer (Reaver)")):
        DoActions(RemoveUnit("Warbringer (Reaver)", P7))
        DoActions(RemoveUnit("Mojo (Scout)", P7))
    EUDEndIf()
    # 아머리 완료 확인
    if EUDIf()(Command(P7, AtLeast, 1, "Rhynadon (Badlands Critter)")):
        DoActions(RemoveUnit("Rhynadon (Badlands Critter)", P7))
        DoActions(RemoveUnit("Gantrithor (Carrier)", P7))
    EUDEndIf()
    # 사이언스 퍼실리티 완료 확인
    if EUDIf()(Command(P7, AtLeast, 1, "Kakaru (Twilight Critter)")):
        DoActions(RemoveUnit("Kakaru (Twilight Critter)", P7))
        DoActions(RemoveUnit("Bengalaas (Jungle Critter)", P7))
    EUDEndIf()
def FindIdleSCV(epd):
    global SCV_ready, bSCVArrived
    if EUDIf()(EUDSCAnd()
    (SCV_ready == 0)
    (bSCVArrived)
    (Bring(P7, AtLeast, 1, "Terran SCV", "Anywhere"))
    ()):
        playerID = epd + 0x4C // 4
        unitType = epd + 0x64 // 4
        orderID = epd + 0x4D // 4
        # Debuging
        #f_simpleprint(epd, 'orderID', f_bread_epd(orderID, 0x4D % 4))
        if EUDIf()(EUDSCAnd()
        (MemoryEPD(unitType, Exactly, EncodeUnit("Terran SCV")))
        (MemoryXEPD(playerID, Exactly, 6, 0xFF))
        (EUDSCOr()
        (MemoryXEPD(orderID, Exactly, 0x0300, 0xFF00)) # 사람전용 Stop
        (MemoryXEPD(orderID, Exactly, 0x9A00, 0xFF00)) # 컴퓨터전용 Stop
        (MemoryXEPD(orderID, Exactly, 0x9C00, 0xFF00)) # 컴퓨터전용 script
        (MemoryXEPD(orderID, Exactly, 0x5500, 0xFF00)) # Move to Harvest Minerals
        (MemoryXEPD(orderID, Exactly, 0x4F00, 0xFF00)) # Move to Harvest
        (MemoryXEPD(orderID, Exactly, 0x0600, 0xFF00)) # Move
        ())
        ()):
            SCV_ready << 1
            idleSCV_epd << epd
            if Setting._DEBUG:
                f_simpleprint("find Idle SCV", idleSCV_epd)
        EUDEndIf()
    EUDEndIf()


def BuildingCheck(epd):
    global commandCenterNum, barracksNum, factoryNum, armoryNum, starportNum, sciFacilityNum, academyNum, engineeringBayNum
    unitType = epd + 0x64 // 4
    playerID = epd + 0x4C // 4
    if EUDIf()(MemoryXEPD(playerID, Exactly, 6, 0xFF)):
        if EUDIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Command Center"))):
            commandCenterNum += 1
        if EUDElseIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Barracks"))):
            barracksNum += 1
        if EUDElseIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Factory"))):
            factoryNum += 1
        if EUDElseIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Armory"))):
            armoryNum += 1
        if EUDElseIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Starport"))):
            starportNum += 1
        if EUDElseIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Science Facility"))):
            sciFacilityNum += 1
        if EUDElseIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Academy"))):
            academyNum += 1
        if EUDElseIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Terran Engineering Bay"))):
            engineeringBayNum += 1
        EUDEndIf()
    EUDEndIf()
def BuildingCheck2():
    global commandCenterNum, barracksNum, factoryNum, armoryNum, starportNum, sciFacilityNum, academyNum, engineeringBayNum
    commandCenterNum << 0
    barracksNum << 0
    factoryNum << 0
    armoryNum << 0
    starportNum << 0
    sciFacilityNum << 0
    academyNum << 0
    engineeringBayNum << 0

    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, commandCenterNum, "Terran Command Center")):
            EUDBreak()
        if EUDElse()():
            commandCenterNum += 1
        EUDEndIf()
    EUDEndWhile()
    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, barracksNum, "Terran Barracks")):
            EUDBreak()
        if EUDElse()():
            barracksNum += 1
        EUDEndIf()
    EUDEndWhile()
    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, factoryNum, "Terran Factory")):
            EUDBreak()
        if EUDElse()():
            factoryNum += 1
        EUDEndIf()
    EUDEndWhile()
    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, armoryNum, "Terran Armory")):
            EUDBreak()
        if EUDElse()():
            armoryNum += 1
        EUDEndIf()
    EUDEndWhile()
    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, starportNum, "Terran Starport")):
            EUDBreak()
        if EUDElse()():
            starportNum += 1
        EUDEndIf()
    EUDEndWhile()
    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, sciFacilityNum, "Terran Science Facility")):
            EUDBreak()
        if EUDElse()():
            sciFacilityNum += 1
        EUDEndIf()
    EUDEndWhile()
    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, academyNum, "Terran Academy")):
            EUDBreak()
        if EUDElse()():
            academyNum += 1
        EUDEndIf()
    EUDEndWhile()
    if EUDWhile()(True):
        if EUDIf()(Command(P7, AtMost, engineeringBayNum, "Terran Engineering Bay")):
            EUDBreak()
        if EUDElse()():
            engineeringBayNum += 1
        EUDEndIf()
    EUDEndWhile()

def beforeUnitLoop():
    commandCenterNum << 0
    barracksNum << 0
    factoryNum << 0
    armoryNum << 0
    starportNum << 0
    sciFacilityNum << 0
    academyNum << 0
    engineeringBayNum << 0
def addSCV(epd):
    for i in EUDLoopRange(0, SCV_MAX):
        if EUDIf()(scv_array[i] == 0):
            scv_array[i] = epd
            EUDBreak()
        EUDEndIf()
    
def onNewUnitLoop(epd):
    global scv_array
    unitType = epd + 0x64 // 4
    playerID = epd + 0x4C // 4
    
    if EUDIf()(EUDSCAnd()
    (MemoryEPD(unitType, Exactly, EncodeUnit("Terran SCV")))
    (MemoryXEPD(playerID, Exactly, 6, 0xFF))
    ()):
        addSCV(epd)
    EUDEndIf()
    
    if EUDIf()(command_epd == 0):
        if EUDIf()(EUDSCAnd()
        (MemoryEPD(unitType, Exactly, EncodeUnit("Terran Command Center")))
        (MemoryXEPD(playerID, Exactly, 6, 0xFF))
        ()):
            command_epd << epd
        EUDEndIf()
    if EUDElseIf()(MemoryXEPD(epd + 0x4D // 4, Exactly, 0, 0xFF00)):
        command_epd << 0
    EUDEndIf()

def onUnitLoop(epd):
    global command_epd
    FindIdleSCV(epd)
    BuildingCheck(epd)
    if EUDIf()(command_epd == 0):
        unitType = epd + 0x64 // 4
        playerID = epd + 0x4C // 4
        if EUDIf()(EUDSCAnd()
        (MemoryEPD(unitType, Exactly, EncodeUnit("Terran Command Center")))
        (MemoryXEPD(playerID, Exactly, 6, 0xFF))
        ()):
            command_epd << epd
        EUDEndIf()
    if EUDElseIf()(MemoryXEPD(epd + 0x4D // 4, Exactly, 0, 0xFF00)):
        command_epd << 0
    EUDEndIf()
def Update():
    global command_epd, scv_array
    for i in EUDLoopRange(0, SCV_MAX):
        if EUDIf()(scv_array[i] != 0):
            orderID = scv_array[i] + 0x4D // 4
            if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0xFF00)): # 죽으면
                scv_array[i] = 0
                EUDContinue()
            EUDEndIf()

            FindIdleSCV(scv_array[i])
        EUDEndIf()
    BuildingCheck2()
    AutoBuild()
    AIScriptMessageDispatcher()

def afterUnitLoop():
    AutoBuild()
    AIScriptMessageDispatcher()