# Import librairies
import advanced_struct as ad
import base_struct as bs
import model
import moderngl as mgl
import os
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

        # Initialize pygame OpenGL context
        WINDOW_SIZE = (1600, 900)
        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_COMPATIBILITY)
        self.window = pg.display.set_mode(WINDOW_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Initialize games structures
        self.base_struct = bs.Base_Struct(mgl.create_context(), WINDOW_SIZE)
        self.clock = pg.time.Clock()

    def add_physic_scene(self, name: str, scene: sc.Physic_Scene) -> None:
        """Add a physic scene into the game

        Args:
            name (str): name of the physic scene into the game
            scene (sc.Scene): physic scene to add into the game
        """
        if list(self.get_physics_scenes().keys()).count(name) <= 0:
            self.get_physics_scenes()[name] = scene
            return
        print("Matrix game : Warning !! The name \"" + name + " \" for the physic scene you want to add is already used.")
        return None

    def add_scene(self, name: str, scene: sc.Scene) -> None:
        """Add a scene into the game

        Args:
            name (str): name of the scene into the game
            scene (sc.Scene): scene to add into the game
        """
        if list(self.scenes.keys()).count(name) <= 0:
            self.scenes[name] = scene
            return
        print("Matrix game : Warning !! The name \"" + name + " \" for the scene you want to add is already used.")
        return None
    
    def assign_map_part(self, name: str, texture_path: str, type: str = "cube") -> None:
        """Assign to the name "name" a texture for a part into a map

        Args:
            name (str): name of the part
            texture_path (str): texture path of the part
            type (str): type of the part
        """
        if list(self.get_parts().keys()).count(name) <= 0:
            self.get_parts()[name] = model.Part(texture_path, type)
            return
        print("Matrix game : Warning !! The name \"" + name + " \" you try to assign for a part already exist.")
        return

    def destroy(self) -> None:
        """Destroy and end the game
        """
        for scene in list(self.get_scenes().values()):
            scene.destroy()
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
    
    def get_current_scene(self) -> str:
        """Return the current scene of the game

        Returns:
            str: _current scene of the game
        """
        return self.current_scene
    
    def get_parts(self) -> dict:
        """Return the parts assigned into the game

        Returns:
            dict: parts assigned into the game
        """
        return self.parts
    
    def get_physics_scenes(self) -> dict:
        """Return a dict with all the physics scenes

        Returns:
            dict: dict with all the physics scenes
        """
        return self.physic_scenes

    def get_player(self) -> pl.Player:
        """Return the player into the game

        Returns:
            pl.Player: player into the game
        """
        return self.player
    
    def get_scenes(self) -> dict:
        """Return a dict with all the scenes

        Returns:
            dict: dict with all the scenes
        """
        return self.scenes

    def handle_events(self) -> None:
        """Handle all the events
        """
        self.get_base_struct().set_mouse_rel_pos(pg.mouse.get_rel())
        for event in pg.event.get():
            if event.type == pg.QUIT: #If the user wants to leave the game
                self.destroy()
    
    def load_advanced_struct(self) -> None:
        """Start the game
        """
        self.advanced_struct = ad.Advanced_Struct(self.get_base_struct())

    def load_elements(self) -> None:
        """Load main elements in the game
        """
        # Initialize games variables
        self.current_scene = ""
        self.parts = {"0": ""}
        self.physic_scenes = {}
        self.player = pl.Player(self.get_advanced_struct(), position = (0, 4, 0))
        #self.player.set_fixed_position((True, False, True))
        self.scenes = {}

    def new_scene(self, name: str, map_path: str = "") -> sc.Scene:
        """Create a new scene and return the scene

        Args:
            name (str): name of the scene into the game
            map_path (str, optional): path of the map into the scene. Defaults to "".

        Returns:
            (sc.Scene, Object): new scene created and an object which help the creation
        """
        if list(self.scenes.keys()).count(name) <= 0: # If the name does not exist
            scene = sc.Scene(self.get_advanced_struct(), name)
            scene2D = None
            self.add_scene(name, scene)

            if map_path != "": # Load the map into the scene
                if os.path.exists(map_path):
                    map_extension = map_path.split(".")[-1]
                    if map_extension == "wad":
                        scene2D = sc.Scene_2D((25, 25))
                        scene2D.load_map(map_path)
                        scene.load_from_2d_scene(scene2D, self.get_parts())
                else: # If the map does not exist
                    print("Matrix game : Warning !! The map \"" + map_path + " \" for loading into the scene \"" + name + "\" does not exist.")

            return scene
        print("Matrix game : Warning !! The name \"" + name + " \" for the scene you want to create is already used.") # If the name already exists
        return None

    def run(self) -> None:
        """Run the game
        """
        while True:
            self.handle_events()
            self.update()
            delta_time = self.get_clock().tick(5000) * 0.001
            self.get_base_struct().set_delta_time(delta_time)

    def set_current_scene(self, scene: str) -> None:
        """Change the current scene

        Args:
            scene (str): name of the new current scene
        """
        if list(self.scenes.keys()).count(scene) > 0:
            self.current_scene = scene
            return
        print("Matrix game : Warning !! The scene \"" + scene + " \" which you want to be the current scene does not exist.")
        return

    def update(self) -> None:
        """Update the screen
        """
        self.get_base_struct().get_context().clear(255, 255, 255)
        self.get_player().update()
        if list(self.get_scenes().keys()).count(self.get_current_scene()) > 0:
            self.get_scenes()[self.get_current_scene()].update()
        surface = pg.Surface((100, 100))
        surface.fill((0, 0, 0))
        self.window.blit(surface, (50, 50))
        pg.display.flip()