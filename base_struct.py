# Import librairies
import glm
import moderngl as mgl
import os
import pygame as png

def get_all_files(path: str) -> list:
    """Return a list of file into a directory

    Args:
        path (str): directory to analyse

    Returns:
        list: list of file into the directory
    """
    all_paths = []
    sub_paths = os.listdir(path)
    for p in sub_paths:
        if len(p.split(".")) <= 1:
            for pa in get_all_files(path + "/" + p):
                all_paths.append(pa)
        else:
            extension = str.lower(p.split(".")[-1])
            if extension == "jpg" or extension == "png" or extension == "jpeg":
                all_paths.append((path + "/" + p, p, extension))
    return all_paths

class Transform_Object:
    """Class representing an object which can be transformed
    """

    def __init__(self, parent = None, position: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0), scale: tuple = (1, 1, 1)) -> None:
        """Create an object which can be transformed

        Args:
            position (tuple, optional): position of the plan. Defaults to (0, 0, 0).
            rotation (tuple, optional): rotation of the plan. Defaults to (0, 0, 0).
            scale (tuple, optional): scale of the plan. Defaults to (0, 0, 0).
        """
        self.fixed_position = (True, True, True)
        self.parent = parent
        self.position = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.scale = (1, 1, 1)

        self.set_position(position)
        self.set_rotation(rotation)
        self.set_scale(scale)

        self.forward = glm.vec3(0, 0, -1)
        self.right = glm.vec3(1, 0, 0)
        self.up = glm.vec3(0, 1, 0)

    def get_absolute_position(self, scaled: bool = False) -> tuple:
        """Return the absolute position of the object into the scene

        Returns:
            tuple: absolute position of the object into the scene
        """
        position = self.get_position(scaled)
        if self.get_parent() != None:
            position = (position[0] + self.get_parent().get_absolute_position(scaled)[0], position[1] + self.get_parent().get_absolute_position(scaled)[1], position[2] + self.get_parent().get_absolute_position(scaled)[2])
        return position
    
    def get_absolute_rotation(self) -> tuple:
        """Return the absolute rotation of the object into the scene

        Returns:
            tuple: absolute rotation of the object into the scene
        """
        rotation = self.get_rotation()
        if self.get_parent() != None:
            rotation = (rotation[0] + self.get_parent().get_absolute_rotation()[0], rotation[1] + self.get_parent().get_absolute_rotation()[1], rotation[2] + self.get_parent().get_absolute_rotation()[2])
        return rotation
    
    def get_absolute_scale(self) -> tuple:
        """Return the absolute scale of the object into the scene

        Returns:
            tuple: absolute scale of the object into the scene
        """
        scale = self.get_scale()
        if self.get_parent() != None:
            parent_scale = self.get_parent().get_absolute_scale()
            scale = (scale[0] * parent_scale[0], scale[1] * parent_scale[1], scale[2] * parent_scale[2])
        return scale
    
    def get_fixed_position(self) -> tuple:
        """Return the fixed position into the object

        Returns:
            tuple: fixed position into the object
        """
        return self.fixed_position

    def get_forward(self) -> glm.vec3:
        """Return the forward vector of the object

        Returns:
            glm.vec3: forward vector of the object
        """
        return self.forward

    def get_model_matrix(self) -> glm.mat4x4:
        """Return the model of the matrix

        Returns:
            glm.mat4x4: _description_
        """

        # Translation
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.get_absolute_position(True))

        # Rotation
        m_model = glm.rotate(m_model, glm.radians(self.get_rotation()[0]), glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, glm.radians(self.get_rotation()[1]), glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, glm.radians(self.get_rotation()[2]), glm.vec3(0, 0, 1))

        # Scaling
        m_model = glm.scale(m_model, self.get_absolute_scale())

        return m_model
    
    def get_parent(self):
        """Return the parent of the object
        """
        return self.parent

    def get_position(self, scaled: bool = False) -> tuple:
        """Return the position of the object

        Returns:
            tuple: position of the object
        """
        position = self.position
        if scaled and self.get_parent() != None:
            parent_scale = self.get_parent().get_scale()
            position = (position[0] * parent_scale[0], position[1] * parent_scale[1], position[2] * parent_scale[2])
        return position
    
    def get_right(self) -> glm.vec3:
        """Return the right vector of the object

        Returns:
            glm.vec3: right vector of the object
        """
        return self.right
    
    def get_rotation(self) -> tuple:
        """Return the rotation of the object

        Returns:
            tuple: rotation of the object
        """
        return self.rotation
    
    def get_scale(self) -> tuple:
        """Return the scale of the object

        Returns:
            tuple: scale of the object
        """
        return self.scale
    
    def get_up(self) -> glm.vec3:
        """Return the up vector of the object

        Returns:
            glm.vec3: up vector of the object
        """
        return self.up
    
    def move(self, translation: tuple) -> None:
        """Move the object

        Args:
            translation (tuple): vector 3d of the translation
        """
        x_transform = translation[0]
        if not self.get_fixed_position()[0]: x_transform = 0
        y_transform = translation[1]
        if not self.get_fixed_position()[1]: y_transform = 0
        z_transform = translation[2]
        if not self.get_fixed_position()[2]: z_transform = 0
        self.set_position((self.get_position()[0] + x_transform, self.get_position()[1] + y_transform, self.get_position()[2] + z_transform))

    def rotate(self, rotation: tuple) -> None:
        """Rotate the object

        Args:
            rotation (tuple): vector 3d of the rotation
        """
        x_rotation = rotation[0]
        y_rotation = rotation[1]
        z_rotation = rotation[2]

        self.set_rotation((self.get_rotation()[0] + x_rotation, self.get_rotation()[1] + y_rotation, self.get_rotation()[2] + z_rotation))
        self.update_vectors()

    def set_fixed_position(self, fixed_position: tuple) -> None:
        """Change the value of the fixed position

        Args:
            fixed_position (tuple): new value of the fixed position
        """
        self.fixed_position = fixed_position

    def set_position(self, position: tuple) -> None:
        """Change the position of the object

        Args:
            position (tuple): new position of the object
        """
        self.position = position

    def set_rotation(self, rotation: tuple) -> None:
        """Change the rotation of the object

        Args:
            rotation (tuple): rotation of the object
        """
        self.rotation = rotation

    def set_scale(self, scale: tuple):
        """Change the scale of the object

        Args:
            scale (tuple): scale of the object
        """
        self.scale = scale
    
    def update(self) -> None:
        """Update the object
        """

    def update_vectors(self):
        x, y, z = glm.radians(self.get_absolute_rotation()[0]), glm.radians(self.get_absolute_rotation()[1]), glm.radians(self.get_absolute_rotation()[2])

        self.forward.x = glm.cos(x) * glm.cos(z)
        self.forward.y = glm.sin(z)
        self.forward.z = glm.sin(x) * glm.cos(z)

        self.forward = glm.normalize(self.get_forward())
        self.right = glm.normalize(glm.cross(self.get_forward(), glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.get_right(), self.get_forward()))

