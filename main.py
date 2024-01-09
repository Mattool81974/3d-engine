import game
import physic as ps
import scene as sc

jeu = game.Game()

# Configure some thing into the game
base_struct = jeu.get_base_struct()
#base_struct.face_order["cube"] = [0, 1, 3, 4, 2, 5] # Don't touch this
jeu.load_advanced_struct()
jeu.load_elements()

# Load maps part
jeu.assign_map_part("1", "textures/concrete_wall")
jeu.assign_map_part("2", "textures/concrete_pillar")

# Load scene
scene = jeu.new_scene("level0", "maps/level0.wad")

# Load objects
player = scene.new_object("player", position = (0, 4, 0), graphic = False, physic = True, static = False, type = "player")
sol = scene.new_object("sol", scene, position = (12, 0, 12), scale = (27, 1, 27), texture_path = "textures/yellow_tile", type = "cube")
mur1 = scene.new_object("mur1", position = (25, 3, 12), rotation = (0, 0, 0), scale = (1, 5, 27), texture_path = "textures/cobble", type = "cube")
mur2 = scene.new_object("mur2", position = (12, 3, 25), rotation = (0, 0, 0), scale = (25, 5, 1), texture_path = "textures/cobble", type = "cube")
mur3 = scene.new_object("mur3", position = (-1, 3, 12), rotation = (0, 0, 0), scale = (1, 5, 27), texture_path = "textures/cobble", type = "cube")
mur4 = scene.new_object("mur4", position = (12, 3, -1), rotation = (0, 0, 0), scale = (25, 5, 1), texture_path = "textures/cobble", type = "cube")

# Run game
jeu.set_current_scene("level0")
jeu.run()