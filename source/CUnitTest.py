import customText as ct
from eudplib import *


def onPluginStart():
    global idptr, idlen
    idptr = 0x57EEEB + 36 * ct.cp
    idlen = f_strlen(idptr)


txtPtr = EUDVariable()
msg = EUDVariable()
msgList = [
    "'f",  # Fix
    "'n",  # getNextPtr
    "'s",  # SaveMem
    "'g",  # GetMem
]


def afterTriggerExec():
    global txtPtr
    if EUDIfNot()(Memory(0x640B58, Exactly, txtPtr)):
        f_detectMsg()
    EUDEndIf()
    f_main()
    f_dwwrite_epd(EPD(0x640B58), txtPtr)


def f_detectMsg():
    ptr = EUDVariable(0x640B60)
    global txtPtr, msg, msgList, idptr, idlen
    msg << -1
    if EUDWhileNot()(Memory(0x640B58, Exactly, txtPtr)):
        EUDContinueIfNot(f_memcmp(ptr, idptr, idlen) == 0)
        dst = ptr + idlen + 3
        for i, m in enumerate(msgList):
            b = u2utf8(m)
            if EUDIf()(f_memcmp(dst, Db(b), len(b)) == 0):
                msg << i
                EUDContinue()
            EUDEndIf()
        EUDSetContinuePoint()
        DoActions([txtPtr.AddNumber(1), ptr.AddNumber(218)])
        Trigger(txtPtr.AtLeast(11), [
            txtPtr.SetNumber(0), ptr.SetNumber(0x640B60)])
    EUDEndWhile()


