import util
from eudplib import *
def detectTimingRush():
    bDetectBegin = EUDVariable(0)

    if EUDIf()(EUDSCOr()
    (EUDSCAnd()
    (Bring(Force1, AtLeast, 25, "Men","LeftAttackRoute1"))
    (Bring(Force1, AtMost, 20, "Spider Mine","LeftAttackRoute1"))
    ())
    (Bring(Force1, AtLeast, 45, "Men","LeftAttackRoute1"))
    ()):
        DoActions(SetDeaths(P7, SetTo, 1, "Flag"))
    if EUDElseIf()(EUDSCOr()
    (EUDSCAnd()
    (Bring(Force1, AtLeast, 25, "Men","LeftAttackRoute2"))
    (Bring(Force1, AtMost, 20, "Spider Mine","LeftAttackRoute2"))
    ())
    (Bring(Force1, AtLeast, 45, "Men","LeftAttackRoute2"))
    ()):
        DoActions(SetDeaths(P7, SetTo, 2, "Flag"))
    if EUDElseIf()(EUDSCOr()
    (EUDSCAnd()
    (Bring(Force1, AtLeast, 25, "Men","RightAttackRoute1"))
    (Bring(Force1, AtMost, 20, "Spider Mine","RightAttackRoute1"))
    ())
    (Bring(Force1, AtLeast, 45, "Men","RightAttackRoute1"))
    ()):
        DoActions(SetDeaths(P7, SetTo, 3, "Flag"))
    if EUDElseIf()(EUDSCOr()
    (EUDSCAnd()
    (Bring(Force1, AtLeast, 25, "Men","RightAttackRoute2"))
    (Bring(Force1, AtMost, 20, "Spider Mine","RightAttackRoute2"))
    ())
    (Bring(Force1, AtLeast, 45, "Men","RightAttackRoute2"))
    ()):
        DoActions(SetDeaths(P7, SetTo, 4, "Flag"))
    if EUDElse()():
        DoActions(SetDeaths(P7, SetTo, 0, "Flag"))
        bDetectBegin << 0
    EUDEndIf()

    # 첫번째로 러쉬가 인식되었다면 방어하러갈 위치를 최하단으로 내림
    if EUDIf()(EUDSCAnd()
    (bDetectBegin == 0)
    (Deaths(P7, AtLeast, 1, "Flag"))
    ()):
        bDetectBegin << 1
        locOffset = util.GetLocOffset("TimingRushDefenseArea")
        if EUDIf()(Deaths(P7, Exactly, 1, "Flag")):
            DoActions([
                MoveLocation("TimingRushDefenseArea", "Terran Marker", P12, "LeftAttackRoute1"),
                SetMemoryEPD(locOffset + 1, SetTo, 3712),
                SetMemoryEPD(locOffset + 3, SetTo, 4096)
            ])
        if EUDElseIf()(Deaths(P7, Exactly, 2, "Flag")):
            DoActions([
                MoveLocation("TimingRushDefenseArea", "Terran Marker", P12, "LeftAttackRoute2"),
                SetMemoryEPD(locOffset + 1, SetTo, 2752),
                SetMemoryEPD(locOffset + 3, SetTo, 3136)
            ])
        if EUDElseIf()(Deaths(P7, Exactly, 3, "Flag")):
            DoActions([
                MoveLocation("TimingRushDefenseArea","Terran Marker", P12, "RightAttackRoute1"),
                SetMemoryEPD(locOffset + 1, SetTo, 2752),
                SetMemoryEPD(locOffset + 3, SetTo, 3136)
            ])
        if EUDElseIf()(Deaths(P7, Exactly, 4, "Flag")):
            DoActions([
                MoveLocation("TimingRushDefenseArea","Terran Marker", P12, "RightAttackRoute2"),
                SetMemoryEPD(locOffset + 1, SetTo, 3712),
                SetMemoryEPD(locOffset + 3, SetTo, 4096)
            ])
        EUDEndIf()
        DoActions([
            Order("Protoss Reaver", P7, "RightAttackRoute1", Attack, "TimingRushDefenseArea"),
            Order("Protoss Reaver", P7, "RightAttackRoute2", Attack, "TimingRushDefenseArea")
        ])
    EUDEndIf()

    # 가장 아래에 있는 적을 찾음
    if EUDIf()(Bring(Force1, AtMost, 5, "Men", "TimingRushDefenseArea")):
        if EUDIf()(MemoryEPD(locOffset +  1, AtMost, 1568)):
            bDetectBegin << 0
        EUDEndIf()
        DoActions([
            SetMemoryEPD(locOffset + 1, Subtract, 32),
            SetMemoryEPD(locOffset + 3, Subtract, 32)
        ])
    EUDEndIf()
