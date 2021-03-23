from eudplib import *
import Setting
import TerranBuild

GROUP_STATE_0FIND_MEMBER        = 0
GROUP_STATE_1PREPARE            = 1
GROUP_STATE_2FIND_SCV           = 2
GROUP_STATE_3GO_TO_SCV          = 3
GROUP_STATE_4MINDCONTROL_SCV    = 4
GROUP_STATE_5Transport_SCV      = 5
GROUP_STATE_6RUN_AWAY           = 6
GROUP_STATE_7ARRIVE_BASE        = 7
GROUP_STATE_8IDLE               = 8
class StrategyGroup(EUDStruct):
    _fields_ = [
        'targetSCVPtr',
        'targetSCVEPD',
        'DarkArchonPtr',
        'DarkArchonEPD',
        'ShuttlePtr',
        'ShuttleEPD',
        'groupState',
        'minDistSCV',
    ]
    def constructor(self):
        self.reset()
        self.groupState = GROUP_STATE_8IDLE
    @EUDMethod
    def reset(self):
        self.targetSCVEPD = 0
        self.targetSCVPtr = 0
        self.DarkArchonPtr = 0
        self.DarkArchonEPD = 0
        self.ShuttlePtr = 0
        self.ShuttleEPD = 0
        self.minDistSCV = 999999
        self.groupState = GROUP_STATE_0FIND_MEMBER

    def beforeUnitLoop(self):
        if EUDIf()(self.groupState == GROUP_STATE_2FIND_SCV):
            self.minDistSCV = 999999
        EUDEndIf()
    @EUDMethod
    def afterUnitLoop(self):
        DA_orderID = self.DarkArchonEPD + 0x4D // 4
        DA_orderTargetPtr = self.DarkArchonEPD + 0x5C // 4
        DA_currentDirection1 = self.DarkArchonEPD + 0x21 // 4
        DA_connectedUnit = self.DarkArchonEPD + 0x80 // 4

        SH_playerID = self.ShuttleEPD + 0x4C // 4
        SH_orderID = self.ShuttleEPD + 0x4D // 4
        SH_orderTargetPtr = self.ShuttleEPD + 0x5C // 4
        SH_orderTargetPos = self.ShuttleEPD + 0x58 // 4
        SH_lockdownTimer = self.ShuttleEPD + 0x117 // 4

        SCV_playerID = self.targetSCVEPD + 0x4C // 4
        SCV_orderID = self.targetSCVEPD + 0x4D // 4
        SCV_connectedUnit = self.targetSCVEPD + 0x80 // 4
        SCV_HP = self.targetSCVEPD + 0x08 // 4
        # unused
        # SCV_orderTargetPtr = self.targetSCVEPD + 0x5C // 4

        SomethingBadHappend = EUDVariable(0)
        SomethingBadHappend << 0
        # 문제가 발생했는가?
        if EUDIf()(EUDSCAnd() # 셔틀은 끝까지 계속 필요
        (self.groupState >= GROUP_STATE_1PREPARE)
        (self.groupState <= GROUP_STATE_7ARRIVE_BASE)
        ()):
            if EUDIf()(EUDSCOr()
                (MemoryXEPD(SH_orderID, Exactly, 0x0000, 0xFF00)) # 셔틀이 죽었거나
                (EUDNot(MemoryXEPD(SH_playerID,Exactly, 6, 0xFF))) # 마컨을 당하여 내꺼가 아니거나
                (MemoryXEPD(SH_lockdownTimer, AtLeast, 0x01000000, 0xFF000000)) # 락다를 당했거나
                ()):
                    self.reset()
                    if Setting._DEBUG:
                        f_simpleprint('Shuttle Dead')
                    SomethingBadHappend << 1
            EUDEndIf()
        EUDEndIf()
        if EUDIf()(EUDSCAnd() # 다칸은 마컨할대까지 계속 필요
        (self.groupState >= GROUP_STATE_1PREPARE)
        (self.groupState <= GROUP_STATE_4MINDCONTROL_SCV)
        ()):
            if EUDIf()(MemoryXEPD(DA_orderID, Exactly, 0x0000, 0xFF00)):
                self.reset()
                if Setting._DEBUG:
                    f_simpleprint('DarkArchon Dead')
                SomethingBadHappend << 1
            EUDEndIf()
        EUDEndIf()
        if EUDIf()(EUDSCAnd() # SCV는 데리러갈때부터 끝까지 계속 필요
        (self.groupState >= GROUP_STATE_3GO_TO_SCV)
        (self.groupState <= GROUP_STATE_7ARRIVE_BASE)
        (EUDNot(MemoryXEPD(SCV_playerID, Exactly, 6, 0xFF)))
        ()):
            if EUDIf()(EUDSCOr()
            (MemoryXEPD(SCV_orderID, Exactly, 0x0000, 0xFF00)) # SCV가 죽거나
            (MemoryXEPD(SCV_orderID, Exactly, 0x0500, 0xFF00)) # 벙커에 있거나
            (MemoryEPD(SCV_HP, AtMost, 15359)) # 체력이 깎였거나
            ()):
                self.targetSCVEPD = 0
                self.targetSCVPtr = 0
                self.groupState = GROUP_STATE_1PREPARE
                if Setting._DEBUG:
                    f_simpleprint('SCV Dead')
                SomethingBadHappend << 1
            EUDEndIf()
        EUDEndIf()
        
        if EUDIf()(SomethingBadHappend == 1):
            EUDReturn()
        EUDEndIf()

        #Switch문 시작
        EUDSwitch(self.groupState)
        if EUDSwitchCase()(GROUP_STATE_0FIND_MEMBER):
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_1PREPARE):
            # 태우도록 명령
            DoActions([
                # 다칸은 탑승하고 셔틀은 태워라
                SetMemoryXEPD(DA_orderID, SetTo, 0x006000, 0xFFFF00), # "Load Unit (Unknown)"
                SetMemoryEPD(DA_orderTargetPtr, SetTo, self.ShuttlePtr),
                SetMemoryXEPD(SH_orderID, SetTo, 0x5E00, 0xFF00), # "Load Unit (Mobile Transport)"
                SetMemoryEPD(SH_orderTargetPtr, SetTo, self.DarkArchonPtr),
            ])
            # 태웠으면 다음 단계
            if EUDIf()(MemoryEPD(DA_connectedUnit, Exactly, self.ShuttlePtr)):
                if Setting._DEBUG:
                    f_simpleprint("Group Prepared")
                self.groupState = GROUP_STATE_2FIND_SCV
            EUDEndIf()

            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_2FIND_SCV):
            #f_simpleprint('finding scv')
            if EUDIf()(self.targetSCVEPD != 0):
                SetMemoryEPD(self.DarkArchonEPD + 0xA2 // 4, 250*0x10000,0xFFFF0000)
                self.groupState = GROUP_STATE_3GO_TO_SCV
            EUDEndIf()
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_3GO_TO_SCV):
            scvPosVal = f_dwread_epd(self.targetSCVEPD + 0x28 // 4)
            scvPosX = f_dwbreak(scvPosVal)[0]
            scvPosY = f_dwbreak(scvPosVal)[1]
            shuttlePosVal = f_dwread_epd(self.ShuttleEPD + 0x28 // 4)
            shuttlePosX = f_dwbreak(shuttlePosVal)[0]
            shuttlePosY = f_dwbreak(shuttlePosVal)[1]
            vecX = scvPosX - shuttlePosX
            vecY = scvPosY - shuttlePosY
            distance = f_sqrt(vecX*vecX + vecY*vecY)
            #f_simpleprint('going to SCV',scvPosVal)
            locX1,locX2,locY1,locY2 = EUDCreateVariables(4)
            locX1 << (shuttlePosX - 32)
            locX2 << (shuttlePosX + 32)
            locY1 << (shuttlePosY - 32)
            locY2 << (shuttlePosY + 32)
            locOffset = EPD(0x58DC60)
            if Setting._DEBUG:
                f_simpleprint(scvPosVal)
            DoActions([
                # 셔틀은 scv로 이동해라
                SetMemoryEPD(locOffset, SetTo, locX1),
                SetMemoryEPD(locOffset + 1, SetTo, locY1),
                SetMemoryEPD(locOffset + 2, SetTo, locX2),
                SetMemoryEPD(locOffset + 3, SetTo, locY2),
                Order("Protoss Shuttle", P7, "GiveMeSCV_EUDLoc", Move, "GiveMeSCV_EUDLoc"),
                SetMemoryEPD(SH_orderTargetPos, SetTo, scvPosVal),
                SetMemoryEPD(SH_orderTargetPtr, SetTo, self.targetSCVPtr),
                SetMemoryXEPD(SH_orderID, SetTo, 0x010600, 0xFF00) # "Ignore (Normal)" (Move)
            ])
            if EUDIf()(distance < 150):
                if Setting._DEBUG:
                    f_simpleprint('arrived')
                self.groupState = GROUP_STATE_4MINDCONTROL_SCV
            EUDEndIf()
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_4MINDCONTROL_SCV):
            # SCV 가져왔으면 다음 단계로
            if EUDIf()(MemoryXEPD(SCV_playerID, Exactly, 6, 0xFF)):
                if Setting._DEBUG:
                    f_simpleprint("Got SCV")
                self.groupState = GROUP_STATE_5Transport_SCV
            EUDEndIf()

            DoActions([
                #셔틀은 내려주고
                SetMemoryXEPD(SH_orderID, SetTo, 0x6F00,0xFF00), # Unload
                #다칸은 마컨
                SetMemoryXEPD(DA_orderID, SetTo, 0xB600,0xFF00), # Cast Mind Control
                SetMemoryEPD(DA_orderTargetPtr, SetTo, self.targetSCVPtr),
            ])
            # facing 맞춰주기
            if EUDIf()(Deaths(P7, AtMost, 6, "Time 3")):
                scvPosVal = f_dwread_epd(self.targetSCVEPD + 0x28 // 4)
                scvPosX = f_dwbreak(scvPosVal)[0]
                scvPosY = f_dwbreak(scvPosVal)[1]
                darkArchonPosVal = f_dwread_epd(self.DarkArchonEPD + 0x28 // 4)
                darkArchonPosX = f_dwbreak(darkArchonPosVal)[0]
                darkArchonPosY = f_dwbreak(darkArchonPosVal)[1]
                x = scvPosX - darkArchonPosX
                y = scvPosY - darkArchonPosY
                angle = (f_atan2(y,x) + 90) % 360
                direction = angle * 255 //360
                DoActions([
                    SetMemoryXEPD(DA_currentDirection1, SetTo, direction*0x100, 0xFF00),
                ])
            EUDEndIf()


            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_5Transport_SCV):
            if Setting._DEBUG:
                f_simpleprint('trasporting')
            count = EUDVariable(0)
            count += 1
            if EUDIf()(count > 0):
                scvPosVal = f_dwread_epd(self.targetSCVEPD + 0x28 // 4)
                scvPosX = f_dwbreak(scvPosVal)[0]
                scvPosY = f_dwbreak(scvPosVal)[1]
                shuttlePosVal = f_dwread_epd(self.ShuttleEPD + 0x28 // 4)
                shuttlePosX = f_dwbreak(shuttlePosVal)[0]
                shuttlePosY = f_dwbreak(shuttlePosVal)[1]
                locX1,locX2,locY1,locY2 = EUDCreateVariables(4)
                if EUDIf()(scvPosX < shuttlePosX):
                    locX1 << scvPosX
                    locX2 << shuttlePosX
                if EUDElse()():
                    locX1 << shuttlePosX
                    locX2 << scvPosX
                EUDEndIf()
                if EUDIf()(scvPosY< shuttlePosY):
                    locY1 << scvPosY
                    locY2 << shuttlePosY
                if EUDElse()():
                    locY1 << shuttlePosY
                    locY2 << scvPosY
                EUDEndIf()
                if EUDIf()(locX1 > 32):
                    locX1 -= 32
                if EUDElse()():
                    locX1 << 0
                EUDEndIf()
                if EUDIf()(locY1 > 32):
                    locY1 -= 32
                if EUDElse()():
                    locY1 << 0
                EUDEndIf()
                locX2 += 32
                locY2 += 32
                if Setting._DEBUG:
                    f_simpleprint(locX1,locY1,locX2,locY2)
                p = f_getcurpl()
                f_setcurpl(6)
                locOffset = EPD(0x58DC60)
                DoActions([
                    SetMemoryEPD(locOffset, SetTo, locX1),
                    SetMemoryEPD(locOffset + 1, SetTo, locY1),
                    SetMemoryEPD(locOffset + 2, SetTo, locX2),
                    SetMemoryEPD(locOffset + 3, SetTo, locY2),
                    # CreateUnit(30,"Terran Marine","GiveMeSCV_EUDLoc",P7),
                    # KillUnit("Terran Marine",P7),
                    # RemoveUnit("Terran Marine", P7),
                    # 셔틀은 scv로 이동해라
                    Order("Protoss Shuttle", P7, "GiveMeSCV_EUDLoc", Move, "GiveMeSCV_EUDLoc"),
                    Wait(0), # 이걸 해야 Order를 먹음
                    RunAIScriptAt("Enter Transport", "GiveMeSCV_EUDLoc")
                ])
                f_setcurpl(p)
            EUDEndIf()
            # 태웠으면 다음 단계
            if EUDIf()(MemoryEPD(SCV_connectedUnit, Exactly, self.ShuttlePtr)):
                if Setting._DEBUG:
                    f_simpleprint("SCV Transported")
                self.groupState = GROUP_STATE_6RUN_AWAY
            EUDEndIf()
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_6RUN_AWAY):
            destinationLocOffset = EPD(0x58DC60) + 1 * 5 # SCVdestination
            destinationX1 = f_dwread_epd(destinationLocOffset)
            destinationY1 = f_dwread_epd(destinationLocOffset+1)
            destinationX2 = f_dwread_epd(destinationLocOffset+2)
            destinationY2 = f_dwread_epd(destinationLocOffset+3)
            shuttlePosVal = f_dwread_epd(self.ShuttleEPD + 0x28 // 4)
            shuttlePosX = f_dwbreak(shuttlePosVal)[0]
            shuttlePosY = f_dwbreak(shuttlePosVal)[1]
            # 목적지에 도달하면 내려라
            if EUDIf()(EUDSCAnd()
            (destinationX1 <= shuttlePosX)
            (shuttlePosX <= destinationX2)
            (destinationY1 <= shuttlePosY)
            (shuttlePosY <= destinationY2)
            ()):
                DoActions([
                #셔틀은 내려주고
                SetMemoryXEPD(SH_orderID, SetTo, 0x6F00,0xFF00), # Unload

                ])
                if EUDIf()(MemoryEPD(SCV_connectedUnit, Exactly, 0)):
                    # 내렸으면 임무끝
                    self.groupState = GROUP_STATE_8IDLE
                    if Setting._DEBUG:
                        f_simpleprint('IDLE')
                    TerranBuild.SCV_ready << 1
                    TerranBuild.addSCV(self.targetSCVEPD)
                    TerranBuild.idleSCV_epd << self.targetSCVEPD
                    TerranBuild.bSCVArrived << 1
                EUDEndIf()
            #도착하지않았다면 이동
            if EUDElse()():
                destinationPosX = (destinationX1 + destinationX2) // 2
                destinationPosY = (destinationY1 + destinationY2) // 2
                destinationPos = destinationPosY * 0x10000 + destinationPosX
                locX1,locX2,locY1,locY2 = EUDCreateVariables(4)
                locX1 << (shuttlePosX - 32)
                locX2 << (shuttlePosX + 32)
                locY1 << (shuttlePosY - 32)
                locY2 << (shuttlePosY + 32)
                locOffset = EPD(0x58DC60)
                DoActions([
                # 셔틀은 튀어라
                    Order("Protoss Shuttle", P7, "GiveMeSCV_EUDLoc", Move, "GiveMeSCV_EUDLoc"),
                    SetMemoryEPD(SH_orderTargetPos, SetTo, destinationPos),
                    SetMemoryXEPD(SH_orderID, SetTo, 0x010600, 0xFF00) # "Ignore (Normal)" (Move)
                ])
            EUDEndIf()
        EUDEndSwitch()

    def UnitLoopUpdate(self, ptr, epd):
        EUDSwitch(self.groupState)
        if EUDSwitchCase()(GROUP_STATE_0FIND_MEMBER):
            unitType = epd + 0x64 // 4
            playerID = epd + 0x4C // 4
            orderID = epd + 0x4D // 4
            position = epd + 0x28 // 4
            if EUDIf()(MemoryXEPD(playerID, Exactly, 6, 0xFF)): #P7
                if EUDIf()(EUDSCAnd()
                (MemoryEPD(unitType, Exactly, EncodeUnit("Protoss Dark Archon")))
                (EUDNot(MemoryXEPD(orderID, Exactly, 0x9600, 0xFF00))) # Reset Collision
                (EUDNot(MemoryXEPD(orderID, Exactly, 0x6A00, 0xFF00))) # Completeing Archon Summon
                (MemoryXEPD(position, AtLeast, 2800*0x10000,0xFFFF0000)) # y좌표가 2800 이상일때
                ()):
                    if EUDIf()(self.DarkArchonEPD == 0):
                        if Setting._DEBUG:
                            f_simpleprint('da set')
                        self.DarkArchonPtr = ptr
                        self.DarkArchonEPD = epd
                        energy = epd + 0xA2 // 4
                        DoActions(SetMemoryXEPD(energy,SetTo,250*256*0x10000, 0xFFFF0000)) #에너지 채움
                    EUDEndIf()
                if EUDElseIf()(EUDSCAnd()
                (MemoryEPD(unitType, Exactly, EncodeUnit("Protoss Shuttle")))
                (EUDNot(MemoryXEPD(orderID, Exactly, 0x1700, 0xFF00))) # 생산중인 상태가 아니고
                ()):
                    if EUDIf()(self.ShuttleEPD == 0):
                        if Setting._DEBUG:
                            f_simpleprint('sh set')
                        self.ShuttlePtr = ptr
                        self.ShuttleEPD = epd
                    EUDEndIf()
                EUDEndIf()
            EUDEndIf()
            
            # 멤버 다 찾았으면 다음단계
            if EUDIf()(EUDSCAnd()
            (self.ShuttleEPD != 0)
            (self.DarkArchonEPD != 0)
            ()):
                if Setting._DEBUG:
                    f_simpleprint("Found Members")
                self.groupState = GROUP_STATE_1PREPARE
            EUDEndIf()
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_1PREPARE):
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_2FIND_SCV):
            unitType = epd + 0x64 // 4
            playerID = epd + 0x4C // 4
            orderID = epd + 0x4D // 4
            hitPoint = epd + 0x08 // 4
            # SCV가 있으면 거리를 계산해둠
            if EUDIf()(EUDSCAnd()
            (MemoryEPD(unitType, Exactly, EncodeUnit("Terran SCV")))
            (EUDNot(MemoryXEPD(orderID, Exactly, 0x0500, 0xFF00))) # 벙커에 있지 않거나
            (MemoryEPD(hitPoint, Exactly, 60*256)) # 풀피인 SCV만 취급
            (EUDSCOr()
            (MemoryXEPD(playerID, Exactly, 0, 0xFF))
            (MemoryXEPD(playerID, Exactly, 1, 0xFF))
            (MemoryXEPD(playerID, Exactly, 2, 0xFF))
            ())
            ()):
                scvPosVal = f_dwread_epd(epd + 0x28 // 4)
                scvPosX = f_dwbreak(scvPosVal)[0]
                scvPosY = f_dwbreak(scvPosVal)[1]
                shuttlePosVal = f_dwread_epd(self.ShuttleEPD + 0x28 // 4)
                shuttlePosX = f_dwbreak(shuttlePosVal)[0]
                shuttlePosY = f_dwbreak(shuttlePosVal)[1]
                vecX = scvPosX - shuttlePosX
                vecY = scvPosY - shuttlePosY
                distance = f_sqrt(vecX*vecX + vecY*vecY)
                if EUDIf()(self.minDistSCV > distance):
                    self.minDistSCV = distance
                    if Setting._DEBUG:
                        f_simpleprint(distance)
                    self.targetSCVEPD = epd
                    self.targetSCVPtr = ptr
                EUDEndIf()
            EUDEndIf()

            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_3GO_TO_SCV):
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_4MINDCONTROL_SCV):
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_6RUN_AWAY):
            EUDBreak()
        if EUDSwitchCase()(GROUP_STATE_8IDLE):
            EUDBreak()
        EUDEndSwitch()

def main():
    pass