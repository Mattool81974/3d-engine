# Import librairies
import advanced_struct as ad
import base_struct as bs
import glm
import math
import model
import moderngl as mgl
import numpy as np
import physic as ps
import player as pl
import pygame as pg
import sys

class Scene_2D:
    """Class representing a 2d scene
    """

    def __init__(self, scene_size: tuple) -> None:
        """Create a 2d scene
        """
        self.map_path = ""
        self.objects = {}
        self.pos = (0, 0)
        self.scene_size = scene_size

        self.fill(0)

    def fill(self, part: int) -> None:
        """Fill the map with a part

        Args:
            part (int): part to fill
        """
        self.map = []
        self.objects.clear()
        for _ in range(self.get_scene_size()[1]):
            line = []
            for __ in range(self.get_scene_size()[0]):
                line.append(part)
            self.map.append(line)

    def get_map_path(self) -> str:
        """Return the path of the map

        Returns:
            str: path of the map
        """
        return self.map_path
    
    def get_objects(self) -> dict:
        """Return a dict of every transform object created

        Returns:
            dict: every transform object created
        """
        return self.objects

    def get_part_at(self, x: int, y: int) -> int:
        """Return a part into the map

        Returns:
            int: part into the map
        """
        return self.map[x][y]
    
    def get_pos(self) -> tuple:
        """Return the pos of the first part of the map

        Returns:
            tuple: pos of the first part of the map
        """
        return self.pos

    def get_scene_size(self) -> tuple:
        """Return the size of the scene

        Returns:
            tuple: _size of the scene
        """
        return self.scene_size
    
    def load_map(self, path: str) -> None:
        """Load a map from a file

        Args:
            path (str): path through the map
        """
        lines = []
        with open(path) as file:
            lines = file.readlines()
        self.map_path = path
        pos_and_size = lines[0] # Load the first line (pos of the first part and size of the map)
        self.pos = (float(pos_and_size.split(" ")[0]), float(pos_and_size.split(" ")[1]))
        size = (int(pos_and_size.split(" ")[2]), int(pos_and_size.split(" ")[3]))
        if size == self.get_scene_size():
            for j in range(1, len(lines)):
                line = lines[j]
                if line != "\n" and line != "":
                    for i in range(len(line)):
                        if line[i] != "\n":
                            self.map[i][j - 1] = str(line[i])

