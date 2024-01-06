# Import librairies
import advanced_struct as ad
import base_struct as bs
import glm
import model
import moderngl as mgl
import numpy as np
import pygame as pg
import sys

class Scene_2D:
    """Class representing a 2d scene
    """

    def __init__(self, scene_size: tuple) -> None:
        """Create a 2d scene
        """
        self.scene_size = scene_size

        self.fill(0)

    def fill(self, part: int) -> None:
        """Fill the map with a part

        Args:
            part (int): part to fill
        """
        self.map = []
        for i in range(self.get_scene_size()[1]):
            line = []
            for j in range(self.get_scene_size()[0]):
                line.append(part)
            self.map.append(line)

    def get_part_at(self, x: int, y: int) -> int:
        """Return a part into the map

        Returns:
            int: part into the map
        """
        return self.map[x][y]

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
        size = lines[0]
        size = (int(size.split(" ")[0]), int(size.split(" ")[1]))
        if size == self.get_scene_size():
            for j in range(1, len(lines)):
                line = lines[j]
                if line != "\n" and line != "":
                    for i in range(len(line)):
                        if line[i] != "\n":
                            self.map[i][j - 1] = int(line[i])

class Scene:
    """Class representing a scene (collection of object)
    """

    def __init__(self, advanced_struct: ad.Advanced_Struct) -> None:
        """Create a scene
        """
        self.advanced_struct = advanced_struct
        self.objects = {}
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
    
    def get_transform_multiplier(self) -> float:
        """Return the multiplier for transforming

        Returns:
            float: multiplier for transforming
        """
        return self.transform_multiplier
    
    def new_object(self, name: str, type: str, position = (0, 0, 0), rotation = (0, 0, 0), scale = (0, 0, 0), texture_path: str = "") -> None:
        """Create a new object into the scene

        Args:
            name (str): name of the object
            type (str): type of the object
        """
        parent = None
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
        else:
            object = model.Graphic_Object(self.get_advanced_struct().get_base_struct(), texture = texture, vbo = vbo, parent = parent, position = position, rotation = rotation, scale = scale, type = type)
            self.add_object(name, object)

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