@EUDFunc
def f_CUnitMember(offset):
    members = [
        "\x150\x170\x11ＰＲＥＶ\x19ｕｎｉｔ",
        "\x150\x174\x0FＮＥＸＴ\x19ｕｎｉｔ",
        "\x150\x178\x08Ｈｉｔ\x03Ｐ\x07ｏｉｎｔ",
        "\x150\x07c\x15Ｃ\x0EＳ\x1Cｐ\x17ｒ\x0Fｉ\x1Dｔ\x18ｅ　",
        "\x1710\x10ｍｏｖ\x08Ｔ\x04ａ\x08ｒ\x04ｇ\x08ｔ",
        "\x1714\x19ｍｏｖ\x08Ｔ\x04ａ\x08ｒ\x04ｇ\x08ｔ",
        "\x1718\x10ｎｘｔ\x03Ｍｏｖ\x1FＷ\x1BＰ",
        "\x171\x07c\x10ｎｘｔ\x08Ｔ\x04ｇ\x08ｔ\x1FＷ\x1BＰ",
        "\x1720\x04ｍｏ\x08ｖｍ\x0EＦｌ\x04ａｇ",
        "\x1724\x0Fｆｌｉｎ\x15ｇｙ\x04ＩＤ",
        "\x1728\x10Ｐｏｓｉｔｉｏｎ",
        "\x172\x07c\x08ｄｗＸ\x04＿\x10Ｈａｌｔ",
        "\x1730\x0EｄｗＹ\x04＿\x10Ｈａｌｔ",
        "\x1734\x0Fｆｌｎｇｙ\x07Ｓｐｄ",
        "\x1738\x0Fｃｒ\x07Ｓｐｅｅｄ\x08１",
        "\x173\x07c\x0Fｃｒ\x07Ｓｐｅｅｄ\x0E２",
        "\x1740\x08ｄｗＸ\x0Fｃｒ\x07Ｓｐｄ",
        "\x1744\x0EｄｗＸ\x0Fｃｒ\x07Ｓｐｄ",
        "\x1748\x0Fｆｌｇ\x1FＡＣＣＥＬ",
        "\x174\x07c\x08ｐｌ\x0Eａｙ\x0Fｅｒ\x10ＩＤ",
        "\x1750\x19ｏｒｄ\x16Ｕｎｔ\x1BＴｙ",
        "\x1754\x04ｍ\x16Ｏｒｄ\x1DＴｉｍｅ",
        "\x1758\x10ｏｒｄ\x08Ｔ\x04ａ\x08ｒ\x04ｇ\x08ｔ",
        "\x175\x07c\x19ｏｒｄ\x08Ｔ\x04ａ\x08ｒ\x04ｇ\x08ｔ",
        "\x1760\x02Ｓｈｉｅｌｄ\x07Ｐｏ",
        "\x1764\x19Ｕｎｉｔ\x1BＴｙｐｅ",
        "\x1768\x11ＰＲＥＶ\x08Ｐ\x19ｕｎｔ",
        "\x176\x07c\x0FＮＥＸＴ\x08Ｐ\x19ｕｎｔ",
        "\x1770\x1FＳＵＢ\x19ｕｎｉｔ　",
        "\x1774\x16ｏｒｄ\x18Ｑ\x08Ｈ\x0Eｅ\x0Fａ\x10ｄ",
        "\x1778\x16ｏｒｄ\x18ＱＴ\x19ａ\x1Bｉ\x1Cｌ",
        "\x177\x07c\x19ａｕｔｏ\x08Ｔ\x04ｇ\x08ｔ\x19Ｕ",
        "\x1780\x19Ｃｏｎｅｃｔ\x03Ｕｎ",
        "\x1784\x16ｏｒｄ\x18Ｑ\x15Ｃ\x11ｏｕｔ",
        "\x1788\x11ＰＲＥＶ\x19Ｕｎ\x1BＴｙ",
        "\x178\x07c\x1E＿ＵＮ\x04ＵＳＥＤ\x1E＿",
        "\x1790\x1DＬａｓｔ\x04Ａ\x03ｔｋ\x08Ｐ",
        "\x1794\x0Fｃｒ\x1CＢｔｎ\x04ｓｅｔ",
        "\x1798\x04Ｂ\x03ｕｉｌｄ\x18Ｑ\x08０\x0E１",
        "\x179\x07c\x04Ｂ\x03ｕｉｌｄ\x18Ｑ\x0F２\x10３",
        "\x07a\x170\x04Ｂ\x03ｄ\x18Ｑ\x11４\x04ＥｎｅＧ",
        "\x07a\x174\x04Ｂ\x03ｌｄ\x18Ｑ\x1FＳｌｏｔ",
        "\x07a\x178\x08ｈｐ\x1Fｓｐ\x0FＧａｉｎ",
        "\x07ac\x11ｒｅｍａｉｎ\x04Ｂ\x1DＴ",
        "\x07b\x170\x04Ｌ\x03ｏａｄ\x19Ｕｎ\x08０\x0E１",
        "\x07b\x174\x04Ｌ\x03ｏａｄ\x19Ｕｎ\x0F２\x10３",
        "\x07b\x178\x04Ｌ\x03ｏａｄ\x19Ｕｎ\x11４\x15５",
        "\x07bc\x04Ｌ\x03ｏａｄ\x19Ｕｎ\x16６\x17７",
        "\x07c\x170\x1Fｕ０\x08ｓｐｉ\x0Eｄｅｒ",
        "\x07c\x174\x1Fｕ１\x08Ｔ\x04ｇ\x08ｔ\x1FＲ\x07ｅｓ",
        "\x07c\x178\x1Fｕ２\x08Ｔ\x04ｇ\x08ｔ\x19Ｒｅｓ",
        "\x07cc\x1Fｕ３\x10Ｃｒｅｅｐ\x1DＴ",
        "\x07d\x170\x1Fｕ０Ｒ\x07ｅｓ\x11Ｃｎｔ",
        "\x07d\x174\x1Fｕ１\x04Ｇ\x03ａｔｈｅｒ",
        "\x07d\x178\x1Fｕ２Ｒ\x07ｅｓ\x18Ｇｒｐ",
        "\x07dc\x04Ｓｔ\x08ｔｓ\x0EＦｌ\x04ａｇ",
        "\x07e\x170\x1FＲ\x07ｓｒｃ\x1BＴｙｐｅ",
        "\x07e\x174\x1FＶｉｓｉｂｌ\x04Ｓｔ",
        "\x07e\x178\x0E２ｎｄ\x16Ｏｒ\x10Ｐｏｓ",
        "\x07ec\x0Fｃｒ\x04Ｂ\x03ｌｄ\x19Ｕｎｔ",
        "\x07f\x170\x11ＰＲ\x04Ｂ\x03ｕｒｗ\x19Ｕｎ",
        "\x07f\x174\x0FＮＸ\x04Ｂ\x03ｕｒｗ\x19Ｕｎ",
        "\x07f\x178\x11ＰＲ\x04Ｐｓｉ\x1FＰｒｖ",
        "\x07fc\x0FＮＸ\x04Ｐｓｉ\x1FＰｒｖ",
        "\x1F00\x04ｕｎｉｔ\x1BＰＡＴＨ",
        "\x1F04\x1BＰＡＴＨＩＮＧ\x07ｈ",
        "\x1F08\x02ｃｏｎｔｕ\x08Ｂｎｄ",
        "\x1F0c\x02ｃｏｎｔｕ\x0EＢｎｄ",
        "\x1F10\x08Ｒｅｍｏｖｅ\x1DＴｉ",
        "\x1F14\x04ｄＭａｔｒｉｘ\x1DＴ",
        "\x1F18\x07Ｉｒｒａｄｉ\x18８\x1DＴ",
        "\x1F1c\x19Ｉｒａｄｉ\x18８\x08Ｂｙ",
        "\x1F20\x07Ｉｒｒａｄｉ\x18８\x08Ｐ",
        "\x1F24\x11Ｍａｅｌｓｔｍ\x1DＴ",
        "\x1F28\x17Ａ\x07ｃｉｄＳｐ\x11４\x1DＴ",
        "\x1F2c\x17Ａ\x07ｃｉｄＳｐ\x11４\x1DＴ",
        "\x1F30\x08Ｂｕｌｌｅｔ\x0F３\x10３",
        "\x1F34\x11＊ｐｏｉｎｔ\x04ＡＩ",
        "\x1F38\x02Ａｉｒ\x18Ｇｒ\x08ＳＴＲ",
        "\x1F3c\x10Ｐｏｓ\x07Ｓｒｔ\x08Ｘ\x0FＬ",
        "\x1F40\x10Ｐｏｓ\x07Ｓｒｔ\x08Ｘ\x10Ｒ",
        "\x1F44\x10Ｐｏｓ\x07Ｓｒｔ\x0EＹ\x0FＴ",
        "\x1F48\x10Ｐｏｓ\x07Ｓｒｔ\x0EＹ\x10Ｂ",
        "\x1F4c\x04Ｒ\x1Fｅｐｕｌｓｅ\x04ｓ"
    ]
    EUDSwitch(offset)
    for i, txt in enumerate(members):
        EUDSwitchCase()(i)
        ct.f_addText(txt)
        EUDBreak()
    EUDEndSwitch()


