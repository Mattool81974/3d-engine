# Import librairies
import advanced_struct as ad
import base_struct as bs
import glm
import model
import moderngl as mgl
import numpy as np
import physic as ps
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
        self.map = {0: []}
        self.name = name
        self.objects = {}
        self.scene_size = scene_size

        self.fill(0, 0)

    def add_object(self, name: str, object: ps.Physic_Object) -> None:
        """Add an object to the scene

        Args:
            name (str): name of this object into the scene
            object (ps.Physic_Object): physic object to add to the scene
        """
        if list(self.get_objects().keys()).count(name) <= 0:
            self.get_objects()[name] = object
            return
        print("Matix physic scene : Warning !! The name \"" + name + "\" into the scene \"" + self.get_name() + "\" already exists.")

    def fill(self, static: int, map_level: int = 0) -> None:
        """Fill the maps with a static state

        Args:
            static (int): static state to fill the map
            map_level (int, optional): level of the map to fill. Defaults to 0.
        """
        self.map[map_level].clear()
        for j in range(self.get_scene_size()[1]):
            map_line = []
            for i in range(self.get_scene_size()[0]):
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
    
    def get_name(self) -> str:
        """Return the name of the scene

        Returns:
            str: name of the scene
        """
        return self.name

    def get_objects(self) -> dict:
        """Return a dict of objects into the scene

        Returns:
            dict: dict of objects into the scene
        """
        return self.objects
    
    def get_scene_size(self) -> tuple:
        """Return the size of the scene

        Returns:
            tuple: size of the scene
        """
        return self.scene_size

    def load_from_2d_scene(self, scene: Scene_2D, parts: dict, map_level: int = 0) -> None:
        """Load the physic map from a 2d scene

        Args:
            scene (Scene_2D): 2d scene used to laod the map
            parts (dict): dict of usefull parts
            map_level (int): map level to load
        """
        for j in range(scene.get_scene_size()[1]): # Load each part of the map
            for i in range(scene.get_scene_size()[0]):
                part = scene.get_part_at(i, j)
                if list(parts.keys()).count(part) > 0: # If the part exists
                    if parts[part] != "":
                        static = parts[part].get_is_a_physic_static_object()
                        if static:
                            self.map[map_level][i][j] = ps.Physic_Static_Object(scene.get_objects()[i][j])
                else: # If the part does not exist
                    print("Matix scene : Warning !! The part \"" + part + "\" into the map \"" + scene.get_map_path() + " \" for loading into the scene \"" + self.get_name() + "\" does not exist.")
    
    def new_object(self, name: str, object: bs.Transform_Object, weight: float = 1) -> ps.Physic_Object:
        """Create a new object into the scene

        Args:
            name (str): name of this object into the scene
            object (bs.Transform_Object): transform for the object
        """
        if list(self.get_objects().keys()).count(name) <= 0:
            object = ps.Physic_Dynamic_Object(self.get_base_struct(), object, weight = weight)
            self.add_object(name, object)
            return object
        print("Matix physic scene : Warning !! The name \"" + name + "\" you want to create into the scene \"" + self.get_name() + "\" already exists.")

    def update(self) -> None:
        """Update the physic scene
        """
        for object in list(self.get_objects().values()):
            object.update()

class Scene(bs.Transform_Object):
    """Class representing a scene (collection of object)
    """

    def __init__(self, advanced_struct: ad.Advanced_Struct, name: str) -> None:
        """Create a scene
        """
        super().__init__(parent = None, position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1))
        self.advanced_struct = advanced_struct
        self.objects = {}
        self.name = name
        self.textures = {}
        self.transform_multiplier = 2

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
    
    def get_transform_multiplier(self) -> float:
        """Return the multiplier for transforming

        Returns:
            float: multiplier for transforming
        """
        return self.transform_multiplier
    
    def load_from_2d_scene(self, scene: Scene_2D, parts: dict) -> None:
        """Load the map from a 2d scene

        Args:
            scene (Scene_2D): 2d scene used to laod the map
        """
        self.set_position((scene.get_pos()[0] * self.get_transform_multiplier(), 0, scene.get_pos()[1] * self.get_transform_multiplier()))
        for j in range(scene.get_scene_size()[1]): # Load each part of the map
            for i in range(scene.get_scene_size()[0]):
                part = scene.get_part_at(i, j)
                if list(parts.keys()).count(part) > 0: # If the part exists
                    if parts[part] != "":
                        texture_path = parts[part].get_texture_path()
                        object = self.new_object(str(i) + ";" + str(j), "cube", position = (1 * i, 3, 1 * j), scale = (1, 5, 1), texture_path = texture_path)
                        if list(scene.get_objects().keys()).count(i) <= 0: scene.get_objects()[i] = {}
                        scene.get_objects()[i][j] = object
                else: # If the part does not exist
                    print("Matix scene : Warning !! The part \"" + part + "\" into the map \"" + scene.get_map_path() + " \" for loading into the scene \"" + self.get_name() + "\" does not exist.")
    
    def new_object(self, name: str, type: str, parent: bs.Transform_Object = None, position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1), texture_path: str = "") -> bs.Transform_Object:
        """Create a new object into the scene and return it

        Args:
            name (str): name of the object
            type (str): type of the object

        Return:
            bs.Transform_Object: object created
        """
        if parent == None:
            parent = self
        position = (position[0] * self.get_transform_multiplier(), position[1] * self.get_transform_multiplier(), position[2] * self.get_transform_multiplier())
        vbo = self.get_advanced_struct().get_all_vbos()[type]

        # If the texture is empty
        if type == "cube":
            if texture_path == "": texture_path = "textures/unknow"
        else:
            if texture_path == "": texture_path = "textures/unknow.png"

        # Get/load textures
        splitted = texture_path.split(".")
        texture = ""
        if splitted[-1] == ".png" or splitted[-1] == ".jpg":
            if list(self.textures.keys()).count(texture_path) <= 0:
                texture = model.Texture(self.get_advanced_struct().get_base_struct(), texture_path)
                self.textures[texture_path] = texture
            else:
                texture = self.textures[texture]
        else:
            all_files = bs.get_all_files(texture_path)
            texture = []
            for file in all_files:
                if list(self.textures.keys()).count(file) <= 0:
                    tex = model.Texture(self.get_advanced_struct().get_base_struct(), file[0])
                    texture.append(tex)
                    self.textures[file] = tex
                else:
                    texture.append(self.textures[file])

        # Add the object into the scene
        if type == "cube":
            object = model.Cube_Object(self.get_advanced_struct().get_base_struct(), texture = texture, vbo = vbo, parent = parent, position = position, rotation = rotation, scale = scale, type = type)
            self.add_object(name, object)
            return object
        else:
            object = model.Graphic_Object(self.get_advanced_struct().get_base_struct(), texture = texture, vbo = vbo, parent = parent, position = position, rotation = rotation, scale = scale, type = type)
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