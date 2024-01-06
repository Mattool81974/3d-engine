# Import librairies
import base_struct as bs
import glm
import model
import moderngl as mgl
import pygame as pg

class Advanced_Struct:
    """Class representing all the advanced struct in the game
    """

    def __init__(self, base_struct: bs.Base_Struct) -> None:
        """Create an advanced struct class
        """
        self.all_vbos = {}
        self.base_struct = base_struct

        cube_vbo = model.Cube_VBO(self.get_base_struct())
        plan_vbo = model.Triangle_VBO(self.get_base_struct())
        square_vbo = model.Square_VBO(self.get_base_struct())

        self.all_vbos["cube"] = cube_vbo
        self.all_vbos["plan"] = plan_vbo
        self.all_vbos["square"] = square_vbo

    def get_all_vbos(self) -> list:
        """Return a list of alls the VBOs

        Returns:
            list: list of alls the VBOs
        """
        return self.all_vbos

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct