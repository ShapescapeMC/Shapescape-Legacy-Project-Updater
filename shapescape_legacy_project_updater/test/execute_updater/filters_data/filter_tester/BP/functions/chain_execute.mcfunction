# Basic
execute as @a at @s positioned ~ ~ ~ run execute as @a at @s positioned ~ ~ ~ run say Hi
execute as @e[type=player] at @s positioned ~ ~ ~ run execute as @e[type=player] at @s positioned ~ ~ ~ run say All players: @e[type=player]
execute as @p[scores={foo=1}] at @s positioned 1 2 3 run execute as @p[scores={foo=1}] at @s positioned 1 2 3 run say Fooooooooo
execute as @e[name="Some name",scores={someScore=1,"other Score"=3}] at @s positioned ~-1 ~.2 ~-.3 run execute as @e[name="Some name",scores={someScore=1,"other Score"=3}] at @s positioned ~-1 ~.2 ~-.3 run say Weird numbers

# Execute detect
execute as @a at @s positioned ~ ~ ~ if block 1 2 3 minecraft:stone  run execute as @a at @s positioned ~ ~ ~ if block 1 2 3 minecraft:stone  run say Hi
execute as @e[type=player] at @s positioned ~ ~ ~ if block 1 ~ 3 minecraft:stone  run execute as @e[type=player] at @s positioned ~ ~ ~ if block 1 ~ 3 minecraft:stone  run say All players: @e[type=player]
execute as @p[scores={foo=1}] at @s positioned 1 2 3 if block 1 ~~-0.3 minecraft:stone  run execute as @p[scores={foo=1}] at @s positioned 1 2 3 if block 1 ~~-0.3 minecraft:stone  run say Fooooooooo
execute as @e[name="Some name",scores={someScore=1,"other Score"=3}] at @s positioned ~-1 ~.2 ~-.3 if block ~~~ stone  run execute as @e[name="Some name",scores={someScore=1,"other Score"=3}] at @s positioned ~-1 ~.2 ~-.3 if block ~~~ stone  run say Weird numbers
