from eudplib import *
import Setting
import util

SUPPORT_REAVER_MAX = 150
reavers = EUDArray(SUPPORT_REAVER_MAX)
nextReaverIdx = EUDVariable(0)

def onNewUnitLoop(epd):
    global nextReaverIdx, reavers
    unitType = epd + 0x64 // 4
    #f_simpleprint(f_dwread_epd(unitType))
    if EUDIf()(MemoryEPD(unitType, Exactly, EncodeUnit("Protoss Reaver"))):
        reavers[nextReaverIdx] = epd
        if Setting.ReaverFixDebug:
            f_simpleprint('new Reaver : ', nextReaverIdx, reavers[nextReaverIdx], epd)
        for i in EUDLoopRange(0, SUPPORT_REAVER_MAX):
            if EUDIf()(EUDSCOr()
            (reavers[i] == 0)
            (reavers[i] == -1)
            ()):
                nextReaverIdx << i
                EUDBreak()
            EUDEndIf()
        if Setting.ReaverFixDebug:
            f_simpleprint('nextReaverIdx << ', i, nextReaverIdx)
    EUDEndIf()

            

def beforeTriggerExec():
    global nextReaverIdx, reavers
    reaverCount = EUDVariable(0)
    reaverCount << 0
    epd = EUDVariable(0)
    for i in EUDLoopRange(0, SUPPORT_REAVER_MAX):
        if EUDIf()(reavers[i] == 0):
            EUDBreak()
        if EUDElseIf()(reavers[i] == -1):
            EUDContinue()
        EUDEndIf()
        epd << reavers[i]
        orderID = epd + 0x4D // 4 # byte
        hangarCount = epd + 0xC8 // 4 # byte
        if EUDIf()(MemoryXEPD(orderID, Exactly, 0x0000, 0xFF00)): ## 죽은 리버면
            reavers[i] = -1
            nextReaverIdx << i
            if Setting.ReaverFixDebug:
                f_simpleprint('reaver dead. nextReaverIdx is ', nextReaverIdx)
            EUDContinue()
        if EUDElse()():
            reaverCount += 1
            if EUDIf()(EUDNot(MemoryXEPD(orderID, Exactly, 0x1700, 0xFF00))): # 생산중인 상태가 아니고
                if EUDIf()(MemoryXEPD(hangarCount, AtLeast, 2, 0xFF)):
                    lastScarabPtr = f_dwread_epd(epd + 0xC0 //4)
                    if EUDIf()(lastScarabPtr != 0):
                        lastScarabEPD = EPD(lastScarabPtr)
                        lastScarab_removeTimer = lastScarabEPD + 0x110 // 4
                        DoActions(SetMemoryXEPD(lastScarab_removeTimer, SetTo, 0x0001,0xFFFF))
                        if Setting.ReaverFixDebug:
                            f_simpleprint("removeTimer Set 1", lastScarabPtr, lastScarabEPD, lastScarab_removeTimer)
                    EUDEndIf()
                if EUDElseIf()(MemoryXEPD(hangarCount, Exactly, 0, 0xFF)):
                    reaverPosVal = f_dwread_epd(epd + 0x28 // 4)
                    connected_unit = epd + 0x80 // 4
                    if EUDIf()(MemoryEPD(connected_unit, Exactly, 0)): # 셔틀엘 탄 상태는 제외
                        temp = f_dwbreak(reaverPosVal)
                        reaverPosX = temp[0]
                        reaverPosY = temp[1]
                        locOffset = util.GetLocOffset("EUDControlLoc")
                        if Setting.ReaverFixDebug:
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
                        if Setting.ReaverFixDebug:
                            SetCurrentPlayer(0)
                            DoActions([
                                MinimapPing("EUDControlLoc"),
                                CreateUnit(1, "Terran Wraith", "EUDControlLoc", P7),
                                KillUnit("Terran Wraith", P7)
                            ])
                    EUDEndIf()
                EUDEndIf()
            EUDEndIf()
        EUDEndIf()
    #f_simpleprint('reaver count : ', reaverCount)

