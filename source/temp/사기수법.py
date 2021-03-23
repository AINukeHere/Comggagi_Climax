from eudplib import *

def beforeTriggerExec():
    if EUDIf()(ElapsedTime(AtLeast, 10)):
        for ptr, epd in EUDLoopUnit2():
            unitType = epd + 0x64 // 4
            orderID = epd + 0x4D // 4
            targetPtr = epd + 0x5C // 4
            if EUDIf()(EUDSCOr()
            (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Zergling")))
            (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Hydralisk")))
            (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Ultralisk")))
            (MemoryEPD(unitType, Exactly, EncodeUnit("Zerg Defiler")))
            ()):
                DoActions([
                    SetMemoryXEPD(orderID, SetTo, 0x2F00, 0xFF00),
                    SetMemoryEPD(targetPtr, SetTo, 0x59CCA8)
                ])
            EUDEndIf()
    EUDEndIf()