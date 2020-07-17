# Simple Minecraft Server Manager
# By Doomlad
# 07/17/2020

import yaml
from modules.replace_keys import replace_key

prefix = "[SMCSM] » "


def server_opt():
    try:
        bukkit_yml = "Bukkit.yml        | "
        spigot_yml = "Spigot.yml        | "
        paper_yml = "Paper.yml         | "
        server_properties_prefix = "server.properties | "
        print(prefix + "Server Optimization will be applied to Bukkit.yml, Spigot.yml, Paper.yml and "
                       "Server.properties\n")

        # [ Bukkit.yml ] #
        with open("bukkit.yml", 'r') as bukkit:
            try:
                bukkit_list = yaml.safe_load(bukkit)
            except yaml.YAMLError:
                print(prefix + "Error: Could not read bukkit.yml")

        # spawn-limits
        # Performance Impact: Medium
        # ➫ While there is more to this than "mobs per player" (explained in PDF),
        # lower values mean less mobs. Avoid going too low or the mob shortages will be noticeable.
        # Subsequent values in the guide will make the reduction less noticeable.
        print(prefix + bukkit_yml + "spawn-limits (m:70, a:10, w-a:15, am:15) -> (m:50, a:8, w-a:3, am:1)           ",
              end="")
        bukkit_list['spawn-limits']['monsters'] = 50
        bukkit_list['spawn-limits']['animals'] = 8
        bukkit_list['spawn-limits']['water-animals'] = 3
        bukkit_list['spawn-limits']['ambient'] = 1
        print('[OK]')

        # chunk-gc.period-in-ticks
        # Performance Impact: Medium
        # ➫ This unloads vacant chunks faster. Ticking fewer chunks means less TPS consumption.
        print(prefix + bukkit_yml + "chunk-gc.period-in-ticks (600) -> (400)                                        ",
              end="")
        bukkit_list['chunk-gc']['period-in-ticks'] = 400
        print('[OK]')

        # ticks-per.monster-spawns
        # Performance Impact: Medium
        # ➫ This sets how often (in ticks) the server attempts to spawn a monster.
        # Slightly increasing the time between spawns should not impact spawn rates.
        print(prefix + bukkit_yml + "ticks-per.monster-spawns (1) -> (4)                                            ",
              end="")
        bukkit_list['ticks-per']['monster-spawns'] = 4
        print('[OK]')

        print()

        # Write configuration in memory to file
        with open("bukkit.yml", 'w') as bukkit:
            try:
                yaml.dump(bukkit_list, bukkit, default_flow_style=False)
            except yaml.YAMLError:
                print(prefix + "Error: Could not write bukkit.yml")

    except FileNotFoundError:
        print(prefix + "Error: Could not find bukkit.yml")

    try:
        # [ Spigot.yml ] #
        with open("spigot.yml", 'r') as spigot:
            try:
                spigot_list = yaml.safe_load(spigot)
            except yaml.YAMLError:
                print(prefix + "Error: Could not read spigot.yml")

        # save-user-cache-on-stop-only
        # Performance Impact: Medium
        # ➫ Should the server constantly save user data (false) or delay that task until a
        # stop/restart (true)? This is nice TPS savings on Spigot (less on Paper since it's more efficient).
        print(prefix + spigot_yml + "save-user-cache-on-stop-only (false) -> (true)                                 ",
              end="")
        spigot_list['settings']['save-user-cache-on-stop-only'] = True
        print('[OK]')

        # max-tick-time
        # Performance Impact: N/A
        # ➫ The optimized value disables this feature.
        # The small TPS savings is not worth the potential damage.
        print(prefix + spigot_yml + "max-tick-time (tile:50, entity:50) -> (tile:1000, entity:1000)                 ",
              end="")
        spigot_list['world-settings']['default']['max-tick-time']['tile'] = 1000
        spigot_list['world-settings']['default']['max-tick-time']['entity'] = 1000
        print('[OK]')

        # mob-spawn-range
        # Performance Impact: N/A
        # ➫ This sets the max mob spawn distance (in chunks) from players.
        # After limiting spawns in Bukkit, this will condense mobs to mimic the appearance of normal rates.
        print(prefix + spigot_yml + "mob-spawn-range (8) -> (6)                                                     ",
              end="")
        spigot_list['world-settings']['default']['mob-spawn-range'] = 6
        print('[OK]')

        # entity-activation-range
        # Performance Impact: Medium
        # ➫ Entities past this range will be ticked less often.
        # Avoid setting this too low or you might break mob behavior (mob aggro, raids, etc).
        print(prefix + spigot_yml + "entity-activation-range (a:32, m:32, r:48, m:16) -> (a:16, m:24, r:48, m:8)    ",
              end="")
        spigot_list['world-settings']['default']['entity-activation-range']['animals'] = 16
        spigot_list['world-settings']['default']['entity-activation-range']['monsters'] = 24
        spigot_list['world-settings']['default']['entity-activation-range']['raiders'] = 48
        spigot_list['world-settings']['default']['entity-activation-range']['misc'] = 8
        print('[OK]')

        # entity-activation-range
        # Performance Impact: Medium
        # ➫ Enabling this prevents the server from ticking villagers outside the activation range.
        # Villager tasks in 1.14+ are very heavy.
        print(prefix + spigot_yml + "tick-inactive-villagers (true) -> (false)                                      ",
              end="")
        spigot_list['world-settings']['default']['entity-activation-range']['tick-inactive-villagers'] = False
        print('[OK]')

        # merge-radius
        # Performance Impact: Medium
        # ➫ Merging items means less ground item ticking.
        # Higher values allow more items to be swept into piles.
        print(prefix + spigot_yml + "merge-radius (item:2.5, exp:3.0) -> (item:4.0, exp:6.0)                        ",
              end="")
        spigot_list['world-settings']['default']['merge-radius']['item'] = 4.0
        spigot_list['world-settings']['default']['merge-radius']['exp'] = 6.0
        print('[OK]')

        # nerf-spawner-mobs
        # Performance Impact: Medium
        # ➫ When enabled, mobs from spawners will not have AI (will not swim/attack/move).
        # This is big TPS savings on servers with mob farms, but also messes with their behavior.
        # A farm limiter plugin might be a better solution.
        print(prefix + spigot_yml + "nerf-spawner-mobs (false) -> (true)                                            ",
              end="")
        spigot_list['world-settings']['default']['nerf-spawner-mobs'] = True
        print('[OK]')

        # arrow-despawn-rate
        # Performance Impact: Minor
        # ➫ Similar to item-despawn-rate, but for fired arrows. Some servers may want to keep arrows on
        # the ground longer, but most will have no complaints from faster removal.
        print(prefix + spigot_yml + "arrow-despawn-rate (1200) -> (300)                                             ",
              end="")
        spigot_list['world-settings']['default']['arrow-despawn-rate'] = 300
        print('[OK]')

        print()

        # Write configuration in memory to file
        with open("spigot.yml", 'w') as spigot:
            try:
                yaml.dump(spigot_list, spigot, default_flow_style=False)
            except yaml.YAMLError:
                print(prefix + "Error: Could not write spigot.yml")

    except FileNotFoundError:
        print(prefix + "Error: Could not find spigot.yml")

    try:
        # [ Paper.yml ] #
        with open("paper.yml", 'r') as paper:
            try:
                paper_list = yaml.safe_load(paper)
            except yaml.YAMLError:
                print(prefix + "Error: Could not read paper.yml")

        # max-auto-save-chunks-per-tick
        # Performance Impact: Heavy
        # ➫ This slows incremental chunk saving during the world save task.
        # This is incredibly important for 1.13+ servers with how inefficient chunk saving is.
        print(prefix + paper_yml + "max-auto-save-chunks-per-tick (24) -> (6)                                      ",
              end="")
        paper_list['world-settings']['default']['max-auto-save-chunks-per-tick'] = 6
        print('[OK]')

        # optimize-explosions
        # Performance Impact: Minor
        # ➫ Paper has a very efficient algorithm for explosions with no impact to game-play.
        print(prefix + paper_yml + "optimize-explosions (false) -> (true)                                          ",
              end="")
        paper_list['world-settings']['default']['optimize-explosions'] = True
        print('[OK]')

        # mob-spawner-tick-rate
        # Performance Impact: Minor
        # ➫ This is the delay (in ticks) before an active spawner attempts spawns.
        # Doubling the delay will not impact spawn rates. Only go higher if you have significant tick
        # loss from ticking spawners.
        print(prefix + paper_yml + "mob-spawner-tick-rate (1) -> (2)                                               ",
              end="")
        paper_list['world-settings']['default']['mob-spawner-tick-rate'] = 2
        print('[OK]')

        # disable-chest-cat-detection
        # Performance Impact: Minor
        # ➫ Chests scan for a cat on top of it when opened by a player.
        # While enabling this eliminates vanilla behavior (cats block chests), do you really need
        # this mechanic?
        print(prefix + paper_yml + "disable-chest-cat-detection (false) -> (true)                                  ",
              end="")
        paper_list['world-settings']['default']['game-mechanics']['disable-chest-cat-detection'] = True
        print('[OK]')

        # container-update-tick-rate
        # Performance Impact: Minor
        # ➫ This changes how often (in ticks) inventories are refreshed while open.
        # Do not exceed 4 to avoid visual issues.
        print(prefix + paper_yml + "container-update-tick-rate (1) -> (3)                                          ",
              end="")
        paper_list['world-settings']['default']['container-update-tick-rate'] = 3
        print('[OK]')

        # max-entity-collisions
        # Performance Impact: Medium
        # ➫ Crammed entities (grinders, farms, etc.) will collide less and consume less TPS in the process.
        print(prefix + paper_yml + "max-entity-collisions (8) -> (2)                                               ",
              end="")
        paper_list['world-settings']['default']['max-entity-collisions'] = 2
        print('[OK]')

        # grass-spread-tick-rate
        # Performance Impact: Medium
        # ➫ The time (in ticks) before the server tries to spread grass in chunks.
        # This will have no game-play impact on most game types.
        print(prefix + paper_yml + "grass-spread-tick-rate (1) -> (4)                                              ",
              end="")
        paper_list['world-settings']['default']['grass-spread-tick-rate'] = 4
        print('[OK]')

        # despawn-ranges
        # Performance Impact: Minor
        # Soft = The distance (in blocks) from a player where mobs will be periodically removed.
        # Hard = Distance where mobs are removed instantly.
        # ➫ Lower ranges clear background mobs and allow more to be spawned in areas with player traffic.
        # This further reduces the game-play impact of reduced spawning (bukkit.yml).
        print(prefix + paper_yml + "despawn-ranges (soft:32, hard:128) -> (soft:28, hard:96)                       ",
              end="")
        paper_list['world-settings']['default']['despawn-ranges']['soft'] = 28
        paper_list['world-settings']['default']['despawn-ranges']['hard'] = 96
        print('[OK]')

        # non-player-arrow-despawn-rate
        # Performance Impact: Heavy
        # ➫ This will significantly reduce hopper lag by preventing InventoryMoveItemEvent
        # being called for EVERY slot in a container.
        print(prefix + paper_yml + "non-player-arrow-despawn-rate (-1) -> (60)                                     ",
              end="")
        paper_list['world-settings']['default']['non-player-arrow-despawn-rate'] = 60
        print('[OK]')

        # creative-arrow-despawn-rate
        # Performance Impact: Minor
        # ➫ Similar to Spigot's arrow-despawn-rate, but targets skeleton-fired arrows.
        # Since players cannot retrieve mob arrows, this is only a cosmetic change.
        print(prefix + paper_yml + "creative-arrow-despawn-rate (-1) -> (60)                                       ",
              end="")
        paper_list['world-settings']['default']['creative-arrow-despawn-rate'] = 60
        print('[OK]')

        # prevent-moving-into-unloaded-chunks
        # Performance Impact: Medium
        # ➫ Prevents players from entering an unloaded chunk (due to lag), which causes more lag.
        # The true setting will set them back to a safe location instead.
        print(prefix + paper_yml + "prevent-moving-into-unloaded-chunks (false) -> (true)                          ",
              end="")
        paper_list['world-settings']['default']['prevent-moving-into-unloaded-chunks'] = True
        print('[OK]')

        # use-faster-eigencraft-redstone
        # Performance Impact: Heavy
        # ➫ This setting reduces redundant redstone updates by as much as 95% without breaking
        # vanilla devices. Empirical testing shows a speedup by as much as 10x!
        print(prefix + paper_yml + "use-faster-eigencraft-redstone (false) -> (true)                               ",
              end="")
        paper_list['world-settings']['default']['use-faster-eigencraft-redstone'] = True
        print('[OK]')

        # armor-stands-tick
        # Performance Impact: Minor
        # ➫ Some items are viewed as entities (require ticking) since they interact with the world.
        # Unticked armor stands will not get pushed by water (do you care?)
        print(prefix + paper_yml + "armor-stands-tick (true) -> (false)                                            ",
              end="")
        paper_list['world-settings']['default']['armor-stands-tick'] = False
        print('[OK]')

        # per-player-mob-spawns
        # Performance Impact: Minor
        # ➫ This implements singleplayer spawning behavior instead of Bukkit's random algorithms.
        # This prevents the actions of others (i.e. Massive farms) from impacting the server's spawn rates.
        print(prefix + paper_yml + "per-player-mob-spawns (false) -> (true)                                        ",
              end="")
        paper_list['world-settings']['default']['per-player-mob-spawns'] = True
        print('[OK]')

        print()

        # Write configuration in memory to file
        with open("paper.yml", 'w') as paper:
            try:
                yaml.dump(paper_list, paper, default_flow_style=False)
            except yaml.YAMLError:
                print(prefix + "Error: Could not write paper.yml")

    except FileNotFoundError:
        print(prefix + "Error: Could not find paper.yml\n")

    try:
        # view-distance
        # Performance Impact: heavy
        # ➫ This is a big performance setting as it forcibly reduces the max render distance for players.
        # Open world servers (like Survival) should strive to use 6+, but others on shared hosts, low specs,
        # or huge player counts might consider 4-5 if chunk gen causes lag.
        server_properties = 'server.properties'
        replace_key(server_properties, 'view-distance', 8)
        print(prefix + server_properties_prefix + "view-distance (10) -> (8)                                                      ",
            end="")
        print('[OK]')

    except FileNotFoundError:
        print(prefix + "Error: Could not find server.properties file!\n")

