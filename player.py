# Import librairies
import advanced_struct as ad
import base_struct as bs
import glm
import model
import moderngl as mgl
import numpy as np
import pygame as pg
import sys

class Player(bs.Transform_Object):
    """Class representing the player
    """

    def __init__(self, advanced_struct: ad.Advanced_Struct, camera: bs.Camera, parent: bs.Transform_Object = None, position: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0), scale: tuple = (1, 1, 1)) -> None:
        """Create a player
        """
        self.advanced_struct = advanced_struct
        super().__init__(self.get_base_struct(), parent, position, rotation, scale)
        self.camera = camera
        self.hud = model.HUD(self.get_base_struct(), self.get_advanced_struct().get_all_vbos()["square"])

        self.forward = glm.vec3(0, 0, -1)
        self.right = glm.vec3(1, 0, 0)
        self.speed = 5
        self.up = glm.vec3(0, 1, 0)

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
    
    def get_speed(self) -> float:
        """Return the speed of the player

        Returns:
            float: speed of the player
        """
        return self.speed
    
    def handle_player_move(self):
        velocity = self.get_speed() * self.get_base_struct().get_delta_time()
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            self.move(self.get_forward() * velocity)
        if keys[pg.K_s]:
            self.move(-self.get_forward() * velocity)
        if keys[pg.K_q]:
            self.move(-self.get_right() * velocity)
        if keys[pg.K_d]:
            self.move(self.get_right() * velocity)
        if keys[pg.K_a]:
            self.move(self.get_up() * velocity)
        if keys[pg.K_w]:
            self.move(-self.get_up() * velocity)

    def handle_player_rotation(self):
        """Handle the rotation of the player
        """
        rel_x = self.get_base_struct().get_mouse_rel_pos()[0]

        self.rotate((rel_x * self.camera.get_camera_value().get_SENSITIVITY(), 0, 0))
    
    def update(self) -> None:
        """Update the player
        """
        self.camera.update()
        self.hud.update()
        self.hud.render()