class Camera_Value:
    """Class representing the value of the camera
    """

    def __init__(self, aspect_ratio: float, position = (0, 0, 0), yaw = -90, pitch = 0) -> None:
        """Create values for the camera
        """
        self.aspect_ratio = aspect_ratio
        self.FAR = 100
        self.FOV = 50
        self.NEAR = 0.1
        self.SENSITIVITY = 0.05
        self.SPEED = 5

        self.position = glm.vec3(position)
        self.pitch = pitch
        self.yaw = yaw

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

    def get_aspect_ratio(self) -> float:
        """Return the aspect ratio of the screen

        Returns:
            float: aspect ratio of the screen
        """
        return self.aspect_ratio
    
    def get_FAR(self) -> float:
        """Return far to the camera

        Returns:
            float: far to the camera
        """
        return self.FAR
    
    def get_forward(self) -> glm.vec3:
        """Return the forward vector

        Returns:
            glm.vec3: forward vector
        """
        return self.forward
    
    def get_FOV(self) -> float:
        """Return the fov of the camera

        Returns:
            float: fov of the camera
        """
        return self.FOV
    
    def get_NEAR(self) -> float:
        """Return near to the camera

        Returns:
            float: near to the camera
        """
        return self.NEAR

    def get_pitch(self) -> float:
        """Return the pitch of the camera

        Returns:
            float: pitch of the camera
        """
        return self.pitch

    def get_position(self) -> glm.vec3:
        """Return the position of the camera

        Returns:
            tuple: _position of the camera
        """
        return self.position
    
    def get_projection(self) -> glm.mat4:
        """Return the projection of the camera

        Returns:
            glm.mat4: projection of the camera
        """
        return glm.perspective(glm.radians(self.get_FOV()), self.get_aspect_ratio(), self.get_NEAR(), self.get_FAR())
    
    def get_right(self) -> glm.vec3:
        """Return the right vector

        Returns:
            glm.vec3: right vector
        """
        return self.right
    
    def get_SENSITIVITY(self) -> float:
        """Return the sensitivity of the camera

        Returns:
            float: sensitivity of the camera
        """
        return self.SENSITIVITY
    
    def get_SPEED(self) -> float:
        """Return the speed of the camera

        Returns:
            float: speed of the camera
        """
        return self.SPEED
    
    def get_up(self) -> glm.vec3:
        """Return the up vector

        Returns:
            glm.vec3: up vector
        """
        return self.up
    
    def get_view(self) -> glm.mat4x4:
        """Return the view matrix

        Returns:
            glm.mat4x4: view matrix
        """
        return glm.lookAt(self.get_position(), self.get_position() + self.get_forward(), self.get_up())
    
    def get_yaw(self) -> float:
        """Return the yaw of the camera

        Returns:
            float: yaw of the camera
        """
        return self.yaw
    
    def set_position(self, position: glm.vec3) -> None:
        """Change the position of the camera

        Args:
            position (vec3): position of the camera
        """
        self.position = position

    def set_pitch(self, pitch: float) -> None:
        """Change the pitch of the camera

        Args:
            pitch (float): new pitch of the camera
        """
        self.pitch = pitch

    def set_yaw(self, yaw: float) -> None:
        """Change the yaw of the camera

        Args:
            yaw (float): new yaw of the camera
        """
        self.yaw = yaw

