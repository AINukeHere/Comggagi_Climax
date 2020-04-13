from eudplib import *
import Setting
import util
TARGET_MAX = 10
class AttackThisArea(EUDStruct):
    _fields_ = [
        ('targetUnits', EUDArray),
        ('attackPlayers', EUDArray),
        'nAttackPlayer',
        ('targetPlayers', EUDArray),
        'nTargetPlayer',
        ('areaLocInfo', EUDArray),
        ('targetUnitPos', EUDArray),
        ('currentFrameTargetInfo', EUDArray) # 현재프레임에서 공격대상 유닛epd값, 위치값, 공격자 수
    ]

    def constructor(self, nAttackPlayer, nTargetPlayer):
        self.targetUnits = EUDArray(TARGET_MAX)
        self.targetUnitPos = EUDArray(TARGET_MAX)
        self.attackPlayers = EUDArray(nAttackPlayer)
        self.nAttackPlayer = nAttackPlayer
        self.nTargetPlayer = nTargetPlayer
        self.areaLocInfo = EUDArray(4)
        self.currentFrameTargetInfo = EUDArray(3)
        for i in EUDLoopRange(0,nAttackPlayer):
            self.attackPlayers[i] = -1
        self.targetPlayers = EUDArray(nTargetPlayer)
        for i in EUDLoopRange(0,nTargetPlayer):
            self.targetPlayers[i] = -1

    @EUDMethod
    def addAttackPlayer(self, player):
        for i in EUDLoopRange(0,self.nAttackPlayer):
            if EUDIf()(self.attackPlayers[i] == -1):
                self.attackPlayers[i] = player
                EUDReturn()
            EUDEndIf()
    @EUDMethod
    def addTargetPlayer(self, player):
        for i in EUDLoopRange(0,self.nTargetPlayer):
            if EUDIf()(self.targetPlayers[i] == -1):
                self.targetPlayers[i] = player
                EUDReturn()
            EUDEndIf()
    @EUDMethod
    def SetArea(self, locationIndex):
        self.ClearTargetUnits()
        locOffset = EPD(0x58DC60) + locationIndex*5
        self.areaLocInfo[0] = f_dwread_epd(locOffset)
        self.areaLocInfo[1] = f_dwread_epd(locOffset+1)*0x10000 # 구조오프셋 pos비교최적화
        self.areaLocInfo[2] = f_dwread_epd(locOffset+2)
        self.areaLocInfo[3] = f_dwread_epd(locOffset+3)*0x10000
        if Setting._DEBUG:
            f_simpleprint(self.areaLocInfo[0],self.areaLocInfo[1],self.areaLocInfo[2],self.areaLocInfo[3])

    def ClearTargetUnits(self):
        for i in EUDLoopRange(0,TARGET_MAX):
            self.targetUnits[i] = 0

    def beforeUnitLoop(self):
        self.currentFrameTargetInfo[2] = 0
        for i in EUDLoopRange(0,TARGET_MAX):
            EUDContinueIf(self.targetUnits[i] == 0)
            epd = EPD(self.targetUnits[i])
            orderID = epd + 0x4D // 4
            statusFlags = epd + 0xDC // 4
            unitType = epd + 0x64 // 4
            #죽은 대상들은 0으로 초기화
            if EUDIf()(EUDSCOr()
            (MemoryXEPD(orderID, Exactly, 0, 0xFF00)) # 죽거나
            (MemoryXEPD(statusFlags, Exactly, 0, 2)) # 지상건물이 아니거나
            (MemoryEPD(unitType, Exactly, EncodeUnit("Infested Command Center"))) # 감염되었거나
            ()):
                if Setting._DEBUG:
                    f_simpleprint('target', i, 'dead')
                if EUDIf()(self.targetUnits[i] == self.currentFrameTargetInfo[0]):
                    self.currentFrameTargetInfo[0] = 0
                    if Setting._DEBUG:
                        f_simpleprint('curFrameTarget Reset')
                EUDEndIf()
                self.targetUnits[i] = 0
            if EUDElseIf()(self.currentFrameTargetInfo[0] == 0):
                self.currentFrameTargetInfo[0] = self.targetUnits[i]
                self.currentFrameTargetInfo[1] = self.targetUnitPos[i]
                if Setting._DEBUG:
                    f_simpleprint('target', i)
            EUDEndIf()

    def changeRandomTarget(self):
        s = f_rand() % TARGET_MAX
        curIdx = s
        if EUDWhile()(s > 0):
            s -= 1
            if EUDIf()(self.targetUnits[curIdx] != 0):
                self.currentFrameTargetInfo[0] = self.targetUnits[curIdx]
                self.currentFrameTargetInfo[1] = self.targetUnitPos[curIdx]
                EUDBreak()
            EUDEndIf()
        EUDEndWhile()
        if Setting._DEBUG:
            f_simpleprint(self.currentFrameTargetInfo[0],self.currentFrameTargetInfo[1])
    @EUDMethod
    def onUnitLoop(self, ptr, epd):
        global attackerCount
        playerID = epd + 0x4C // 4
        unitType = epd + 0x64 // 4
        unitPos = epd + 0x28 // 4
        orderID = epd + 0x4D // 4
        statusFlags = epd + 0xDC // 4
        if EUDIf()(MemoryXEPD(orderID, Exactly, 0, 0xFF00)):
            EUDReturn()
        EUDEndIf()
        #일단 로케이션 안에 있나
        if EUDIf()(EUDSCAnd()
            # 동적 좌표
            # (MemoryXEPD(unitPos, AtLeast, self.areaLocInfo[0], 0xFFFF)) # posX <= locX1
            # (MemoryXEPD(unitPos, AtMost, self.areaLocInfo[2], 0xFFFF)) # locX2 <= posX
            # (MemoryXEPD(unitPos, AtLeast, self.areaLocInfo[1], 0xFFFF0000)) # posY <= locY1
            # (MemoryXEPD(unitPos, AtMost, self.areaLocInfo[3], 0xFFFF0000)) # locY2 <= posY
            # 정적 좌표
            (MemoryXEPD(unitPos, AtLeast, 1808, 0xFFFF)) # posX <= locX1
            (MemoryXEPD(unitPos, AtMost, 2288, 0xFFFF)) # locX2 <= posX
            (MemoryXEPD(unitPos, AtLeast, 592*0x10000, 0xFFFF0000)) # posY <= locY1
            (MemoryXEPD(unitPos, AtMost, 864*0x10000, 0xFFFF0000)) # locY2 <= posY
        ()):
            bTargetPlayer = EUDVariable(0)
            bTargetPlayer << 0
            bTargetUnitType = EUDVariable(0)
            bTargetUnitType << 0
            # targetPlayer 소유인지 체크
            for i in EUDLoopRange(0, self.nTargetPlayer):
                if EUDIf()(EUDSCAnd()
                (self.targetPlayers[i] != -1)
                (MemoryXEPD(playerID, Exactly, self.targetPlayers[i], 0xFF))
                ()):
                    bTargetPlayer << 1
                    EUDBreak()
                EUDEndIf()
            # targetPlayer소유라면 targetUnitType 체크
            if EUDIf()(EUDSCAnd()
            (bTargetPlayer)
            (MemoryXEPD(statusFlags, AtLeast, 1, 2)) # 지상건물이어야함
            ()):
                if EUDIf()(EUDSCOr()
                (MemoryEPD(unitType, Exactly, EncodeUnit('Terran Command Center')))
                (MemoryEPD(unitType, Exactly, EncodeUnit('Terran Barracks')))
                (MemoryEPD(unitType, Exactly, EncodeUnit('Terran Factory')))
                (MemoryEPD(unitType, Exactly, EncodeUnit('Protoss Nexus')))
                ()):
                    bTargetUnitType << 1
                EUDEndIf()
                # 최종적으로 일점사대상이라면
                if EUDIf()(bTargetUnitType):
                    for i in EUDLoopRange(TARGET_MAX):
                        # 등록되어있으면 Break
                        if EUDIf()(self.targetUnits[i] == ptr):
                            EUDBreak()
                        EUDEndIf()
                        # 빈 자리에 등록
                        if EUDIf()(self.targetUnits[i] == 0):
                            self.targetUnits[i] = ptr
                            self.targetUnitPos[i] = f_dwread_epd(epd+0x28//4)
                            if Setting._DEBUG:
                                f_simpleprint('register', f_bread_epd(playerID,0x4C % 4),f_dwread_epd(unitType))
                            EUDBreak()
                        EUDEndIf()
                EUDEndIf()
            if EUDElseIf()(self.currentFrameTargetInfo[0] != 0): # 타겟이 있을때만 실행하자
                bAttackPlayer = EUDVariable(0)
                bAttackPlayer << 0
                bAttackUnitType = EUDVariable(0)
                bAttackUnitType << 0
                # attackPlayer의 소유인지 체크
                for i in EUDLoopRange(0, self.nAttackPlayer):
                    if EUDIf()(EUDSCAnd()
                    (self.attackPlayers[i] != -1)
                    (MemoryXEPD(playerID, Exactly, self.attackPlayers[i], 0xFF))
                    ()):
                        bAttackPlayer << 1
                        EUDBreak()
                    EUDEndIf()
                # attackPlayer소유라면 attackUnitType 체크
                if EUDIf()(bAttackPlayer):
                    if EUDIf()(EUDSCOr()
                    (MemoryEPD(unitType, Exactly, EncodeUnit('Zerg Zergling')))
                    (MemoryEPD(unitType, Exactly, EncodeUnit('Zerg Hydralisk')))
                    (MemoryEPD(unitType, Exactly, EncodeUnit('Zerg Ultralisk')))
                    (MemoryEPD(unitType, Exactly, EncodeUnit('Protoss Zealot')))
                    (MemoryEPD(unitType, Exactly, EncodeUnit('Protoss Dark Templar')))
                    ()):
                        orderState = epd + 0x4E // 4
                        orderTargetCUnit = epd + 0x5C // 4
                        orderTargetPosition = epd + 0x58 // 4
                        secondTarget = epd + 0x7C // 4
                        if Setting.ENTRANCE_ATTACKER_PRINT:
                            self.currentFrameTargetInfo[2] += 1
                        DoActions([
                            SetMemoryXEPD(orderID, SetTo, 0x0A00, 0xFF00),
                            SetMemoryXEPD(orderState, SetTo, 0x010000,0xFF0000),
                            SetMemoryEPD(orderTargetCUnit, SetTo, self.currentFrameTargetInfo[0]), # targetEPD
                            SetMemoryEPD(orderTargetPosition, SetTo, self.currentFrameTargetInfo[1]), # targetPos
                            SetMemoryEPD(secondTarget, SetTo, self.currentFrameTargetInfo[0]), # targetEPD
                        ])
                    EUDEndIf()
                EUDEndIf()
            EUDEndIf()
        EUDEndIf()