class Physic_Scene:
    """Class representating a graphic scene (collection of physic object)
    """

    def __init__(self, advanced_struct: ad.Advanced_Struct, name: str, scene_size: tuple) -> None:
        """Create a physic scene

        Args:
            advanced_struct (ad.Advanced_Struct): advanced structure of the game
            name (str): name of the scene
        """
        self.advanced_struct = advanced_struct
        self.dynamic_objects = {}
        self.map = {0: []}
        self.name = name
        self.scene_size = scene_size
        self.static_objects = {}

        self.fill(0, 0)

    def add_dynamic_object(self, name: str, object: ps.Physic_Dynamic_Object) -> None:
        """Add a dynamic object to the scene

        Args:
            name (str): name of this object into the scene
            object (ps.Physic_Dynamic_Object): physic dynamic object to add to the scene
        """
        if list(self.get_dynamic_objects().keys()).count(name) <= 0:
            self.get_dynamic_objects()[name] = object
            return
        print("Matix physic scene : Warning !! The name \"" + name + "\" into the scene \"" + self.get_name() + "\" already exists.")

    def add_static_object(self, name: str, object: ps.Physic_Static_Object, level: int = 0) -> None:
        """Add a static object to the scene

        Args:
            name (str): name of this object into the scene
            object (ps.Physic_Static_Object): physic static object to add to the scene
        """
        if list(self.get_static_objects().keys()).count(name) <= 0:
            self.get_static_objects()[name] = object
            if round(object.get_transform().get_position()[0]) >= 0 and round(object.get_transform().get_position()[0]) < self.get_scene_size()[0]:
                if round(object.get_transform().get_position()[2]) >= 0 and round(object.get_transform().get_position()[2]) < self.get_scene_size()[1]:
                    self.map[level][round(object.get_transform().get_position()[0])][round(object.get_transform().get_position()[2])] = object
            return
        print("Matix physic scene : Warning !! The name \"" + name + "\" into the scene \"" + self.get_name() + "\" already exists.")

    def check_collision(self) -> None:
        """Check the collision for the dynamic objects to static object
        """
        for object in self.get_dynamic_objects().values():
            collision = object.get_collision()
            if collision != None:
                pos = object.get_transform().get_position()
                delta_time = self.get_base_struct().get_delta_time()
                movement = object.get_transform().get_movement()

                future_pos = (pos[0] + movement[0] * delta_time, pos[1] + movement[1] * delta_time, pos[2] + movement[2] * delta_time)
                if math.floor(future_pos[2] - collision.get_width()) == math.floor(future_pos[2] + collision.get_width()): # If the object will collide with 2 case on X axe
                    future_pos = (pos[0] + collision.get_width() + movement[0] * delta_time, pos[1] + collision.get_width() + movement[1] * delta_time, pos[2] + collision.get_width() + movement[2] * delta_time)
                    future = self.map[0][round(future_pos[0])][math.floor(pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[0]) > future_pos[0] and future_pos[0] < pos[0] + collision.get_width()):
                                object.get_transform().movement = (0, movement[1], movement[2])
                    movement = object.get_transform().get_movement()

                    future = self.map[0][round(future_pos[0])][math.ceil(pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[0]) > future_pos[0] and future_pos[0] < pos[0] + collision.get_width()):
                                object.get_transform().movement = (0, movement[1], movement[2])
                    movement = object.get_transform().get_movement()

                    future_pos = (pos[0] + movement[0] * delta_time - collision.get_width(), pos[1] + movement[1] * delta_time - collision.get_width(), pos[2] + movement[2] * delta_time - collision.get_width())
                    future = self.map[0][round(future_pos[0])][math.floor(pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[0]) < future_pos[0] and future_pos[0] > pos[0] - collision.get_width()):
                                object.get_transform().movement = (0, movement[1], movement[2])
                    movement = object.get_transform().get_movement()

                    future = self.map[0][round(future_pos[0])][math.ceil(pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[0]) > future_pos[0] and future_pos[0] < pos[0] - collision.get_width()):
                                object.get_transform().movement = (0, movement[1], movement[2])
                    movement = object.get_transform().get_movement()
                else: #If the object will collide with one case on X axe
                    future_pos = (pos[0] + collision.get_width() + movement[0] * delta_time, pos[1] + collision.get_width() + movement[1] * delta_time, pos[2] + collision.get_width() + movement[2] * delta_time)
                    future = self.map[0][round(future_pos[0])][round(pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[0]) > future_pos[0] and future_pos[0] < pos[0] + collision.get_width()):
                                object.get_transform().movement = (0, movement[1], movement[2])
                    movement = object.get_transform().get_movement()

                    future_pos = (pos[0] + movement[0] * delta_time - collision.get_width(), pos[1] + movement[1] * delta_time - collision.get_width(), pos[2] + movement[2] * delta_time - collision.get_width())
                    future = self.map[0][round(future_pos[0])][round(pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[0]) < future_pos[0] and future_pos[0] > pos[0] - collision.get_width()):
                                object.get_transform().movement = (0, movement[1], movement[2])
                    movement = object.get_transform().get_movement()

                future_pos = (pos[0] + movement[0] * delta_time, pos[1] + movement[1] * delta_time, pos[2] + movement[2] * delta_time)
                if math.floor(future_pos[0] - collision.get_width()) == math.floor(future_pos[0] + collision.get_width()): # If the object will collide with 2 case on Y axe
                    future_pos = (pos[0] + collision.get_width() + movement[0] * delta_time, pos[1] + collision.get_width() + movement[1] * delta_time, pos[2] + collision.get_width() + movement[2] * delta_time)
                    future = self.map[0][math.floor(pos[0])][round(future_pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[2]) > future_pos[2] and future_pos[2] < pos[2] + collision.get_width()):
                                object.get_transform().movement = (movement[0], movement[1], 0)
                    movement = object.get_transform().get_movement()

                    future = self.map[0][math.ceil(pos[0])][round(future_pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[2]) > future_pos[2] and future_pos[2] < pos[2] + collision.get_width()):
                                object.get_transform().movement = (movement[0], movement[1], 0)
                    movement = object.get_transform().get_movement()

                    future_pos = (pos[0] + movement[0] * delta_time - collision.get_width(), pos[1] + movement[1] * delta_time - collision.get_width(), pos[2] + movement[2] * delta_time - collision.get_width())
                    future = self.map[0][math.floor(pos[0])][round(future_pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[2]) < future_pos[2] and future_pos[2] > pos[2] - collision.get_width()):
                                object.get_transform().movement = (movement[0], movement[1], 0)
                    movement = object.get_transform().get_movement()

                    future = self.map[0][math.ceil(pos[0])][round(future_pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[2]) > future_pos[2] and future_pos[2] < pos[2] - collision.get_width()):
                                object.get_transform().movement = (movement[0], movement[1], 0)
                    movement = object.get_transform().get_movement()
                else: #If the object will collide with one case on Y axe
                    future_pos = (pos[0] + collision.get_width() + movement[0] * delta_time, pos[1] + collision.get_width() + movement[1] * delta_time, pos[2] + collision.get_width() + movement[2] * delta_time)
                    future = self.map[0][round(pos[0])][round(future_pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[2]) > future_pos[2] and future_pos[2] < pos[2] + collision.get_width()):
                                object.get_transform().movement = (movement[0], movement[1], 0)
                    movement = object.get_transform().get_movement()

                    future_pos = (pos[0] + movement[0] * delta_time - collision.get_width(), pos[1] + movement[1] * delta_time - collision.get_width(), pos[2] + movement[2] * delta_time - collision.get_width())
                    future = self.map[0][round(pos[0])][round(future_pos[2])]
                    if future != 0:
                        if future.get_collision() != None:
                            if not (round(future_pos[2]) < future_pos[2] and future_pos[2] > pos[2] - collision.get_width()):
                                object.get_transform().movement = (movement[0], movement[1], 0)
                    movement = object.get_transform().get_movement()

    def destroy(self) -> None:
        """Destroy the scene
        """
    
    def fill(self, static: int, map_level: int = 0) -> None:
        """Fill the maps with a static state

        Args:
            static (int): static state to fill the map
            map_level (int, optional): level of the map to fill. Defaults to 0.
        """
        self.map[map_level].clear()
        for _ in range(self.get_scene_size()[1]):
            map_line = []
            for __ in range(self.get_scene_size()[0]):
                map_line.append(static)
            self.map[map_level].append(map_line)

    def get_advanced_struct(self) -> ad.Advanced_Struct:
        """Return the advanced structure of the game

        Return:
            ad.Advanced_Struct: advanced structure of the game
        """
        return self.advanced_struct
    
    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base structure of the game

        Returns:
            bs.Base_Struct: base structure of the game
        """
        return self.get_advanced_struct().get_base_struct()
    
    def get_dynamic_objects(self) -> dict:
        """Return the dict of the dynamics object

        Returns:
            dict: dict of the dynamics object
        """
        return self.dynamic_objects
    
    def get_name(self) -> str:
        """Return the name of the scene

        Returns:
            str: name of the scene
        """
        return self.name

    def get_static_objects(self) -> dict:
        """Return a dict of static objects into the scene

        Returns:
            dict: dict of static objects into the scene
        """
        return self.static_objects
    
    def get_scene_size(self) -> tuple:
        """Return the size of the scene

        Returns:
            tuple: size of the scene
        """
        return self.scene_size

    def new_dynamic_object(self, name: str, object: bs.Transform_Object, weight: float = 1) -> ps.Physic_Dynamic_Object:
        """Create a new dynamic object into the scene

        Args:
            name (str): name of this object into the scene
            object (bs.Transform_Object): transform for the object
        """
        if list(self.get_dynamic_objects().keys()).count(name) <= 0:
            object = ps.Physic_Dynamic_Object(self.get_base_struct(), object, weight = weight)
            self.add_dynamic_object(name, object)
            return object
        print("Matix physic scene : Warning !! The name \"" + name + "\" you want to create into the physic scene \"" + self.get_name() + "\" already exists.")

    def new_static_object(self, name: str, object: bs.Transform_Object, resistance: float = -1) -> ps.Physic_Static_Object:
        """Create a new static object into the scene

        Args:
            name (str): name of this object into the scene
            object (bs.Transform_Object): transform for the object
        """
        if list(self.get_static_objects().keys()).count(name) <= 0:
            object = ps.Physic_Static_Object(self.get_base_struct(), object)
            self.add_static_object(name, object)
            return object
        print("Matix physic scene : Warning !! The name \"" + name + "\" you want to create into the scene \"" + self.get_name() + "\" already exists.")

    def set_scene_size(self, scene_size: tuple) -> None:
        """Change the size of the scene (reset the map)

        Args:
            scene_size (tuple): size of the scene
        """
        self.scene_size = scene_size
        self.fill(0)
    
    def update(self) -> None:
        """Update the physic scene
        """
        for object in list(self.get_static_objects().values()):
            object.update()
        for object in list(self.get_dynamic_objects().values()):
            object.update()
        self.check_collision()

class Graphic_Scene(bs.Transform_Object):
    """Class representing a graphic scene (collection of graphic object)
    """

    def __init__(self, advanced_struct: ad.Advanced_Struct, name: str) -> None:
        """Create a scene
        """
        super().__init__(advanced_struct.get_base_struct(), parent = None, position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1))
        self.advanced_struct = advanced_struct
        self.objects = {}
        self.name = name

    def add_object(self, name: str, object: bs.Transform_Object):
        """Add an object to the scene

        Args:
            name (str): name of the object
            object (Transform_Object): object to add to the scene
        """
        if list(self.objects.keys()).count(name) == 0 and list(self.objects.values()).count(object) == 0:
            self.objects[name] = object

    def destroy(self) -> None:
        """Destroy the scene
        """
        for object in self.objects.items():
            object[1].destroy()

    def get_advanced_struct(self) -> ad.Advanced_Struct:
        """Return the advanced struct of the game

        Returns:
            ad.Advanced_Struct: advanced struct of the game
        """
        return self.advanced_struct
    
    def get_name(self) -> str:
        """Return the name of the scene

        Returns:
            str: name of the scene
        """
        return self.name
      
    def new_object(self, name: str, transform: bs.Transform_Object, type: SyntaxError, texture_path: str = "") -> bs.Transform_Object:
        """Create a new object into the scene and return it

        Args:
            name (str): name of the object
            type (str): type of the object

        Return:
            bs.Transform_Object: object created
        """
        vbo = self.get_advanced_struct().get_all_vbos()[type]

        # If the texture is empty
        if texture_path == "":
            if type == "cube" or type == "test":
                texture_path = "textures/unknow"
            else:
                texture_path = "textures/unknow.png"

        # Get/load textures
        splitted = texture_path.split(".")
        texture = ""
        textures = self.get_advanced_struct().get_all_textures()
        if splitted[-1] == "png" or splitted[-1] == "jpg":
            if list(textures.keys()).count(texture_path) <= 0:
                texture = [model.Texture(self.get_advanced_struct().get_base_struct(), texture_path)]
                textures[texture_path] = texture[0]
            else:
                texture = textures[texture]
        else:
            all_files = bs.get_all_files(texture_path)
            texture = []
            for file in all_files:
                if list(textures.keys()).count(file) <= 0:
                    tex = model.Texture(self.get_advanced_struct().get_base_struct(), file[0])
                    texture.append(tex)
                    textures[file] = tex
                else:
                    texture.append(textures[file])

        # Add the object into the scene
        if type == "cube":
            object = model.Cube_Object(self.get_advanced_struct().get_base_struct(), texture = texture, transform = transform, vbo = vbo, type = type)
            self.add_object(name, object)
            return object
        elif type == "test":
            object = model.Cube_Object(self.get_advanced_struct().get_base_struct(), one_texture = True, texture = texture, transform = transform, vbo = vbo, type = type)
            self.add_object(name, object)
            return object
        else:
            object = model.Graphic_Object(self.get_advanced_struct().get_base_struct(), texture = texture, transform = transform, vbo = vbo, type = type)
            self.add_object(name, object)
            return object

    def render(self) -> None:
        """Render the scene
        """
        for object in self.objects.items():
            object[1].render()

    def update(self) -> None:
        """Update the scene
        """
        for object in self.objects.items():
            object[1].update()

class Scene(bs.Transform_Object):
    """Class representating a scene
    """

    def __init__(self, advanced_struct: ad.Advanced_Struct, name: str, graphic: bool = True, physic: bool = True, scene_size: tuple = (25, 25)) -> None:
        """Create a scene
        """
        self.advanced_struct = advanced_struct
        super().__init__(advanced_struct.get_base_struct(), None, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        self.player = None
        self.name = name
        self.objects = {}
        self.scene_size = scene_size

        # Create physic and graphic scene if necessary
        self.graphic = graphic
        self.physic = physic
        if self.use_graphic():
            self.graphic_scene = Graphic_Scene(advanced_struct, name)
        if self.use_physic():
            self.physic_scene = Physic_Scene(advanced_struct, name, self.get_scene_size())

    def add_object(self, name: str, object: bs.Transform_Object):
        """Add an object to the scene

        Args:
            name (str): name of the object
            object (Transform_Object): object to add to the scene
        """
        if list(self.objects.keys()).count(name) == 0 and list(self.objects.values()).count(object) == 0:
            self.objects[name] = object

    def destroy(self) -> None:
        """Destroy the scene
        """
        if self.use_graphic(): self.get_graphic_scene().destroy()
        if self.use_physic(): self.get_physic_scene().destroy()

    def get_advanced_struct(self) -> ad.Advanced_Struct:
        """Return the advanced struct of the game

        Returns:
            ad.Advanced_Struct: advanced struct of the game
        """
        return self.advanced_struct
    
    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.get_advanced_struct().get_base_struct()
    
    def get_graphic_scene(self) -> Graphic_Scene:
        """Return the graphic scene of this scene

        Returns:
            Graphic_Scene: graphic scene of this scene
        """
        return self.graphic_scene

    def get_name(self) -> str:
        """Return the name of the scene

        Returns:
            str: name of the scene
        """
        return self.name

    def get_objects(self) -> dict:
        """Return the dict of all the object in the scene

        Returns:
            dict: all the object in the scene
        """
        return self.objects
    
    def get_physic_scene(self) -> Physic_Scene:
        """Return the physic scene of this scene

        Returns:
            Physic_Scene: physic scene of this scene
        """
        return self.physic_scene
    
    def get_player(self) -> pl.Player:
        """Return the player into the scene, or None

        Returns:
            pl.Player: player into the scene, or None
        """
        return self.player
    
    def get_scene_size(self) -> tuple:
        """Return the size of the scene

        Returns:
            tuple: size of the scene
        """
        return self.scene_size
      
    def load_from_2d_scene(self, scene: Scene_2D, parts: dict) -> None:
        """Load the map from a 2d scene

        Args:
            scene (Scene_2D): 2d scene used to load the map
            parts (dict): parts used to make the scene
        """
        self.set_position((scene.get_pos()[0], 0, scene.get_pos()[1]))
        if self.use_physic(): self.get_physic_scene().set_scene_size(scene.get_scene_size())
        for j in range(scene.get_scene_size()[1]): # Load each part of the map
            for i in range(scene.get_scene_size()[0]):
                part = scene.get_part_at(i, j)
                if list(parts.keys()).count(part) > 0: # If the part exists
                    if parts[part] != "":
                        name = str(i) + ";" + str(j)
                        type = parts[part].get_type()
                        self.new_object(name, collision_type = "cube", parent = None, position = (1 * i, 3, 1 * j), scale = (1, 5, 1), texture_path = parts[part].get_texture_path(), type = type)
                else: # If the part does not exist
                    print("Matix scene : Warning !! The part \"" + part + "\" into the map \"" + scene.get_map_path() + " \" for loading into the scene \"" + self.get_name() + "\" does not exist.")
    
    def new_object(self, name: str, collision_type: str = "", collision_width: float = 0.3, graphic: bool = True, parent: bs.Transform_Object = None, physic: bool = True, position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1), static: bool = True, texture_path: str = "", type: str = "cube") -> bs.Transform_Object:
        """Create a new object into the scene and return it

        Args:
            name (str): name of the object
            type (str): type of the object

        Return:
            bs.Transform_Object: object created
        """
        if parent == None:
            parent = self
        
        # Create and add the object into the scene
        object = None
        if type == "player":
            object = pl.Player(self.get_advanced_struct(), self.get_advanced_struct().get_camera(), parent, position, rotation, scale)
            self.player = object
        else:
            object = bs.Transform_Object(self.get_base_struct(), parent, position, rotation, scale)
            self.add_object(name, object)

        # Add the object into the graphic and physic scene
        if self.use_graphic() and graphic:
            if texture_path == "":
                if type == "cube": texture_path = "textures/unknow"
                else: texture_path = "textures/unknow.png"

            self.get_graphic_scene().new_object(name, object, type, texture_path)
        if self.use_physic() and physic:
            physic_object = None
            if static:
                physic_object = self.get_physic_scene().new_static_object(name, object)
            else:
                physic_object = self.get_physic_scene().new_dynamic_object(name, object)

            if collision_type == "cube":
                physic_object.collision = ps.Square_Collision(collision_width)
        return object
    
    def update(self) -> None:
        """Update the scene
        """
        self.get_player().handle_player_move()
        self.get_player().handle_player_rotation()
        for object in self.get_objects().values():
            object.update()
        if self.use_physic():
            self.get_physic_scene().update()
        if self.use_graphic():
            self.get_graphic_scene().update()
            self.get_graphic_scene().render()
        for object in self.get_objects().values():
            object.soft_reset()
        self.get_player().update()
        self.get_player().soft_reset()
        
    def use_graphic(self) -> bool:
        """Return if the scene use graphic or not

        Returns:
            bool: if the scene use graphic or not
        """
        return self.graphic
    
    def use_physic(self) -> bool:
        """Return if the scene use physic or not

        Returns:
            bool: if the scene use physic or not
        """
        return self.physic