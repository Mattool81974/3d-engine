# Import librairies
import advanced_struct as ad
import base_struct as bs
import model
import moderngl as mgl
import player as pl
import pygame as pg
import scene as sc
import sys

class Game:
    """Class representing the main game
    """

    def __init__(self) -> None:
        """Create a main game
        """
        WINDOW_SIZE = (1600, 900)

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_COMPATIBILITY)

        self.window = pg.display.set_mode(WINDOW_SIZE, flags=pg.OPENGLBLIT | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.base_struct = bs.Base_Struct(mgl.create_context(), WINDOW_SIZE)

        self.advanced_struct = ad.Advanced_Struct(self.get_base_struct())
        self.clock = pg.time.Clock()

        self.player = pl.Player(self.get_advanced_struct(), position = (0, 2, 0))
        self.scene = sc.Scene(self.get_advanced_struct())

        self.scene.new_object("sol", "cube", scale = (27, 1, 27))
        self.scene.new_object("mur1", "cube", position = (13, 2.3, 0), rotation = (0, 0, 0), scale = (1, 5, 27), texture_path = "textures/cobble")
        self.scene.new_object("mur2", "cube", position = (0, 2.3, 13), rotation = (0, 0, 0), scale = (25, 5, 1), texture_path = "textures/cobble")
        self.scene.new_object("mur3", "cube", position = (-13, 2.3, 0), rotation = (0, 0, 0), scale = (1, 5, 27), texture_path = "textures/cobble")
        self.scene.new_object("mur4", "cube", position = (0, 2.3, -13), rotation = (0, 0, 0), scale = (25, 5, 1), texture_path = "textures/cobble")

        sc2d = sc.Scene_2D((25, 25))
        sc2d.load_map("maps/level0.txt")
        for j in range(sc2d.get_scene_size()[1]):
            for i in range(sc2d.get_scene_size()[0]):
                if sc2d.get_part_at(i, j) == 1:
                    self.scene.new_object(str(i) + ";" + str(j), "cube", position = (12 - 1 * i, 2.5, 12 - 1 * j), scale = (1, 5, 1), texture_path = "textures/cobble")

    def destroy(self) -> None:
        """Destroy and end the game
        """
        self.get_scene().destroy()
        pg.quit()
        sys.exit()

    def get_advanced_struct(self) -> ad.Advanced_Struct:
        """Return the advanced struct of the game

        Returns:
            ad.Advanced_Struct: advanced struct of the game
        """
        return self.advanced_struct

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the Base_Struct of the game

        Returns:
            bs.Base_Struct: Base_Struct of the game
        """
        return self.base_struct
    
    def get_clock(self) -> pg.time.Clock:
        """Return the clock into the game

        Returns:
            pg.time.Clock: clock into the game
        """
        return self.clock
    
    def get_player(self) -> pl.Player:
        """Return the player into the game

        Returns:
            pl.Player: player into the game
        """
        return self.player
    
    def get_scene(self) -> sc.Scene:
        """Return the scene rendered

        Returns:
            sc.Scene: scene rendered
        """
        return self.scene

    def handle_events(self) -> None:
        """Handle all the events
        """
        self.get_base_struct().set_mouse_rel_pos(pg.mouse.get_rel())
        for event in pg.event.get():
            if event.type == pg.QUIT: #If the user wants to leave the game
                self.destroy()

    def run(self) -> None:
        """Run the game
        """
        while True:
            self.handle_events()
            self.update()
            delta_time = self.get_clock().tick(5000) * 0.001
            self.get_base_struct().set_delta_time(delta_time)

    def update(self) -> None:
        """Update the screen
        """
        self.get_base_struct().get_context().clear(255, 255, 255)
        self.get_player().update()
        self.get_scene().update()
        self.get_scene().render()
        surface = pg.Surface((100, 100))
        surface.fill((0, 0, 0))
        self.window.blit(surface, (50, 50))
        pg.display.flip()