def MouseX(Modifier, Value):
    return Memory(0x6CDDC4, Modifier, Value)


def MouseY(Modifier, Value):
    return Memory(0x6CDDC8, Modifier, Value)


def PressShift():
    return MemoryX(0x596A28, Exactly, 1, 1)


@EUDFunc
def f_colorByValue(epd):
    if EUDIf()(MemoryEPD(epd, Exactly, 0)):
        ct.f_addText("\x15")
    if EUDElse()():
        ct.f_addText("\x16")
    EUDEndIf()


def f_main():
    ptr, epd = EUDVariable(0x59CCA8), EUDVariable(EPD(0x59CCA8))
    ptrStack = EUDArray(99)
    stackPos = EUDVariable()
    lastPtr, lastEpd = EUDCreateVariables(2)

    view = [
        EUDVariable(0x0C // 4), EUDVariable(0x4C // 4), EUDVariable(0x58 // 4),
        EUDVariable(0x64 // 4), EUDVariable(0x80 // 4), EUDVariable(0xA4 // 4),
        EUDVariable(0xC4 // 4), EUDVariable(0xDC // 4), EUDVariable(0x120 // 4)
    ]
    fixed = EUDLightVariable()
    mouseButton = EUDLightVariable()
    Trigger(Memory(0x6CDDC0, Exactly, 0), mouseButton.SetNumber(1))

    def LeftClicked():
        return [mouseButton.Exactly(1), MemoryX(0x6CDDC0, AtLeast, 1, 2)]

    def RightClicked():
        return [mouseButton.Exactly(1), MemoryX(0x6CDDC0, AtLeast, 1, 8)]

    nextptr, nextepd, _n = EUDVariable(), EUDVariable(), Forward()
    if EUDIfNot()([_n << Memory(0x628438, Exactly, 0)]):
        SetVariables([nextptr, nextepd], f_cunitepdread_epd(EPD(0x628438)))
        DoActions(SetMemory(_n + 8, SetTo, nextptr))
    EUDEndIf()

    @EUDFunc
    def SaveToMemory():
        nonlocal stackPos
        stackPos += 1
        Trigger(stackPos.AtLeast(ptrStack.length), stackPos.SetNumber(0))
        f_dwwrite_epd(EPD(ptrStack) + stackPos, ptr)
        SetVariables([lastPtr, lastEpd], [ptr, epd])

    @EUDFunc
    def getNextPtr():
        if EUDIf()(nextptr >= 0x59CCA8):
            SaveToMemory()
            SetVariables([ptr, epd], [nextptr, nextepd])
        EUDEndIf()

    @EUDFunc
    def GetMemory():
        nonlocal stackPos
        if EUDIf()(lastPtr == 0):
            EUDReturn()
        EUDEndIf()
        SetVariables([ptr, epd], [lastPtr, lastEpd])
        Trigger(stackPos.Exactly(0), stackPos.SetNumber(99))
        stackPos -= 1
        SetVariables([lastPtr, lastEpd], f_cunitepdread_epd(EPD(ptrStack) + stackPos))

    global msg, msgList
    if EUDIfNot()(msg == -1):
        EUDSwitch(msg)
        if EUDSwitchCase()(msgList.index("'f")):  # Fix
            DoActions(fixed.AddNumberX(1, 1))
            EUDBreak()
        if EUDSwitchCase()(msgList.index("'n")):  # getNextPtr
            getNextPtr()
            EUDBreak()
        if EUDSwitchCase()(msgList.index("'s")):  # SaveToMemory
            SaveToMemory()
            EUDBreak()
        if EUDSwitchCase()(msgList.index("'g")):  # GetMemory
            GetMemory()
            EUDBreak()
        EUDEndSwitch()
        msg << -1
    EUDEndIf()

    if EUDIf()([fixed == 0, Memory(0x6284B8, AtLeast, 0x59CCA8)]):
        if EUDIfNot()(Memory(0x6284B8, Exactly, ptr)):
            SetVariables([ptr, epd], f_cunitepdread_epd(EPD(0x6284B8)))
        EUDEndIf()
    EUDEndIf()

    ct.f_makeText("　　　　\x1FＰＴＲ　　")
    if EUDIf()(fixed >= 1):
        ct.f_addText("\x08")
    if EUDElseIf()([
        MouseX(AtMost, 212),
        MouseY(AtLeast, 110),
        MouseY(AtMost, 125),
    ]):
        if EUDIf()(LeftClicked()):
            SaveToMemory()
        if EUDElseIf()(RightClicked()):
            DoActions(fixed.AddNumberX(1, 1))
        EUDEndIf()
        ct.f_addText("\x1F")
    if EUDElse()():
        f_colorByValue(EPD(ptr.getValueAddr()))
    EUDEndIf()
    ct.f_addText(hptr(ptr), "\x1F/　　\x11ＭＥＭＯＲＹ　")
    memEpd = EPD(ptrStack) + stackPos
    if EUDIf()([
        MouseX(AtLeast, 213),
        MouseX(AtMost, 425),
        MouseY(AtLeast, 110),
        MouseY(AtMost, 125),
    ]):
        if EUDIf()(LeftClicked()):
            GetMemory()
        EUDEndIf()
        ct.f_addText("\x1F")
    if EUDElse()():
        f_colorByValue(memEpd)
    EUDEndIf()
    ct.f_addText(hptr(f_dwread_epd(memEpd)), "\x1F/\x0FＮＥＸＴ\x1FＰＴＲ")
    if EUDIf()([
        MouseX(AtLeast, 426),
        MouseX(AtMost, 638),
        MouseY(AtLeast, 110),
        MouseY(AtMost, 125),
    ]):
        if EUDIf()(LeftClicked()):
            getNextPtr()
        EUDEndIf()
        ct.f_addText("\x1F")
    if EUDElse()():
        f_colorByValue(EPD(nextptr.getValueAddr()))
    EUDEndIf()
    ct.f_addText(hptr(nextptr), "\n")

    EUDIf()(ptr >= 0x59CCA8)
    colorSwitch = EUDLightVariable()
    for i, v in enumerate(view):
        colorSwitch << 1
        f_CUnitMember(v)
        if EUDIf()([
            MouseX(AtLeast, 213 * (i % 3)),
            MouseX(AtMost, 213 * (i % 3) + 212),
            MouseY(AtLeast, 126 + 16 * (i // 3)),
            MouseY(AtMost, 141 + 16 * (i // 3)),
        ]):
            if EUDIf()(LeftClicked()):
                Trigger(v.Exactly(0), v.SetNumber(84))
                if EUDIf()(PressShift()):
                    v -= 10
                if EUDElse()():
                    v -= 1
                EUDEndIf()
            if EUDElseIf()(RightClicked()):
                if EUDIf()(PressShift()):
                    v += 10
                if EUDElse()():
                    v += 1
                EUDEndIf()
                Trigger(v.AtLeast(84), v.SubtractNumber(84))
            EUDEndIf()
            ct.f_addText("\x1F")
            colorSwitch << 0
        EUDEndIf()

        EUDSwitch(v)
        if EUDSwitchCase()(29, 30, 34, 44, 45, 46, 47, 60, 61, 62, 63, 64, 65, 66, 67, 76, 77, 78, 79, 80, 81, 82):
            ct.f_addText("\x0800000000")
            EUDBreak()
        if EUDSwitchDefault()():
            dst = epd + v
            if EUDIf()(colorSwitch == 1):
                f_colorByValue(dst)
            EUDEndIf()
            ct.f_addText(hptr(f_dwread_epd(dst)))
        EUDEndSwitch()

        if i % 3 < 2:
            ct.f_addText("\x1F/")
        else:
            ct.f_addText("\n")
    EUDEndIf()
    ct.f_displayTextAll()

    Trigger(Memory(0x6CDDC0, AtLeast, 1), mouseButton.SetNumber(0))
