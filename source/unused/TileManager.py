from eudplib import *
from BuildingInfo import GetBuildSizeX, GetBuildSizeY

chkt = GetChkTokenized()
MTXM = bytearray(chkt.getsection('MTXM'))
UNIT = bytearray(chkt.getsection('UNIT'))

mapsize=(128,128)
print('MTXM len : ', len(MTXM))
MTXM_STRUCT_SIZE = 2
tileNum = int(len(MTXM) / MTXM_STRUCT_SIZE)
print('tileNum : ' , tileNum)
tileDB = [0]*tileNum
tileCV5 = []
CV5_STRUCT_SIZE = 52
tileVF4 = []
VF4_STRUCT_SIZE = 32
tileSet = []

print('UNIT len : ', len(UNIT))
UNIT_STRUCT_SIZE = 36
print('unit count : ', len(UNIT)/UNIT_STRUCT_SIZE)

#tileDBforInGame = Db(tileNum)
tileDBforInGame = EUDArray(tileNum)
testRange = 1500
def InGameInit():
    for i in range(tileNum):
        tileDBforInGame[i] = tileDB[i]

# 단일인덱스 출력. 안쓸거임
# def VisualizingTileDB(idx):
#     if EUDIf()(tileDBforInGame[idx] & 0x01) == 1:
#         X = (idx%mapsize[0])*32
#         Y = (idx//mapsize[0])*32

#         DoActions([
#             SetMemory(0x58DC60, SetTo, X),
#             SetMemory(0x58DC64, SetTo, Y),
#             SetMemory(0x58DC68, SetTo, X+32),
#             SetMemory(0x58DC6C, SetTo, Y+32),
#             CreateUnit(1,"Terran Marine","Location 0", P1),
#         ])
#     EUDEndIf()

