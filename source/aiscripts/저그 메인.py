# stat_txt.tbl entry 1344: Zerg Expansion Custom Level<0>
ZMCx(1344, 101, aiscript):
	multirun(SendMessage)
	debug(Z_Load,EUD AI was successfully loaded.          )
		--Z_Load--
	start_campaign()
	wait(1)

	start_town()
	defaultbuild_off()
	farms_timing()
	default_min(0)
	wait(1)

	help_iftrouble()

	define_max(20, Zerg Queen)
	#Upgrades
	multirun(GroundUpgrades)
	multirun(AirUpgrades)
	multirun(SpawningUpgrades)
	multirun(DenUpgrades)
	multirun(OverlordUpgrades)
	multirun(DefilerUpgrades)
	multirun(UltraUpgrades)
	multirun(QueenUprades)


	#Defense
	multirun(Defense)

	build(1, Zerg Hatchery, 150)
	build(10, Zerg Drone,80)
	build(1, Zerg Spawning Pool, 80)
	build(1, Zerg Hydralisk Den, 80)

	wait_build(1, Zerg Spawning Pool)
	build(1, Zerg Lair, 80)
	build(1, Zerg Queen's Nest, 80)
	build(1, Zerg Spire, 80)

	wait_build(1, Zerg Queen's Nest)
	build(1, Zerg Hive, 80)
	build(1, Zerg Ultralisk Cavern, 80)
	build(1, Zerg Defiler Mound, 80)
	build(1, Zerg Greater Spire, 80)

	build(30, Zerg Hatchery,80)
	build(30, Zerg Lair,80)
	build(30, Zerg Hive,80)
	player_need(30, Zerg Overlord)
	player_need(2, Zerg Spawning Pool)
	player_need(3, Zerg Hydralisk Den)
	player_need(2, Zerg Spire)
	player_need(1, Zerg Greater Spire)
	player_need(2, Zerg Ultralisk Cavern)
	player_need(2, Zerg Queen's Nest)
	player_need(3, Zerg Defiler Mound)

	#zerg_ready
	multirun(zerg_ready)

	allies_watch(4, FirstExpand)
	multirun(TrainLoop_Zergling)
	wait(1)
	wait(240)
	multirun(TrainLoop_Mutalisk)
	wait(1)
	multirun(TrainLoop_Hydralisk)
	wait(1000)
	create_unit(Protoss Observer,3600,3900)
	wait(500)
	wait(1)

	# train(12, Zerg Ultralisk) # 48
	# train(20, Zerg Hydralisk) # 20
	# train(50, Zerg Mutalisk) # 100
	#multirun(TrainLoop_Zergling)
	#wait(7)
	#multirun(TrainLoop_Hydralisk)
	#wait(96)
	#multirun(TrainLoop_Ultralisk)
	#wait(600)
	#create_unit(Protoss Observer,3600,3900)
	# train(60, Zerg Zergling)
	# multirun(TrainLoop_Mutalisk)

	wait(300)
	# create_unit(Protoss Observer,3600,3900)
	wait(500)

	wait(1200)
	train(50, Zerg Mutalisk)
	attack_add(50, Zerg Mutalisk)
	attack_prepare()
	multirun(TrainLoop_Mutalisk)
	wait(300)
	create_unit(Protoss Observer,3600,3900)
	attack_do()
	attack_clear()

	train(30, Zerg Mutalisk)
	train(20, Zerg Guardian)
	train(20, Zerg Devourer)
	attack_add(20, Zerg Guardian)
	attack_add(20, Zerg Devourer)
	attack_prepare()
	allies_watch(5, FirstExpand)
	multirun(BaseTrain1)
	multirun(BaseTrain2)
	multirun(BaseTrain3)
	multirun(BaseTrain4)
	multirun(BaseTrain5)
	multirun(BaseTrain6)
	wait(300)
	attack_do()
	attack_clear()


	wait(4320)
	wait(6000)
	multirun(ExpandLoop)
	stop()
	#####################################################


		--zerg_ready--
	if_owned(Protoss Zealot,zerg_start)
	wait(1)
	goto(zerg_ready)

		--zerg_start--
	random_jump(85, GDS)
	debug(DEBUG_01, Ultra Mutal Zergling Devourer)
		--DEBUG_01--
	do_morph(10, Zerg Defiler)
	wait(1)
	do_morph(10, Zerg Defiler)
	wait(1)
	do_morph(10, Zerg Defiler)
	wait(1)
	do_morph(10, Zerg Defiler)
	wait(1)
	do_morph(10, Zerg Defiler)
	wait(1)
	multirun(TrainLoop_Ultralisk)
	wait(1)
	multirun(TrainLoop_Mutalisk)
	wait(1)
	multirun(TrainLoop_Zergling)
	wait(1)
	multirun(TrainLoop_Devourer)
	wait(240)
	multirun(TrainLoop_Hydralisk)
	wait(904)
	create_unit(Protoss Observer,3600,3900)
		--Cannot--
	create_unit(16,200,200) # Sarah Kerrigan (Ghost)
	if_owned(16, Can) # Sarah Kerrigan (Ghost)
	wait(1)
	goto(Cannot)
		--Can--
	wait(1000)
	goto(zerg_start)


		--GDS--
	debug(DEBUG_02, Guardian Devourer Scourge)
		--DEBUG_02--
	multirun(TrainLoop_Mutalisk)
	wait(1)
	multirun(TrainLoop_Guardian)
	wait(1)
	multirun(TrainLoop_Devourer)
	wait(1)
	multirun(TrainLoop_Scourge)
	wait(624)
	create_unit(Protoss Observer,3600,3900)
		--Cannot2--
	create_unit(80,200,200) # Mojo (Scout)
	if_owned(80, Can2) # Mojo (Scout)
	wait(1)
	goto(Cannot2)
		--Can2--
	wait(1000)
	goto(zerg_start)
	#####################################################






	#####################################################
		--TrainLoop_Ultralisk--
	do_morph(100, Zerg Ultralisk)	#wait_force(100, Zerg Ultralisk)
	wait(5)
	if_owned(Protoss Observer,TrainStop)
	goto(TrainLoop_Ultralisk)

		--TrainLoop_Zergling--
	do_morph(100, Zerg Zergling)	#wait_force(100, Zerg Zergling)
	wait(5)
	if_owned(Protoss Observer,TrainStop)
	goto(TrainLoop_Zergling)

		--TrainLoop_Mutalisk--
	do_morph(100, Zerg Mutalisk)	#wait_force(100, Zerg Mutalisk)
	wait(5)
	if_owned(Protoss Observer,TrainStop)
	goto(TrainLoop_Mutalisk)

		--TrainLoop_Guardian--
	do_morph(100,Zerg Guardian)	#wait_force(100, Zerg Guardian)
	wait(5)
	if_owned(Protoss Observer,TrainStop)
	goto(TrainLoop_Guardian)

		--TrainLoop_Devourer--
	do_morph(100,Zerg Devourer)	#wait_force(100, Zerg Devourer)
	wait(5)
	if_owned(Protoss Observer, TrainStop)
	goto(TrainLoop_Devourer)

		--TrainLoop_Scourge--
	do_morph(100,Zerg Scourge)	#wait_force(100, Zerg Scourge)
	wait(5)
	if_owned(Protoss Observer, TrainStop)
	goto(TrainLoop_Scourge)

		--TrainLoop_Hydralisk--
	do_morph(100,Zerg Hydralisk)	#wait_force(100, Zerg Hydralisk)
	wait(5)
	if_owned(Protoss Observer, TrainStop)
	goto(TrainLoop_Hydralisk)


		--TrainStop--
	stop()
	#####################################################


		--BaseTrain1--
	train(10, Zerg Ultralisk)
	wait(1)
	goto(BaseTrain1)
		--BaseTrain2--
	#train(10, Zerg Hydralisk)
	wait(1)
	goto(BaseTrain2)
		--BaseTrain3--
	train(10, Zerg Mutalisk)
	wait(1)
	goto(BaseTrain3)
		--BaseTrain4--
	train(10, Zerg Defiler)
	wait(1)
	goto(BaseTrain4)
		--BaseTrain5--
	train(10, Zerg Devourer)
	wait(1)
	goto(BaseTrain5)
		--BaseTrain6--
	train(10, Zerg Guardian)
	wait(1)
	goto(BaseTrain6)







	#####################################################
		--GroundUpgrades--
	wait_build(3, Zerg Evolution Chamber)
	wait(1)
	upgrade(1, Zerg Melee Attacks, 30)
	upgrade(1, Zerg Missile Attacks, 30)	
	upgrade(1, Zerg Carapace, 30)
	wait(4000)
	upgrade(2, Zerg Melee Attacks, 30)
	upgrade(2, Zerg Missile Attacks, 30)
	upgrade(2, Zerg Carapace, 30)
	wait(4500)
	upgrade(3, Zerg Melee Attacks, 30)
	upgrade(3, Zerg Missile Attacks, 30)
	upgrade(3, Zerg Carapace, 30)
	stop()

		--AirUpgrades--
	wait_build(2, Zerg Spire)
	wait(1)
	upgrade(1, Zerg Flyer Attacks, 30)
	upgrade(1, Zerg Flyer Carapace, 30)
	wait(4000)
	upgrade(2, Zerg Flyer Attacks, 30)
	upgrade(2, Zerg Flyer Carapace, 30)
	wait(4500)
	upgrade(3, Zerg Flyer Attacks, 30)
	upgrade(3, Zerg Flyer Carapace, 30)
	stop()

		--SpawningUpgrades--
	wait_build(2, Zerg Spawning Pool)
	wait(1)
	upgrade(1, Metabolic Boost, 30)
	wait(2000)
	upgrade(1, Adrenal Glands, 30)
	stop()
	

		--DenUpgrades--
	wait_build(3, Zerg Hydralisk Den)
	wait(1)
	upgrade(1, Grooved Spines, 30)
	upgrade(1, Muscular Augments, 30)
	tech(Lurker Aspect, 30)
	stop()

	
		--OverlordUpgrades--
	wait_build(4, Zerg Lair)
	wait(1)
	tech(Burrowing, 30)
	upgrade(1, Pneumatized Carapace, 30)
	upgrade(1, Ventral Sacs, 30)
	upgrade(1, Antennae, 30)
	stop()
	
	
		--DefilerUpgrades--
	wait_build(3, Zerg Defiler Mound)
	wait(1)
	tech(Plague, 30)
	tech(Consume, 30)
	upgrade(1, Metasynaptic Node, 30)
	stop()


		--UltraUpgrades--
	wait_build(2, Zerg Ultralisk Cavern)
	wait(1)
	upgrade(1, Chitinous Plating, 30)
	upgrade(1, Anabolic Synthesis, 30)
	stop()


		--QueenUprades--
	wait_build(2, Zerg Queen's Nest)
	wait(1)
	tech(Spawn Broodling, 30)
	upgrade(1, Gamete Meiosis, 30)
	stop()

	#####################################################














		
	####################################################


		--ExpandLoop--
	expand(99,NormalExpand)
	wait(4320)
	goto(ExpandLoop)

	# 바로 플토앞마당
		--FirstExpand--
	start_town()
	get_oldpeons(9)
	build(1, Zerg Hatchery, 80)
	wait_build(1, Zerg Hatchery)
	build(5, Zerg Drone, 80)
	build(1, Zerg Spawning Pool, 80)
	build(1, Zerg Hydralisk Den, 80)
	build(2, Zerg Spire, 80)
	build(1, Zerg Queen's Nest, 80)
	build(1, Zerg Ultralisk Cavern, 80)
	build(1, Zerg Defiler Mound, 80)
	build(1, Zerg Greater Spire, 80)
	wait(240)
	build(2 ,Zerg Hatchery, 80)
	wait_buildstart(2, Zerg Hatchery)
	build(3 ,Zerg Hatchery, 80)
	wait_buildstart(3, Zerg Hatchery)
	build(4 ,Zerg Hatchery, 80)
	wait_buildstart(4, Zerg Hatchery)
	build(5 ,Zerg Hatchery, 80)
	wait_buildstart(5,Zerg Hatchery)
	build(6 ,Zerg Hatchery, 80)
	wait_buildstart(5,Zerg Hatchery)
	build(7 ,Zerg Hatchery, 80)
	wait_buildstart(5,Zerg Hatchery)
	build(8 ,Zerg Hatchery, 80)
	wait_buildstart(5,Zerg Hatchery)
	build(9 ,Zerg Hatchery, 80)
	wait_buildstart(5,Zerg Hatchery)
	build(10 ,Zerg Hatchery, 80)
	wait_build(10, Zerg Hatchery)
	place_guard(Zerg Defiler, 1)

	build(10, Zerg Lair, 80)
	wait_build(10, Zerg Lair)
	build(10, Zerg Hive, 80)
	stop()



		--NormalExpand--
	start_town()
	get_oldpeons(10)
	build(1, Zerg Hatchery, 80)
	wait_buildstart(1, Zerg Hatchery)
	build(3, Zerg Drone,80)	
	build(2, Zerg Hatchery, 80)
	wait_buildstart(2, Zerg Hatchery)
	build(3, Zerg Hatchery, 80)
	wait_buildstart(3, Zerg Hatchery)
	build(4, Zerg Hatchery, 80)
	wait_buildstart(4, Zerg Hatchery)
	build(5, Zerg Hatchery, 80)
	wait_buildstart(5, Zerg Hatchery)
	build(6, Zerg Hatchery, 80)
	wait_buildstart(6, Zerg Hatchery)
	build(7, Zerg Hatchery, 80)
	wait_buildstart(7, Zerg Hatchery)
	build(8, Zerg Hatchery, 80)
	wait_buildstart(8, Zerg Hatchery)
	build(9, Zerg Hatchery, 80)
	wait_buildstart(9, Zerg Hatchery)
	build(10, Zerg Hatchery, 80)
	wait_buildstart(10, Zerg Hatchery)
	place_guard(Zerg Defiler, 1)
	wait_build(1, Zerg Hatchery)
	player_need(2, Zerg Spawning Pool)
	player_need(2, Zerg Hydralisk Den)
	wait_build(10, Zerg Hatchery)
	build(10, Zerg Lair, 80)
	wait_build(10, Zerg Lair)
	player_need(2, Zerg Spire)
	player_need(2, Zerg Queen's Nest)
	build(10, Zerg Hive, 80)
	player_need(2, Zerg Ultralisk Cavern)
	player_need(2, Zerg Defiler Mound)
	player_need(2, Zerg Greater Spire)
	stop()
	###########################################




	###########################################
		--Defense--
	wait(2000)
	#defensebuild_gg(1, Zerg Zergling)
	#defensebuild_gg(1, Zerg Hydralisk)
	#defensebuild_gg(1, Zerg Ultralisk)
	#defensebuild_ag(1, Zerg Hydralisk)
	#defensebuild_aa(1, Zerg Mutalisk)
	#defensebuild_ga(1, Zerg Mutalisk)
	#defensebuild_ga(1, Zerg Guardian)
	#defensebuild_aa(1, Zerg Devourer)
	#defensebuild_aa(1, Zerg Scourge)
	defenseuse_gg(1, Zerg Zergling)
	defenseuse_gg(1, Zerg Ultralisk)
	defenseuse_ag(1, Zerg Hydralisk)
	defenseuse_aa(1, Zerg Mutalisk)
	defenseuse_ga(1, Zerg Mutalisk)
	defenseuse_ga(1, Zerg Guardian)
	defenseuse_aa(1, Zerg Devourer)
	defenseuse_aa(1, Zerg Scourge)
	stop()
	###########################################










		--SendMessage--
	wait(1)
	if_owned(0,hi1) # Terran Marine
	if_owned(1,hi2) # Terran Ghost
	if_owned(2,hi3) # Terran Vulture
	if_owned(3,hi4) # Terran Goliath

	goto(SendMessage)

		--hi1--
	debug(hi1_end, ㅎㅇ)
		--hi1_end--
	create_unit(20, 3673,3770) # Jim Raynor(Marine)
	goto(SendMessage)

		--hi2--
	debug(hi2_end, ㅈㅈ)
		--hi2_end--
	create_unit(20, 3673,3770) # Jim Raynor(Marine)
	goto(SendMessage)

		--hi3--
	debug(hi3_end, HAVE FUN!)
		--hi3_end--
	create_unit(20, 3673,3770) # Jim Raynor(Marine)
	goto(SendMessage)

		--hi4--
	random_jump(96,hi4continue)
	goto(hi3)
		--hi4continue--
	debug(hi4continue2, ㅋㅋㅋ)
		--hi4continue2--
	wait(36)
	debug(hi4_end, 또 죽으려고 들어왔군)
		--hi4_end--
	create_unit(20, 3673,3770) # Jim Raynor(Marine)
	goto(SendMessage)