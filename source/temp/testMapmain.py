from eudplib import *
import math
def CUnit(idx):
    if idx == 0:
        return 0x59CCA8
    else:
        return 0x628298 - 0x150*(idx-1)
def beforeTriggerExec():
    for ptr, epd in EUDLoopUnit():
        if EUDIf()(EUDSCAnd()
        (MemoryXEPD(epd+0x4C //4 , Exactly, 5, 0xFF))
        (MemoryEPD(epd + 0x64 // 4, Exactly, 176))
        ()):
            f_simpleprint("gived")
            DoActions([
                SetMemoryXEPD(epd+0x4C // 4, SetTo, 11, 0xFF)
            ])
        EUDEndIf()