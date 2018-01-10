"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""

import hlt
import logging

game = hlt.Game("NeverDieBot")
logging.info("Bot Started!")

def largest(planets): # Find largest planets

    curpl = [] # Set Vars
    maxr = 0

    for planet in planets: # Create array of largest planets
        if(planet.radius >= maxr):
            maxr = planet.radius
            curpl.append(planet)

    logging.info("Largest planets: "+str(curpl)) # Log data
    return curpl # Return arrays of largest planets

i = 1

ships = []

while True: # Loops each turn

    game_map = game.update_map() # Get updated version of map
    command_queue = [] # Commands to execute this turn

    for ship in game_map.get_me().all_ships():
        planets = largest(game_map.all_planets())
        planet = planets[len(planets)-i]
        logging.info(len(planets))

        if(ship.docking_status != ship.docking_status.UNDOCKED):
            continue

        if(planet.owner == None or planet.owner == game_map.get_me()):
            if ship.can_dock(planet):
                ships.append(ship)
                command_queue.append(ship.dock(planet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
        else:
            i+=1
            continue

    game.send_command_queue(command_queue)
