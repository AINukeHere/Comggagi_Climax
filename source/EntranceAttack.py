from eudplib import *
_DEBUG = False

### Settings ###
defenserPlayers = [0,1,2]
attackerPlayers = [6,7]
attackerUnitTypes = [
    EncodeUnit("Zerg Zergling"),
    EncodeUnit("Zerg Hydralisk"),
    EncodeUnit("Protoss Zealot"),
    EncodeUnit("Protoss Dark Templar"),
]
MAX_ATTACKER = 200
MAX_DEFENSER_CANDIDATE = 50
MAX_DEFENSER = 4
### Settings ###


attackerUnits = EUDArray(MAX_ATTACKER)
defenserUnits = EUDArray(MAX_DEFENSER)
defenserUnitCandidates = EUDArray(MAX_DEFENSER_CANDIDATE)
def AddAttacker(epd):
    for i in EUDLoopRange(0, MAX_ATTACKER):
        if EUDIf()(attackerUnits[i] == 0):
            attackerUnits[i] = epd
            if _DEBUG:
                f_simpleprint("attacker unit registed")
            EUDBreak()
        EUDEndIf()
def onNewUnitLoop(epd):

    playerID = epd + 0x4C // 4
    unitType = epd + 0x64 // 4
    unitPos = epd + 0x28 // 4
    # 입막하는 플레이어인지 검사
    if EUDIf()(EUDSCOr()
    (MemoryXEPD(playerID, Exactly, defenserPlayers[0], 0xFF))
    (MemoryXEPD(playerID, Exactly, defenserPlayers[1], 0xFF))
    (MemoryXEPD(playerID, Exactly, defenserPlayers[2], 0xFF))
    (MemoryXEPD(playerID, Exactly, 11, 0xFF))
    ()):
        # 테란입막건물같이 이동가능한 놈들은 무조건 등록, 그 외에는 입구에 설치된 건물만 등록
        if EUDIf()(EUDSCOr()
        (MemoryEPD(unitType, Exactly, EncodeUnit("Terran Command Center")))
        (MemoryEPD(unitType, Exactly, EncodeUnit("Terran Barracks")))
        (MemoryEPD(unitType, Exactly, EncodeUnit("Terran Factory")))
        ()):
            for i in EUDLoopRange(0, MAX_DEFENSER_CANDIDATE):
                if EUDIf()(defenserUnitCandidates[i] == 0):
                    defenserUnitCandidates[i] = epd
                    if _DEBUG:
                        f_simpleprint("defenser unit candicate registed")
                    EUDBreak()
                EUDEndIf()
        EUDEndIf()
        if EUDIf()(EUDSCAnd()
        (EUDSCOr()
        (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Hatchery")))
        (MemoryEPD(unitType, Exactly, EncodeUnit("Protoss Nexus")))
        (MemoryEPD(unitType, Exactly, EncodeUnit("Protoss Cybernetics Core")))
        ())
        (MemoryXEPD(unitPos, AtLeast, 1808, 0xFFFF)) # posX <= locX1
        (MemoryXEPD(unitPos, AtMost, 2288, 0xFFFF)) # locX2 <= posX
        (MemoryXEPD(unitPos, AtLeast, (592+128)*0x10000, 0xFFFF0000)) # posY <= locY1
        (MemoryXEPD(unitPos, AtMost, (864+128)*0x10000, 0xFFFF0000)) # locY2 <= posY
        ()):
            for i in EUDLoopRange(0, MAX_DEFENSER):
                if EUDIf()(defenserUnits[i] == 0):
                    defenserUnits[i] = epd
                    if _DEBUG:
                        f_simpleprint("defenser unit registed")
                    EUDBreak()
                EUDEndIf()
        EUDEndIf()
    # 입구를 뚫는 플레이어인지 검사
    if EUDElseIf()(EUDSCAnd()
    (EUDSCOr()
    (MemoryXEPD(playerID, Exactly, attackerPlayers[0], 0xFF))
    (MemoryXEPD(playerID, Exactly, attackerPlayers[1], 0xFF))
    ())
    (EUDSCOr()
    (MemoryEPD(unitType, Exactly, attackerUnitTypes[0]))
    (MemoryEPD(unitType, Exactly, attackerUnitTypes[1]))
    (MemoryEPD(unitType, Exactly, attackerUnitTypes[2]))
    (MemoryEPD(unitType, Exactly, attackerUnitTypes[3]))
    ())
    ()):
        AddAttacker(epd)
    EUDEndIf()

targetUnitPtr = EUDVariable(0)
targetUnitEPD = EUDVariable(0)
targetUnitPos = EUDVariable(0)
def Update():
    global targetUnitPtr, targetUnitEPD
    defenserUnitCount = EUDVariable(0)
    defenserUnitCount << 0
    defenserUnitCandidateCount = EUDVariable(0)
    defenserUnitCandidateCount << 0
    # 입막건물관리
    for i in EUDLoopRange(0, MAX_DEFENSER):
        if EUDIf()(defenserUnits[i] != 0):
            # 파괴된 건물 제외
            orderID = defenserUnits[i] + 0x4D // 4
            if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0xFF00)):
                if EUDIf()(targetUnitEPD == defenserUnits[i]):
                    targetUnitEPD << 0
                EUDEndIf()                
                defenserUnits[i] = 0
                EUDContinue()
            EUDEndIf()
            if _DEBUG:
                defenserUnitCount += 1
            # 확실한 입막건물들을 관리하며 존재한다면 최종타겟으로 설정
            targetUnitEPD << defenserUnits[i]
            targetUnitPtr << targetUnitEPD*4 + 0x58A364
            targetUnitPos << f_dwread_epd(targetUnitEPD + 0x28 // 4)
            if _DEBUG:
                f_simpleprint("targetUnitEPD in defenserUnits = ", targetUnitEPD)
        EUDEndIf()
    for i in EUDLoopRange(0, MAX_DEFENSER_CANDIDATE):
        if EUDIf()(defenserUnitCandidates[i] != 0):
            orderID = defenserUnitCandidates[i] + 0x4D // 4
            statusFlags = defenserUnitCandidates[i] + 0xDC // 4
            if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0xFF00)):# 터진경우
                if EUDIf()(targetUnitEPD == defenserUnitCandidates[i]):
                    targetUnitEPD << 0
                EUDEndIf()
                defenserUnitCandidates[i] = 0
                EUDContinue()
            if EUDElseIf()(MemoryXEPD(statusFlags, Exactly, 0, 2)): # 지상건물이 아닌경우 (테란이 입구건물 띄움)
                if EUDIf()(targetUnitEPD == defenserUnitCandidates[i]):
                    targetUnitEPD << 0
                EUDEndIf()
                EUDContinue()
            EUDEndIf()
            if _DEBUG:
                defenserUnitCandidateCount += 1

            # 확실한 입막건물이 없다면 후보자들 중에서 뽑는다.
            if EUDIf()(targetUnitEPD == 0):
                unitPos = defenserUnitCandidates[i] + 0x28 // 4
                if EUDIf()(EUDSCAnd()
                (MemoryXEPD(statusFlags, AtLeast, 1, 2)) # 지상건물이어야함
                (MemoryXEPD(unitPos, AtLeast, 1984, 0xFFFF)) # posX <= locX1
                (MemoryXEPD(unitPos, AtMost, 2128, 0xFFFF)) # locX2 <= posX
                (MemoryXEPD(unitPos, AtLeast, 704*0x10000, 0xFFFF0000)) # posY <= locY1
                (MemoryXEPD(unitPos, AtMost, 928*0x10000, 0xFFFF0000)) # locY2 <= posY
                ()):
                    targetUnitEPD << defenserUnitCandidates[i]
                    targetUnitPtr << targetUnitEPD*4 + 0x58A364
                    targetUnitPos << f_dwread_epd(targetUnitEPD + 0x28 // 4)
                    if _DEBUG:
                        f_simpleprint("targetUnitEPD in candidates = ", targetUnitEPD)
                EUDEndIf()
            EUDEndIf()
        EUDEndIf()
    # if _DEBUG:
    #     f_simpleprint(defenserUnitCount, defenserUnitCandidateCount)


    # 공격자
    epd = EUDVariable(0)
    if _DEBUG:
        attackerCount=EUDVariable(0)
        attackerCount<< 0
        attackerCount2=EUDVariable(0)
        attackerCount2<< 0
    bAttack = EUDVariable(0)
    if EUDIf()(EUDSCAnd()
    (targetUnitEPD != 0)
    (Bring(Force1, Exactly, 0, "Men", "EntranceLoc1"))
    ()):
        bAttack << 1
    if EUDElse()():
        bAttack << 0
    EUDEndIf()
    for i in EUDLoopRange(0, MAX_ATTACKER):
        if EUDIf()(attackerUnits[i] != 0):
            epd << attackerUnits[i]
            orderID = epd + 0x4D // 4
            if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0xFF00)):
                attackerUnits[i] = 0
                EUDContinue()
            EUDEndIf()
            if EUDIf()(bAttack):
                unitPos = epd + 0x28 // 4
                if _DEBUG:
                    attackerCount2 += 1
                if EUDIf()(EUDSCAnd()
                (MemoryXEPD(unitPos, AtLeast, 1808, 0xFFFF)) # posX <= locX1
                (MemoryXEPD(unitPos, AtMost, 2288, 0xFFFF)) # locX2 <= posX
                (MemoryXEPD(unitPos, AtLeast, 720*0x10000, 0xFFFF0000)) # posY <= locY1
                (MemoryXEPD(unitPos, AtMost, 992*0x10000, 0xFFFF0000)) # locY2 <= posY
                ()):
                    orderState = epd + 0x4E // 4
                    orderTargetCUnit = epd + 0x5C // 4
                    orderTargetPosition = epd + 0x58 // 4
                    secondTarget = epd + 0x7C // 4
                    if _DEBUG:
                        attackerCount += 1
                    DoActions([
                        SetMemoryXEPD(orderState, SetTo, 0x010A00,0x00FF00),
                        SetMemoryEPD(orderTargetCUnit, SetTo, targetUnitPtr), # targetPtr
                        SetMemoryEPD(orderTargetPosition, SetTo, targetUnitPos), # targetPos
                        SetMemoryEPD(secondTarget, SetTo, targetUnitPtr), # targetPtr # 이것까지 제어해야 질럿,닥템들이 때림
                    ])
                EUDEndIf()
            EUDEndIf()
        EUDEndIf()
    if _DEBUG:
        f_simpleprint('attacker = ', attackerCount,'/',attackerCount2)