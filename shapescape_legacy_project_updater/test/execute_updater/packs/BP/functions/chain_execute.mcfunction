# Basic
execute @a ~ ~ ~ execute @a ~ ~ ~ say Hi
execute @e[type=player] ~ ~ ~ execute @e[type=player] ~ ~ ~ say All players: @e[type=player]
execute @p[scores={foo=1}] 1 2 3 execute @p[scores={foo=1}] 1 2 3 say Fooooooooo
execute @e[name="Some name",scores={someScore=1,"other Score"=3}] ~-1 ~.2 ~-.3 execute @e[name="Some name",scores={someScore=1,"other Score"=3}] ~-1 ~.2 ~-.3 say Weird numbers

# Execute detect
execute @a ~ ~ ~ detect 1 2 3 minecraft:stone 1 execute @a ~ ~ ~ detect 1 2 3 minecraft:stone 1 say Hi
execute @e[type=player] ~ ~ ~ detect 1 ~ 3 minecraft:stone 1 execute @e[type=player] ~ ~ ~ detect 1 ~ 3 minecraft:stone 1 say All players: @e[type=player]
execute @p[scores={foo=1}] 1 2 3 detect 1 ~~-0.3 minecraft:stone 1 execute @p[scores={foo=1}] 1 2 3 detect 1 ~~-0.3 minecraft:stone 1 say Fooooooooo
execute @e[name="Some name",scores={someScore=1,"other Score"=3}] ~-1 ~.2 ~-.3 detect ~~~ stone -1 execute @e[name="Some name",scores={someScore=1,"other Score"=3}] ~-1 ~.2 ~-.3 detect ~~~ stone -1 say Weird numbers
