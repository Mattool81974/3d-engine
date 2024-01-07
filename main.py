import game
import scene as sc

jeu = game.Game()

# Load maps part
jeu.assign_map_part("1", "textures/concrete_wall")
jeu.assign_map_part("2", "textures/concrete_pillar")

# Load scene
scene = jeu.new_scene("level0", "maps/level0.wad")
scene.set_scale((1, 1, 1))
jeu.set_current_scene("level0")

# Load objects
sol = scene.new_object("sol", "cube", position = (12, 0, 12), scale = (27, 1, 27), texture_path = "textures/yellow_tile")
mur1 = scene.new_object("mur1", "cube", position = (25, 3, 12), rotation = (0, 0, 0), scale = (1, 5, 27), texture_path = "textures/cobble")
mur2 = scene.new_object("mur2", "cube", position = (12, 3, 25), rotation = (0, 0, 0), scale = (25, 5, 1), texture_path = "textures/cobble")
mur3 = scene.new_object("mur3", "cube", position = (-1, 3, 12), rotation = (0, 0, 0), scale = (1, 5, 27), texture_path = "textures/cobble")
mur4 = scene.new_object("mur4", "cube", position = (12, 3, -1), rotation = (0, 0, 0), scale = (25, 5, 1), texture_path = "textures/cobble")

jeu.run()