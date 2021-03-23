from eudplib import *

buildingInfo = EUDArray(228*2)
def init():
    global buildingInfo
    # 4x3
    buildingInfo[2*EncodeUnit('Terran Command Center') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Command Center') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Barracks') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Barracks') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Factory') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Factory') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Starport') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Starport') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Science Facility') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Science Facility') + 1] = 3
    buildingInfo[2*EncodeUnit('Terran Engineering Bay') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Engineering Bay') + 1] = 3
    buildingInfo[2*EncodeUnit('Protoss Nexus') + 0] = 4
    buildingInfo[2*EncodeUnit('Protoss Nexus') + 1] = 3
    buildingInfo[2*EncodeUnit('Protoss Gateway') + 0] = 4
    buildingInfo[2*EncodeUnit('Protoss Gateway') + 1] = 3
    buildingInfo[2*EncodeUnit('Protoss Stargate') + 0] = 4
    buildingInfo[2*EncodeUnit('Protoss Stargate') + 1] = 3
    buildingInfo[2*EncodeUnit('Zerg Hatchery') + 0] = 4
    buildingInfo[2*EncodeUnit('Zerg Hatchery') + 1] = 3
    buildingInfo[2*EncodeUnit('Zerg Lair') + 0] = 4
    buildingInfo[2*EncodeUnit('Zerg Lair') + 1] = 3
    buildingInfo[2*EncodeUnit('Zerg Hive') + 0] = 4
    buildingInfo[2*EncodeUnit('Zerg Hive') + 1] = 3

    # 4x2
    buildingInfo[2*EncodeUnit('Terran Refinery') + 0] = 4
    buildingInfo[2*EncodeUnit('Terran Refinery') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Assimilator') + 0] = 4
    buildingInfo[2*EncodeUnit('Protoss Assimilator') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Defiler Mound') + 0] = 4
    buildingInfo[2*EncodeUnit('Zerg Defiler Mound') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Extractor') + 0] = 4
    buildingInfo[2*EncodeUnit('Zerg Extractor') + 1] = 2
    # 3x2
    buildingInfo[2*EncodeUnit('Terran Supply Depot') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Supply Depot') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Academy') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Academy') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Armory') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Armory') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Bunker') + 0] = 3
    buildingInfo[2*EncodeUnit('Terran Bunker') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Forge') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Forge') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Cybernetics Core') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Cybernetics Core') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Shield Battery') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Shield Battery') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Robotics Facility') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Robotics Facility') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Citadel of Adun') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Citadel of Adun') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Robotics Support Bay') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Robotics Support Bay') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Fleet Beacon') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Fleet Beacon') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Templar Archives') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Templar Archives') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Observatory') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Observatory') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Arbiter Tribunal') + 0] = 3
    buildingInfo[2*EncodeUnit('Protoss Arbiter Tribunal') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Evolution Chamber') + 0] = 3
    buildingInfo[2*EncodeUnit('Zerg Evolution Chamber') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Hydralisk Den') + 0] = 3
    buildingInfo[2*EncodeUnit('Zerg Hydralisk Den') + 1] = 2
    buildingInfo[2*EncodeUnit("Zerg Queen's Nest") + 0] = 3
    buildingInfo[2*EncodeUnit("Zerg Queen's Nest") + 1] = 2
    buildingInfo[2*EncodeUnit("Zerg Spawning Pool") + 0] = 3
    buildingInfo[2*EncodeUnit("Zerg Spawning Pool") + 1] = 2
    buildingInfo[2*EncodeUnit("Zerg Ultralisk Cavern") + 0] = 3
    buildingInfo[2*EncodeUnit("Zerg Ultralisk Cavern") + 1] = 2
    # 2x2
    buildingInfo[2*EncodeUnit('Terran Comsat Station') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Comsat Station') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Nuclear Silo') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Nuclear Silo') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Control Tower') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Control Tower') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Covert Ops') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Covert Ops') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Physics Lab') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Physics Lab') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Machine Shop') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Machine Shop') + 1] = 2
    buildingInfo[2*EncodeUnit('Terran Missile Turret') + 0] = 2
    buildingInfo[2*EncodeUnit('Terran Missile Turret') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Pylon') + 0] = 2
    buildingInfo[2*EncodeUnit('Protoss Pylon') + 1] = 2
    buildingInfo[2*EncodeUnit('Protoss Photon Cannon') + 0] = 2
    buildingInfo[2*EncodeUnit('Protoss Photon Cannon') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Creep Colony') + 0] = 2
    buildingInfo[2*EncodeUnit('Zerg Creep Colony') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Greater Spire') + 0] = 2
    buildingInfo[2*EncodeUnit('Zerg Greater Spire') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Spire') + 0] = 2
    buildingInfo[2*EncodeUnit('Zerg Spire') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Spore Colony') + 0] = 2
    buildingInfo[2*EncodeUnit('Zerg Spore Colony') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Sunken Colony') + 0] = 2
    buildingInfo[2*EncodeUnit('Zerg Sunken Colony') + 1] = 2
    buildingInfo[2*EncodeUnit('Zerg Nydus Canal') + 0] = 2
    buildingInfo[2*EncodeUnit('Zerg Nydus Canal') + 1] = 2
@EUDFunc
def GetBuildSizeX(unitType):
    EUDReturn(buildingInfo[2*unitType + 0])
@EUDFunc
def GetBuildSizeY(unitType):
    EUDReturn(buildingInfo[2*unitType + 1])