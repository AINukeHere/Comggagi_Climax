# stat_txt.tbl entry 1514: Expansion Protoss Campaign Insane<0>
PSUx(1514, 101, aiscript):
	debug(startmsg, eudddddddddddddddddddddddddddddddddddddddd)
		--startmsg--
	start_campaign()
	wait(1)

	start_town()
	defaultbuild_off()
	default_min(5)
	capt_expand()
	wait(1)
	help_iftrouble()

	#Unit		Number	Supply
	#probe		30	30
	#dark templar 	10	20
	#dragoon		40	80
	#high templar		15	30
	#archon		10	40
	#dark archon		5	20
	#reaver		5	20
	#shuttle		5	10
	#observer		5	5
	#scout		5	15
	#corsair		10	20
	#carrier		15	90
	#arbiter		5	20


	#define_max(30, Protoss Probe)
	define_max(50, Protoss Zealot)
	define_max(50, Protoss Dragoon)
	define_max(15, Protoss High Templar)
	define_max(5, Protoss Archon)
	define_max(10, Protoss Dark Templar)
	define_max(5, Protoss Dark Archon)
	define_max(5, Protoss Observer)
	define_max(10, Protoss Reaver)
	define_max(5, Protoss Shuttle)
	define_max(5, Protoss Scout)
	define_max(15, Protoss Corsair)
	define_max(15, Protoss Carrier)
	define_max(10, Protoss Arbiter)

	player_need(1, Protoss Nexus)
	player_need(10, Protoss Probe)
	player_need(19, Protoss Stargate)
	player_need(30, Protoss Gateway)
	player_need(3, Protoss Forge)
	player_need(2, Protoss Cybernetics Core)
	player_need(12, Protoss Robotics Facility)
	player_need(1, Protoss Citadel of Adun)
	player_need(3, Protoss Robotics Support Bay)
	player_need(2, Protoss Observatory)
	player_need(3, Protoss Fleet Beacon)
	player_need(3, Protoss Templar Archives)
	player_need(3, Protoss Arbiter Tribunal)
	

	#do_morph
	multirun(Gateway)
	multirun(Robotics)
	multirun(Stargate)
	multirun(Arbiter)
	
	
	
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

	wait(1440)
	train(20, Protoss Zealot)
	attack_add(20, Protoss Zealot)
	attack_prepare()
	wait(300)
	attack_do()
	attack_clear()
	expand(1, _expand)

	attack_add(20, Protoss Zealot)
	attack_add(10, Protoss Dragoon)
	attack_prepare()
	wait(300)
	attack_do()
	attack_clear()
	expand(2, _expand)

	train(8, Protoss Carrier)
	train(6, Protoss Corsair)
	train(3, Protoss Arbiter)
	attack_add(8, Protoss Carrier)
	attack_add(6, Protoss Corsair)
	attack_add(3, Protoss Arbiter)
	attack_prepare()
	wait(500)
	attack_do()
	attack_clear()
	create_unit(Terran Marine,200,200)
	goto(StartExpand)
	#stop()


		--Gateway--
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(15, Protoss High Templar)
	wait(1)
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(40, Protoss Zealot)
	wait(1)
	do_morph(15, Protoss High Templar)
	wait(1)
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(15, Protoss High Templar)
	wait(1)
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(40, Protoss Zealot)
	wait(1)
	do_morph(15, Protoss High Templar)
	wait(1)
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(15, Protoss High Templar)
	wait(1)
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(40, Protoss Zealot)
	wait(1)
	do_morph(15, Protoss High Templar)
	wait(1)
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(15, Protoss High Templar)
	wait(1)
	do_morph(40, Protoss Dragoon)
	wait(1)
	do_morph(10, Protoss Dark Templar)
	wait(180)

	do_morph(10, Protoss Archon)
	wait(1)
	do_morph(10, Protoss Archon)
	wait(1)

	do_morph(5, Protoss Dark Archon)
	wait(480)
	goto(Gateway)

		--Robotics--
	do_morph(5, Protoss Reaver)
	wait(1)
	do_morph(5, Protoss Shuttle)
	wait(1)
	do_morph(5, Protoss Observer)
	wait(252)
	goto(Robotics)

		--Stargate--
	do_morph(15, Protoss Carrier)
	wait(1)
	do_morph(15, Protoss Carrier)
	wait(1)
	do_morph(5, Protoss Scout)
	wait(1)
	do_morph(10, Protoss Corsair)
	wait(1)
	do_morph(10, Protoss Corsair)
	wait(100)
	goto(Stargate)

		--Arbiter--
	do_morph(20, Protoss Arbiter)
	wait(1)
	goto(Arbiter)

		--ForgeUpgrade--
	wait_build(3, Protoss Forge)
	wait(200)
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
	wait_build(2, Protoss Cybernetics Core)
	upgrade(1, Singularity Charge, 30)
	wait(2520)
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
	wait_build(1, Protoss Citadel of Adun)
	wait(200)
	upgrade(1, Leg Enhancements, 30)
	stop()

		--TemplarUpgrade--
	wait_build(3, Protoss Templar Archives)
	wait(200)
	tech(Psionic Storm, 30)		
	tech(Mind Control, 30)
	wait(3000)
	upgrade(1, Khaydarin Amulet, 30)
	upgrade(1, Argus Talisman, 30)
	tech(Hallucination, 30)
	stop()

		--SurpportUpgrade--
	wait_build(3, Protoss Robotics Support Bay)
	upgrade(1, Scarab Damage, 30)
	upgrade(1, Reaver Capacity, 30)
	upgrade(1, Gravitic Drive, 30)
	stop()

		--FleetUpgrade--
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
	wait_build(2, Protoss Arbiter Tribunal)
	wait(200)
	tech(Stasis Field, 30)
	tech(Recall, 30)
	upgrade(1, Khaydarin Core, 30)
	stop()

		--ObserverUpgrade--
	wait_build(2, Protoss Observatory)
	wait(200)
	upgrade(1, Gravitic Boosters, 30)
	upgrade(1, Sensor Array, 30)
	stop()





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




		--StartExpand--
	expand(99,_expand)
	wait(7000)
	goto(StartExpand)

		--_expand--
	start_town()
	creep(0)
	build(1, Protoss Nexus, 80)
	build(1, Protoss Pylon, 80)
	wait_build(1, Protoss Pylon)
	build(1, Protoss Gateway, 80)
	wait_build(1, Protoss Gateway)
	build(2, Protoss Pylon, 80)
	wait_build(2, Protoss Pylon)
	build(2, Protoss Gateway, 80)
	wait_build(2, Protoss Gateway)
	build(3, Protoss Pylon, 80)
	wait_build(3, Protoss Pylon)
	build(3, Protoss Gateway, 80)
	wait_build(3, Protoss Gateway)
	build(4, Protoss Pylon, 80)
	wait_build(4, Protoss Pylon)
	build(1, Protoss Photon Cannon, 80)
	wait_build(1, Protoss Photon Cannon)
	build(2, Protoss Photon Cannon, 80)
	wait_build(2, Protoss Photon Cannon)
	build(3, Protoss Photon Cannon, 80)
	wait_build(3, Protoss Photon Cannon)
	build(1, Protoss Robotics Facility, 80)
	wait_build(1, Protoss Robotics Facility)
	build(1, Protoss Stargate, 80)
	wait_build(1, Protoss Stargate)
	build(5, Protoss Pylon, 80)
	wait_build(5, Protoss Pylon)
	build(4, Protoss Gateway, 80)
	wait_build(4,Protoss Gateway)
	build(2, Protoss Stargate, 80)
	wait_build(2, Protoss Stargate)
	build(5, Protoss Gateway, 80)
	wait_build(5,Protoss Gateway)
	build(3, Protoss Stargate, 80)
	wait_build(3, Protoss Stargate)
	stop()