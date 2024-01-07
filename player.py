# Import librairies
import advanced_struct as ad
import base_struct as bs
import glm
import model
import moderngl as mgl
import numpy as np
import pygame as pg
import sys

class Camera(bs.Transform_Object):
    def __init__(self, base_struct: bs.Base_Struct, parent: bs.Transform_Object = None, position: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0), scale: tuple = (1, 1, 1)) -> None:
        """Create a camera object
        """
        super().__init__(parent, position, rotation, scale)
        self.base_struct = base_struct
        self.camera_value = base_struct.get_camera_value()

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct
    
    def get_camera_value(self) -> bs.Camera_Value:
        """Return the values of the camera

        Returns:
            bs.Camera_Value: values of the camera
        """
        return self.camera_value
    
    def handle_camera_move(self) -> None:
        """Handle the move of the camera
        """
        self.get_camera_value().set_position(self.get_absolute_position())

    def handle_camera_rotation(self):
        rel_y = self.get_base_struct().get_mouse_rel_pos()[1]

        self.rotate((0, 0, -rel_y * self.get_camera_value().get_SENSITIVITY()))

        self.get_camera_value().set_yaw(self.get_absolute_rotation()[0])
        self.get_camera_value().set_pitch(self.get_absolute_rotation()[1])
        self.get_camera_value().set_pitch(max(-89, min(89, self.get_camera_value().get_pitch())))

    def handle_camera_vectors(self):
        """Handle the vectors of the camera
        """
        self.get_camera_value().forward = self.get_forward()
        self.get_camera_value().right = self.get_right()
        self.get_camera_value().up = self.get_up()

    def update(self):
        self.handle_camera_move()
        self.handle_camera_rotation()
        self.handle_camera_vectors()

class Player(bs.Transform_Object):
    """Class representing the player
    """

    def __init__(self, advanced_struct: ad.Advanced_Struct, parent: bs.Transform_Object = None, position: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0), scale: tuple = (1, 1, 1)) -> None:
        """Create a player
        """
        super().__init__(parent, position, rotation, scale)
        self.advanced_struct = advanced_struct
        self.camera = Camera(self.get_base_struct(), self)
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
        self.handle_player_move()
        self.handle_player_rotation()
        self.camera.update()
        self.hud.update()
        self.hud.render()