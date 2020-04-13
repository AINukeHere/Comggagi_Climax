# stat_txt.tbl entry 1514: Expansion Protoss Campaign Insane<0>
PSUx(1514, 101, aiscript):
	debug(startmsg, ㅎㅇ)
		--startmsg--
	start_campaign()
	wait(1)

	start_town()
	defaultbuild_off()
	default_min(5)
	farms_timing()
	capt_expand()
	wait(1)
	help_iftrouble()

	define_max(30, Protoss Probe)
	define_max(20, Protoss Zealot)
	define_max(40, Protoss Dragoon)
	define_max(20, Protoss High Templar)
	define_max(255, Protoss Archon)
	define_max(20, Protoss Dark Templar)
	define_max(10, Protoss Dark Archon)
	define_max(8, Protoss Observer)
	define_max(20, Protoss Reaver)
	define_max(10, Protoss Shuttle)
	define_max(255, Protoss Scout)
	define_max(15, Protoss Corsair)
	define_max(6, Protoss Carrier)
	define_max(15, Protoss Arbiter)

	player_need(1, Protoss Nexus)
	player_need(10, Protoss Probe)
	player_need(11, Protoss Stargate)
	player_need(30, Protoss Gateway)
	player_need(3, Protoss Forge)
	player_need(3, Protoss Cybernetics Core)
	player_need(17, Protoss Robotics Facility)
	player_need(1, Protoss Citadel of Adun)
	player_need(3, Protoss Robotics Support Bay)
	player_need(2, Protoss Observatory)
	player_need(3, Protoss Fleet Beacon)
	player_need(3, Protoss Templar Archives)
	player_need(3, Protoss Arbiter Tribunal)

	#Morph
	multirun(Morph_Gateway)
	multirun(Morph_Robotics)
	multirun(Morph_Stargate)

	#Upgrades
	multirun(ForgeUpgrade)
	multirun(CoreUpgrade)
	multirun(AdunUpgrade)
	multirun(TemplarUpgrade)
	multirun(SurpportUpgrade)
	multirun(FleetUpgrade)
	multirun(ArbiterUpgrade)
	multirun(ObserverUpgrade)
	
	#Defense
	multirun(Defense)

	# 테란기지
	allies_watch(5, tryFirstTerranBase)

	
	train(12, Protoss Zealot)
	attack_add(12, Protoss Zealot)
	attack_prepare()
	wait(300)
	attack_do()
	attack_clear()
	#expand(1, _expand)

	train(12, Protoss Dark Templar)
	train(12, Protoss Dragoon)
	attack_add(12, Protoss Dark Templar)
	attack_add(12, Protoss Dragoon)
	attack_prepare()
	wait(300)
	attack_do()
	attack_clear()
	#expand(2, _expand)

	train(6, Protoss Carrier)
	train(8, Protoss Corsair)
	train(5, Protoss Arbiter)
	attack_add(6, Protoss Carrier)
	attack_add(8, Protoss Corsair)
	attack_add(5, Protoss Arbiter)
	attack_prepare()
	wait(300)
	attack_do()
	attack_clear()
	create_unit(77,307,3300) # Fenix (Zealot)
	# 저그쪽 기지
	allies_watch(6, _expand)

		--expandLoop--
	wait(4500)
	expand(99, _expand)
	goto(expandLoop)

		--_expand--
	debug(_expandDebug,expand)
		--_expandDebug--
	start_town()
	creep(0)
	# if_owned(Terran SCV, firstTerranBaseStart)
	# goto(protossMulti)
	# 	--firstTerranBaseStart--
	# multirun(firstTerranBaseStart)
	# 	--protossMulti--
	build(1, Protoss Nexus, 80)
	get_oldpeons(2)
	build(1, Protoss Pylon, 80)
	wait_build(1, Protoss Pylon)
	build(1, Protoss Gateway, 80)
	build(1, Protoss Robotics Facility, 80)
	build(2, Protoss Pylon, 80)
	wait_build(2, Protoss Pylon)
	build(2, Protoss Gateway, 80)
	build(2, Protoss Robotics Facility, 80)
	build(3, Protoss Pylon, 80)
	wait_build(3, Protoss Pylon)
	build(3, Protoss Gateway, 80)
	build(3, Protoss Robotics Facility, 80)
	build(4, Protoss Pylon, 80)
	wait_build(4, Protoss Pylon)
	build(1, Protoss Photon Cannon, 80)
	wait_buildstart(1, Protoss Photon Cannon)
	build(2, Protoss Photon Cannon, 80)
	wait_buildstart(2, Protoss Photon Cannon)
	build(3, Protoss Photon Cannon, 80)
	wait_buildstart(3, Protoss Photon Cannon)
	build(4, Protoss Photon Cannon, 80)
	wait_buildstart(4, Protoss Photon Cannon)
	build(5, Protoss Photon Cannon, 80)
	wait_buildstart(5, Protoss Photon Cannon)
	build(6, Protoss Photon Cannon, 80)
	wait_buildstart(6, Protoss Photon Cannon)
	stop()
	
		--Morph_Gateway--
	do_morph(30, Protoss Dark Templar)
	do_morph(6, Protoss Dark Archon)
	wait(24)
	goto(Morph_Gateway)

		--Morph_Robotics--
	do_morph(30, Protoss Reaver)
	do_morph(10, Protoss Shuttle)
	wait(24)
	goto(Morph_Robotics)

		--Morph_Stargate--
	do_morph(12, Protoss Corsair)
	do_morph(12, Protoss Arbiter)
	wait(24)
	goto(Morph_Stargate)

		--Defense--
	wait(2000)
	#defensebuild_gg(1, Protoss Dark Templar)
	#defensebuild_gg(1, Protoss Dragoon)
	#defensebuild_ag(1, Protoss Dragoon)
	#defensebuild_gg(1, Protoss Archon)
	#defensebuild_ag(1, Protoss Archon)
	#defensebuild_gg(1, Protoss Reaver)
	#defensebuild_ga(1, Protoss Scout)
	#defensebuild_aa(1, Protoss Scout)
	#defensebuild_aa(1, Protoss Corsair)
	#defensebuild_ga(1, Protoss Carrier)
	#defensebuild_aa(1, Protoss Carrier)
	defenseuse_gg(1, Protoss Zealot)
	defenseuse_gg(1, Protoss Dark Templar)
	defenseuse_gg(1, Protoss Dragoon)
	defenseuse_ag(1, Protoss Dragoon)
	defenseuse_gg(1, Protoss Archon)
	defenseuse_ag(1, Protoss Archon)
	defenseuse_gg(1, Protoss Reaver)
	defenseuse_ga(1, Protoss Scout)
	defenseuse_aa(1, Protoss Scout)
	defenseuse_aa(1, Protoss Corsair)
	defenseuse_ga(1, Protoss Carrier)
	defenseuse_aa(1, Protoss Carrier)
	stop()
	

	#테란 기지
		--tryFirstTerranBase--
	debug(t02,t02)
		--t02--

		--checkBringSCV--
	if_owned(75, firstTerranBaseStart) # Zeratul
	wait(1)
	#debug(a31, 79)
	goto(checkBringSCV)

		--firstTerranBaseStart--
	debug(abcde, CreateUnit CreateUnit CreateUnit CreateUnit CreateUnit CreateUnit)
		--abcde--
	start_town()
	create_unit(79, 307,3300) # Tassadar


	creep(0)
	build(1, Terran Command Center, 80)
	wait_build(1, Terran Command Center)
	player_need(5, Terran SCV)
	build(1, Terran Barracks, 80)
	wait_build(1, Terran Barracks)


	build(1, Terran Factory, 80)
	wait_buildstart(1, Terran Factory)
	build(2, Terran Factory, 80)
	wait_buildstart(2, Terran Factory)
	build(3, Terran Factory, 80)
	wait_buildstart(3, Terran Factory)
	build(4, Terran Factory, 80)
	wait_buildstart(4, Terran Factory)
	build(5, Terran Factory, 80)
	wait_buildstart(5, Terran Factory)
	build(5, Terran Machine Shop, 80)
	wait_build(3, Terran Machine Shop)

	multirun(FactoryTrainLoop)
	multirun(MachineShopUpgrade)

	defensebuild_gg(1, Terran Siege Tank)
	defenseuse_gg(1, Terran Siege Tank)
	defensebuild_gg(1, Terran Goliath)
	defenseuse_gg(1, Terran Goliath)

	build(1, Terran Armory, 80)
	build(1, Terran Starport, 80)
	wait_build(1, Terran Starport)
	build(2, Terran Armory, 80)
	build(1, Terran Science Facility, 80)
	wait_build(1, Terran Science Facility)
	upgrade(1, Terran Vehicle Plating, 30)
	upgrade(1, Terran Vehicle Weapons, 30)
	wait(4000)
	upgrade(2, Terran Vehicle Plating, 30)
	upgrade(2, Terran Vehicle Weapons, 30)
	wait(4500)
	upgrade(3, Terran Vehicle Plating, 30)
	upgrade(3, Terran Vehicle Weapons, 30)

	
		

		--FactoryTrainLoop--
	do_morph(20, Terran Siege Tank<0>Tank Mode)
	do_morph(20, Terran Vulture)
	wait(12)
	goto(FactoryTrainLoop)
	
		--ForgeUpgrade--
	build(3, Protoss Forge, 80)
	wait_build(3, Protoss Forge)
	upgrade(1, Protoss Ground Weapons, 30)
	upgrade(1, Protoss Armor, 30)		
	upgrade(1, Protoss Plasma Shields, 30)
	wait(4000)
	upgrade(2, Protoss Ground Weapons, 30)	
	upgrade(2, Protoss Armor, 30)		
	upgrade(2, Protoss Plasma Shields, 30)
	wait(4500)
	upgrade(3, Protoss Ground Weapons, 30)	
	upgrade(3, Protoss Armor, 30)		
	upgrade(3, Protoss Plasma Shields, 30)	
	stop()

		--CoreUpgrade--
	build(3, Protoss Cybernetics Core, 80)
	wait_build(3, Protoss Cybernetics Core)
	upgrade(1, Singularity Charge, 30)
	upgrade(1, Protoss Air Weapons, 30)
	upgrade(1, Protoss Plating, 30)
	wait(4000)
	upgrade(2, Protoss Air Weapons, 30)
	upgrade(2, Protoss Plating, 30)	
	wait(4500)
	upgrade(3, Protoss Air Weapons, 30)	
	upgrade(3, Protoss Plating, 30)		
	stop()

		--AdunUpgrade--
	build(1, Protoss Citadel of Adun, 80)
	wait_build(1, Protoss Citadel of Adun)
	wait(200)
	upgrade(1, Leg Enhancements, 30)
	stop()

		--TemplarUpgrade--
	build(3, Protoss Templar Archives, 80)
	wait_build(3, Protoss Templar Archives)
	wait(200)
	tech(Psionic Storm, 30)
	tech(Mind Control, 30)
	upgrade(1, Argus Talisman, 30)
	wait(3000)
	upgrade(1, Khaydarin Amulet, 30)
	tech(Hallucination, 30)
	stop()

		--SurpportUpgrade--
	build(3, Protoss Robotics Support Bay, 80)
	wait_build(3, Protoss Robotics Support Bay)
	upgrade(1, Scarab Damage, 30)
	upgrade(1, Reaver Capacity, 30)
	upgrade(1, Gravitic Drive, 30)
	stop()

		--FleetUpgrade--
	build(3, Protoss Fleet Beacon, 80)
	wait_build(3, Protoss Fleet Beacon)
	wait(200)
	upgrade(1, Gravitic Thrusters, 30)
	upgrade(1, Carrier Capacity, 30)
	tech(Disruption Web, 30)
	wait(2500)
	upgrade(1, Argus Jewel, 30)
	upgrade(1, Apial Sensors, 30)
	stop()

		--ArbiterUpgrade--
	build(3, Protoss Arbiter Tribunal, 80)
	wait_build(3, Protoss Arbiter Tribunal)
	tech(Stasis Field, 30)
	tech(Recall, 30)
	upgrade(1, Khaydarin Core, 30)
	stop()

		--ObserverUpgrade--
	build(2, Protoss Observatory, 80)
	wait_build(2, Protoss Observatory)
	upgrade(1, Gravitic Boosters, 30)
	upgrade(1, Sensor Array, 30)
	stop()

		--MachineShopUpgrade--
	tech(Tank Siege Mode, 30)
	tech(Spider Mines, 30)
	upgrade(1, Ion Thrusters, 30)
	stop()
