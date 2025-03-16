execute as @a at @s positioned ~ ~ ~ run say Hi
execute as @e[type=player] at @s positioned ~ ~ ~ run say All players: @e[type=player]
execute as @p[scores={foo=1}] at @s positioned 1 2 3 run say Fooooooooo
execute as @e[name="Some name",scores={someScore=1,"other Score"=3}] at @s positioned ~-1 ~.2 ~-.3 run say Weird numbers
