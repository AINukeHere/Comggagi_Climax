from eudplib import *
import BuildingInfo
import TileManager
import JobManager

newCUnit = EUDArray(1700 * 336)
epd2newCUnit = EPD(newCUnit) - EPD(0x59CCA8)

def main():
    # 새로운유닛루프를 돌면서 건물이 지어지면 타일DB 업데이트
    for ptr,epd in LoopNewUnit():
        unitTypeEPD = epd + 0x64 // 4
        unitType = f_dwread_epd(unitTypeEPD)
        if EUDIf()(unitType == EncodeUnit("Terran SCV")):
            # secondaryOrderPosition // unused -> 배정된 Job 인덱스를 저장
            assignedJobIndex = epd + 0xE8 // 4
            DoActions(SetMemoryEPD(assignedJobIndex, SetTo, -1)) # 초기값 -1 (배정되지않음)
            f_simpleprint('0xE8 = -1')
        EUDEndIf()

        statusFlags = epd + 0xDC //4
        # 지상건물에 대해서
        if EUDIf()(MemoryXEPD(statusFlags, AtLeast, 1, 2)):
            #unused_0x8C -> 죽음상태플래그 0이면 생존 1이면 사망
            deathFlag = epd + 0x8C // 4
            DoActions(SetMemoryXEPD(deathFlag, SetTo, 0, 0xFFFF)) # 초기값 0 (죽지않은 상태)

            # 광물지대도 인식되어버리므로 예외처리
            EUDContinueIf(EUDSCOr()
            (unitType == EncodeUnit('Mineral Field (Type 1)'))
            (unitType == EncodeUnit('Mineral Field (Type 2)'))
            (unitType == EncodeUnit('Mineral Field (Type 3)'))
            (unitType == EncodeUnit('Vespene Geyser'))
            ())

            unitPosX_EPD = epd + 0x28 //4
            unitPosY_EPD = epd + 0x2A //4
            unitPosX = f_wread_epd(unitPosX_EPD, 0)
            unitPosY = f_wread_epd(unitPosY_EPD, 2)
            buildSizeX = BuildingInfo.GetBuildSizeX(unitType)
            buildSizeY = BuildingInfo.GetBuildSizeY(unitType)
            buildingXmin = (unitPosX // 32) - buildSizeX // 2
            buildingYmin = (unitPosY // 32) - buildSizeY // 2
            TileManager.OnNewBuilding(buildingXmin,buildingYmin,buildSizeX,buildSizeY)
        EUDEndIf()

    # 전체 유닛루프
    for ptr, epd in EUDLoopUnit2():
        orderID = epd + 0x4D // 4
        statusFlags = epd + 0xDC //4
        #unused_0x8C
        deathFlag = epd + 0x8C // 4
        orderIDValue = f_bread_epd(orderID, 0x4D % 4)
        # 유닛이 파괴되었을 경우
        if EUDIf()(EUDSCAnd()
        (orderIDValue == 0)
        (MemoryXEPD(statusFlags, AtLeast, 1, 2))
        ()):
            if EUDIfNot()(MemoryXEPD(deathFlag, Exactly, 1, 0xFFFF)):
                DoActions(SetMemoryXEPD(deathFlag, SetTo, 1, 0xFFFF))
                f_simpleprint('Destory Ground Building')
                unitPosX_EPD = epd + 0x28 //4
                unitPosY_EPD = epd + 0x2A //4
                unitPosX = f_wread_epd(unitPosX_EPD, 0)
                unitPosY = f_wread_epd(unitPosY_EPD, 2)
                unitTypeEPD = epd + 0x64 // 4
                unitType = f_dwread_epd(unitTypeEPD)
                buildSizeX = BuildingInfo.GetBuildSizeX(unitType)
                buildSizeY = BuildingInfo.GetBuildSizeY(unitType)
                buildingXmin = (unitPosX // 32) - buildSizeX // 2
                buildingYmin = (unitPosY // 32) - buildSizeY // 2
                TileManager.OnDestroyBuilding(buildingXmin,buildingYmin,buildSizeX,buildSizeY)
            EUDEndIf()
        EUDEndIf()
        JobManager.OnUnitLooping(epd)
    JobManager.OnUnitLoopEnd()



def LoopNewUnit(allowance=2):
    firstUnitPtr = EPD(0x628430)
    EUDCreateBlock("newunitloop", "newlo")
    tos0 = EUDLightVariable()
    tos0 << 0

    ptr, epd = f_cunitepdread_epd(firstUnitPtr)
    if EUDWhile()(ptr >= 1):
        tos1 = f_bread_epd(epd + 0xA5 // 4, 1)
        global epd2newCUnit
        tos2 = epd + epd2newCUnit
        if EUDIfNot()(MemoryEPD(tos2, Exactly, tos1)):
            DoActions(SetMemoryEPD(tos2, SetTo, tos1))
            yield ptr, epd
        if EUDElse()():
            DoActions(tos0.AddNumber(1))
            EUDBreakIf(tos0.AtLeast(allowance))
        EUDEndIf()
        EUDSetContinuePoint()
        f_cunitepdread_epd(epd + 1, ret=[ptr, epd])
    EUDEndWhile()

    EUDPopBlock("newunitloop")