class Base_Struct:
    """Class representing all the base struct in the game
    """

    def __init__(self, context: mgl.Context, window_size: tuple) -> None:
        """Create a base struct in the game
        """
        self.context = context
        self.context.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.delta_time = 0
        self.mouse_rel_pos = (0, 0)
        self.window_size = window_size

        self.camera_value = Camera_Value(self.get_window_size()[0] / self.get_window_size()[1])

        self.texture_count = 128

    def get_camera_value(self) -> Camera_Value:
        """Return the camera value

        Returns:
            Camera_Value: camera value
        """
        return self.camera_value

    def get_context(self) -> mgl.Context:
        """Return the Context of the game

        Returns:
            mgl.Context: Context of the game
        """
        return self.context
    
    def get_delta_time(self) -> float:
        """Return the delta time in seconds

        Returns:
            float: delta time in seconds
        """
        return self.delta_time
    
    def get_mouse_rel_pos(self) -> tuple:
        """Return the relative pos of the mouse

        Returns:
            tuple: relative pos of the mouse
        """
        return self.mouse_rel_pos
    
    def get_texture_count(self) -> int:
        """Return the number of texture into the game

        Returns:
            int: number of texture into the game
        """
        return self.texture_count
    
    def get_window_size(self) -> tuple:
        """Return the size of the window

        Returns:
            tuple: size of the window
        """
        return self.window_size
    
    def set_delta_time(self, delta_time: float) -> None:
        """Change the value of the delta time

        Args:
            delta_time (float): new value of the delta time
        """
        self.delta_time = delta_time

    def set_mouse_rel_pos(self, mouse_rel_pos: tuple) -> None:
        """Change the value of the mouse rel pos

        Args:
            mouse_rel_pos (tuple): new value of the mouse rel pos
        """
        self.mouse_rel_pos = mouse_rel_pos

    def set_texture_count(self, texture_count: int) -> None:
        """Change the texture count into the game

        Args:
            texture_count (int): texture count into the game
        """
        self.texture_count = texture_count