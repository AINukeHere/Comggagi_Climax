# stat_txt.tbl entry 1507: Expansion Protoss Campaign Difficult<0>
PHIx(1507, 101, aiscript):
	start_campaign()
	wait(1)

	start_areatown()
	defaultbuild_off()
	default_min(0)
	wait(1)
	build(1, Protoss Nexus, 80)
    #Terran쪽
	multirun(FactoryTrainLoopReady)
	multirun(CommandCenterFinishReady)
	#multirun(MachineShopUpgradeReady)

    debug(loop, inLoop)
        --loop--
    wait(500)
    goto(loop)

		--CommandCenterFinishReady--
	if_owned(78, CommandCenterFinish) # Fenix (Dragoon)
	wait(1)
	goto(CommandCenterFinishReady)
		--CommandCenterFinish--
	create_unit(75,307,3300) # Zeratul
	debug(DEBUG_LOG_01, Zeratul Created adsdf)
		--DEBUG_LOG_01--
	#stop()
	#wait(900)
		--buildLoop--
	do_morph(5, Terran SCV)
	wait(1)
	#debug(buildLoop, goto build Loop)
	goto(buildLoop)


		--FactoryTrainLoopReady--
	if_owned(88, FactoryTrainLoopStart) # Artanis
	wait(1)
	goto(FactoryTrainLoopReady)
		--FactoryTrainLoopStart--
	create_unit(79,307,3300) # Tassadar (Templar)
	#build(5, Terran Factory, 80)
	build(5, Terran Machine Shop, 80)
	#player_need(5, Terran Machine Shop)
	debug(FactoryTrainLoop, Tassadar Created asdf)
		--FactoryTrainLoop--
	#do_morph(20, Terran Siege Tank<0>Tank Mode)
	wait(12)
	goto(FactoryTrainLoop)
	


		--MachineShopUpgrade--
	tech(Tank Siege Mode, 30)
	tech(Spider Mines, 30)
	upgrade(1, Ion Thrusters, 30)
	stop()

	# defensebuild_gg(1, Terran Siege Tank)
	# defenseuse_gg(1, Terran Siege Tank)
	# defensebuild_gg(1, Terran Goliath)
	# defenseuse_gg(1, Terran Goliath)

	# build(1, Terran Armory, 80)
	# build(1, Terran Starport, 80)
	# wait_build(1, Terran Starport)
	# build(2, Terran Armory, 80)
	# build(1, Terran Science Facility, 80)
	# wait_build(1, Terran Science Facility)
	# upgrade(1, Terran Vehicle Plating, 30)
	# upgrade(1, Terran Vehicle Weapons, 30)
	# wait(4000)
	# upgrade(2, Terran Vehicle Plating, 30)
	# upgrade(2, Terran Vehicle Weapons, 30)
	# wait(4500)
	# upgrade(3, Terran Vehicle Plating, 30)
	# upgrade(3, Terran Vehicle Weapons, 30)