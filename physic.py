# Import librairies
import base_struct as bs
import glm

class Collision:
    """Class representating a collision
    """

    def __init__(self) -> None:
        """Create a collision
        """

class Square_Collision(Collision):
    """Class representating a square-shaped collision
    """

    def __init__(self) -> None:
        """Create a square shaped collision
        """

class Physic_Object:
    """Class representating a physic object
    """

    def __init__(self, transform: bs.Transform_Object, collision: Collision = None) -> None:
        """Create a physic object
        """
        self.collision = collision
        self.transform = transform

    def get_collision(self) -> Collision:
        """Return the collision of the object

        Returns:
            Collision: collision of the object
        """
        return self.collision

    def get_transform(self) -> bs.Transform_Object:
        """Return the transform object of the physic object

        Returns:
            bs.Transform_Object: transform object of the physic object
        """
        return self.transform

class Physic_Static_Object(Physic_Object):
    """Class representating a static physic object, heritating from Physic_Object
    """

    def __init__(self, transform: bs.Transform_Object, collision: Collision = None) -> None:
        """Create a static physic object
        """
        super().__init__(transform, collision)
        self.resistance = -1

class Physic_Dynamic_Object(Physic_Object):
    """Class representating a dynamic physic object, heritating from Physic_Object
    """

    def __init__(self, base_struct: bs.Base_Struct, transform: bs.Transform_Object, collision: Collision = None, weight: float = 1) -> None:
        """Create a dynamic physic object
        """
        super().__init__(transform, collision)
        self.base_struct = base_struct
        self.gravity_force = 1
        self.movement = (0, 0, 0)
        self.weight = weight

    def apply_force(self, force: float, vector: tuple) -> None:
        """Apply a force to the object

        Args:
            force (float): force to apply (in newton)
            vector (tuple): vector of the force
        """
        vector = glm.normalize(vector)
        divisor = force / self.get_weight()
        self.set_movement((self.get_movement()[0] + vector[0] * divisor, self.get_movement()[1] + vector[1] * divisor, self.get_movement()[2] + vector[2] * divisor))

    def get_base_struct(self) -> bs.Base_Struct:
        """Return the base struct of the game

        Returns:
            bs.Base_Struct: base struct of the game
        """
        return self.base_struct
    
    def get_gravity_force(self) -> float:
        """Return the gravity force for this object

        Returns:
            float: gravity force for this object
        """
        return self.gravity_force

    def get_movement(self) -> float:
        """Return the movement of the object

        Returns:
            float: movement of the object
        """
        return self.movement

    def get_weight(self) -> float:
        """Return the weight of the object

        Returns:
            float: weight of the object
        """
        return self.weight
    
    def set_gravity_force(self, gravity_force: float) -> None:
        """Change the value of the gravity force

        Args:
            gravity_force (float): new value of the gravity force
        """
        self.gravity_force = gravity_force

    def set_movement(self, movement: tuple) -> None:
        """Change the movement of the object

        Args:
            movement (tuple): new movement of the object
        """
        self.movement = movement

    def update(self) -> None:
        """Update the physic of the transform
        """
        self.apply_force(self.get_base_struct().get_gravity_force() * self.get_gravity_force() * self.get_base_struct().get_delta_time() * self.get_weight(), (0, 1, 0))
        movement = (self.get_movement()[0] * self.get_base_struct().get_delta_time(), self.get_movement()[1] * self.get_base_struct().get_delta_time(), self.get_movement()[2] * self.get_base_struct().get_delta_time())
        self.get_transform().move(movement)