def VisualizingTileDB(start,end):
    i = EUDVariable()
    i << start
    if EUDWhile()(end > i):
        X = (i % mapsize[0])*32
        Y = (i // mapsize[1])*32
        locOffset = EPD(0x58DC60)
        DoActions([
            SetMemoryEPD(locOffset, SetTo, X),
            SetMemoryEPD(locOffset + 1, SetTo, Y),
            SetMemoryEPD(locOffset + 2, SetTo, X+32),
            SetMemoryEPD(locOffset + 3, SetTo, Y+32),
        ])
        if EUDIf()((tileDBforInGame[i] & 0x04) != 0):
            DoActions([
                CreateUnit(1,"Zerg Scourge","GiveMeSCV_EUDLoc", P1),
            ])
        if EUDElseIf()(EUDSCAnd()((tileDBforInGame[i] & 0x02) != 0)(tileDBforInGame[i] & 0x01 != 0)()):
            DoActions([
                CreateUnit(1,"Gui Montag","GiveMeSCV_EUDLoc", P1),
            ])
        if EUDElseIf()((tileDBforInGame[i] & 0x08) != 0):
            DoActions([
                CreateUnit(1,"Samir Duran","GiveMeSCV_EUDLoc", P1),
            ])
        if EUDElseIf()((tileDBforInGame[i] & 0x01) != 0):
            DoActions([
                CreateUnit(1,"Jim Raynor (Marine)","GiveMeSCV_EUDLoc", P1),
            ])
        EUDEndIf()
        

        DoActions([
            KillUnit(EncodeUnit("Jim Raynor (Marine)"),P1),
            KillUnit(EncodeUnit("Gui Montag"),P1),
            KillUnit(EncodeUnit("Zerg Scourge"),P1),
            KillUnit(EncodeUnit("Samir Duran"),P1),
        ])
        i+=1
    EUDEndWhile()

def OnNewBuilding(xmin,ymin,width,height):
    for deltaX in EUDLoopRange(width):
        for deltaY in EUDLoopRange(height):
            tileDBforInGame[(xmin+deltaX) + (ymin+deltaY)*mapsize[0]] |= 0x04
            tileDBforInGame[(xmin+deltaX) + (ymin+deltaY)*mapsize[0]] &= ~0x08
def OnDestroyBuilding(xmin,ymin,width,height):
    for deltaX in EUDLoopRange(width):
        for deltaY in EUDLoopRange(height):
            tileDBforInGame[(xmin+deltaX) + (ymin+deltaY)*mapsize[0]] &= ~0x04
            #f_simpleprint(xmin+deltaX,ymin+deltaY)

# 여기에 지을거니까 영역표시점
def requestBuildArea(buildingID,posX,posY, isBuild):
    buildingWidth = GetBuildSizeX(buildingID)
    buildingHeight = GetBuildSizeY(buildingID)
    checkedTilePosX, checkedTilePosY,curCheckX,curCheckY = EUDCreateVariables(4)
    checkedTilePosX << posX
    checkedTilePosY << posY
    if EUDIf()(buildingWidth == 3):
        checkedTilePosX << posX - 16
    EUDEndIf()
    if EUDIf()(buildingHeight == 3):
        checkedTilePosY << posY - 16
    EUDEndIf()
    checkedTilePosX = checkedTilePosX // 32
    checkedTilePosY = checkedTilePosY // 32

    deltaX = EUDVariable(-1)
    if EUDIf()(buildingWidth == 4):
        deltaX << -2
    EUDEndIf()

    for buildTileX in EUDLoopRange(buildingWidth):
        for buildTileY in EUDLoopRange(buildingHeight):
            curCheckX << checkedTilePosX + buildTileX + deltaX
            curCheckY << checkedTilePosY + buildTileY - 1
            if EUDIf()(isBuild):
                tileDBforInGame[curCheckX + curCheckY*mapsize[0]] |= 0x08
            if EUDElse()():
                tileDBforInGame[curCheckX + curCheckY*mapsize[0]] &= ~0x08
            EUDEndIf()


# 특정위치로부터 특정 건물을 건설할 지점을 계산하여 반환합니다.
@EUDFunc
def GetBuildPosition(building, searchStartPosX, searchStartPosY, findingDepth):
    buildingWidth = GetBuildSizeX(building)
    buildingHeight = GetBuildSizeY(building)
    searchStartTilePosX = (searchStartPosX // 32)
    searchStartTilePosY = (searchStartPosY // 32)
    #f_simpleprint('buildingWidth : ', buildingWidth)
    result = EUDVariable(1)
    deltaX = EUDVariable(-1)
    deltaX << -1
    if EUDIf()(buildingWidth == 4):
        deltaX << -2
    EUDEndIf()
    # 여기부터 tileDB를 보고 건설가능한지 체크합니다.
    curSearchingDepth = EUDVariable(0) # 원위치로부터 얼마나 떨어진 곳에서 조사를 할것인지에 대한 변수
    curSearchingDepth << 0
    curSearchTilePosX, curSearchTilePosY, curCheckX, curCheckY, finalBuildPosX, finalBuildPosY = EUDCreateVariables(6) # 타일조사에 관한 변수.
    if EUDWhile()(curSearchingDepth < findingDepth):
        for xmin in range(-1,2):
            for ymin in range(-1,2):
                
                curSearchTilePosX << searchStartTilePosX + curSearchingDepth*xmin
                curSearchTilePosY << searchStartTilePosY + curSearchingDepth*ymin
                result << 1
                for buildTileX in EUDLoopRange(buildingWidth):
                    for buildTileY in EUDLoopRange(buildingHeight):
                        curCheckX << curSearchTilePosX + buildTileX + deltaX
                        curCheckY << curSearchTilePosY + buildTileY - 1
                        # 디버깅을 위한 시각화 코드
                        # f_simpleprint('check here ',curCheckX,curCheckY, tileDBforInGame[curCheckX + (curCheckY)*mapsize[0]])
                        DoActions([
                            SetMemory(0x58DC60, SetTo, curCheckX*32),
                            SetMemory(0x58DC64, SetTo, curCheckY*32),
                            SetMemory(0x58DC68, SetTo, curCheckX*32+32),
                            SetMemory(0x58DC6C, SetTo, curCheckY*32+32),
                            # CreateUnit(1,"Zerg Scourge","Location 0", P1),
                            # KillUnit(EncodeUnit("Zerg Scourge"),P1),
                            # CreateUnit(1,"Khalis Crystal","Location 0", P1),
                            # KillUnit(EncodeUnit("Khalis Crystal"),P1),
                        ])
                        if EUDIf()(EUDSCOr()
                        ( (tileDBforInGame[curCheckX + curCheckY*mapsize[0]] & 0x01) == 0) # 건설가능한 지형이 아니거나
                        ( (tileDBforInGame[curCheckX + curCheckY*mapsize[0]] & 0x04) != 0) # 이미 지어진 건물자리이거나
                        ( (tileDBforInGame[curCheckX + curCheckY*mapsize[0]] & 0x08) != 0) # 지을 예정인 자리이거나
                        ( curCheckX >= mapsize[0])( curCheckY >= mapsize[1]) # 맵밖을 검사하거나
                        ( EUDSCAnd()
                            ( building == EncodeUnit('Terran Command Center') ) # 커맨드인데
                            ( (tileDBforInGame[curCheckX + curCheckY*mapsize[0]] & 0x02) != 0) # 자원필드에 영향을 받으면
                            ())
                        ()):
                            #f_simpleprint('cant build here', curCheckX, (curCheckY),'value=',tileDBforInGame[curCheckX + (curCheckY)*mapsize[0]])
                            result << 0
                            EUDBreak()
                        EUDEndIf()
                if EUDIf()(result == 1):
                    EUDBreak()
                EUDEndIf()
        curSearchingDepth += 1
    EUDEndWhile()

    #f_simpleprint('result = ', result)
    if EUDIf()(curSearchingDepth < findingDepth):
        finalBuildPosX << curSearchTilePosX*32
        finalBuildPosY << curSearchTilePosY*32
        if EUDIf()(buildingWidth == 3):
            finalBuildPosX += 16
        EUDEndIf()
        if EUDIf()(buildingHeight == 3):
            finalBuildPosY += 16
        EUDEndIf()
        #f_simpleprint('return : ', finalBuildPosX, finalBuildPosY)
        EUDReturn(finalBuildPosX,finalBuildPosY)
    EUDEndIf()
    f_simpleprint('cannot found build position')
    EUDReturn(-1,-1)


# tildDB bit info
# 0x01 : 지형이 허용이 되는가? (허용되면 1, 허용되지않으면 0)
# 0x02 : 자원필드가 있어 특정건물(커맨드센터,해처리,넥서스)을 지을 수 없는 타일인가?(자원필드범위가 있으면 1, 없으면 0)
# 0x04 : 건물이 이미 지어져있는가? (지어져있으면 1, 없으면 0)
# 0x08 : 건물을 지을 예정인가? (지을 예정이면 1, 아니면 0)
def init():
    # CV5 파일분석
    f = open('tileset/Desert.CV5','rb')
    while True:
        obj = f.read(CV5_STRUCT_SIZE)
        if len(obj) < CV5_STRUCT_SIZE:
            #print('end of file : ' , len(obj))
            break
        for i in range(20,52,2):
            tileSet.append(int.from_bytes(obj[i:i+2],byteorder='little',signed=False))
        #print()

        tileCV5.append(obj)
    #print('tileCV5 read', len(tileCV5))

    #print('tileSet len : ', len(tileSet))

    f = open('tileset/Desert.VF4','rb')
    while True:
        obj = f.read(VF4_STRUCT_SIZE)
        if len(obj) < VF4_STRUCT_SIZE:
            #print('end of file : ' , len(obj))
            break
        tileVF4.append(obj)
    #print('tileVF4 read', len(tileVF4))

    ## MTXM으로부터 tileDB 초기화
    tempPrintCount = 10
    for i in range(0, len(MTXM), MTXM_STRUCT_SIZE):
        megaTileIndexByteArray = MTXM[i:i+2]
        megaTileIndex = int.from_bytes(megaTileIndexByteArray,byteorder='little',signed=False)
        megaTileRowIndex = int(megaTileIndex / 16)
        buildable = tileCV5[megaTileRowIndex][2] >> 4 == 0
        mapTileIndex = i >> 1
        # if tempPrintCount > 0:
        #     tempPrintCount-=1
        #     print(buildable)

        # minitile까지 고려한 buildable 검사
        # megaTile References
        tileIndex = tileSet[megaTileIndex]
        miniTileInfos = tileVF4[tileIndex]
        megaTileBuildable = True
        for j in range(0,32,2):
            minitileInfoByteArray = miniTileInfos[j:j+2]
            minitileInfo = int.from_bytes(minitileInfoByteArray,byteorder='little',signed=False)
            if (minitileInfo & 0x01) == 0:
                megaTileBuildable = False
                break
        if tempPrintCount > 0:
            tempPrintCount-=1
            # print("megaTileIndex = ",megaTileIndex, "index = ", tileIndex, "len = ", len(miniTileInfos))
            # print(miniTileInfos)
            # print(megaTileBuildable)
        mapTileIndex = i >> 1
        if buildable and megaTileBuildable:
            tileDB[mapTileIndex] |= 0x01
        else:
            tileDB[mapTileIndex] &= ~0x01

    # 자원필드 정보초기화
    for i in range(0, len(UNIT), UNIT_STRUCT_SIZE):
        unitID = int.from_bytes(UNIT[i+8:i+10],byteorder='little',signed=False)
        if unitID == EncodeUnit("Mineral Field (Type 1)") or unitID == EncodeUnit("Mineral Field (Type 2)") or unitID == EncodeUnit("Mineral Field (Type 3)"):
            posX = int.from_bytes(UNIT[i+4:i+6],byteorder='little',signed=False)
            posY = int.from_bytes(UNIT[i+6:i+8],byteorder='little',signed=False)
            tileX = posX // 32
            tileY = posY // 32
            # 자원부분은 절대로 못지음
            tileDB[tileX-1 + tileY*mapsize[0]] &= ~0x01
            tileDB[tileX+0 + tileY*mapsize[0]] &= ~0x01
            # 자원주위 커맨드,해처리,넥서스 못지음
            for y in range(-3,4):
                for x in range(-4,4):
                    finalX = max(min(tileX+x, mapsize[0]-1), 0)
                    finalY = max(min(tileY+y, mapsize[1]-1), 0)
                    tileDB[finalX + finalY*mapsize[0]] |= 0x02
                    #print('[',x,',',y,']')
            # 두번째줄
            # tileDB[tileX-4 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-3 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-2 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-1 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX-0 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX+1 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX+2 + (tileY-3)*mapsize[0]] |= 0x02
            # tileDB[tileX+3 + (tileY-3)*mapsize[0]] |= 0x02

        elif unitID == EncodeUnit("Vespene Geyser"):
            posX = int.from_bytes(UNIT[i+4:i+6],byteorder='little',signed=False)
            posY = int.from_bytes(UNIT[i+6:i+8],byteorder='little',signed=False)
            tileX = posX // 32
            tileY = posY // 32
            #자원부분은 절대로 못지음
            tileDB[tileX-2 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX-1 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX-0 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX+1 + (tileY-1)*mapsize[0]] &= ~0x01
            tileDB[tileX-2 + (tileY+0)*mapsize[0]] &= ~0x01
            tileDB[tileX-1 + (tileY+0)*mapsize[0]] &= ~0x01
            tileDB[tileX-0 + (tileY+0)*mapsize[0]] &= ~0x01
            tileDB[tileX+1 + (tileY+0)*mapsize[0]] &= ~0x01
            # 자원주위 커맨드,해처리,넥서스 못지음
            for y in range(-4,4):
                for x in range(-5,5):
                    tileDB[tileX+x + (tileY+y)*mapsize[0]] |= 0x02

    print('tileDB sample')
    for i in range(128,128+256+128):
        #print('[',i,']',tileDB[i])
        print(tileDB[i],end=' ')
    