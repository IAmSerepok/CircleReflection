import numpy as np
from typing import Tuple, List


class Circle:
    """Класс круга"""
    def __init__(self, center: Tuple[float, float] = (0, 0), radius: float = 1) -> None:
        """Инициализация круга

        Args:
            center (Tuple[float, float], optional): Центр круга. Defaults to (0, 0).
            radius (float, optional): Радиус круга. Defaults to 1.
        """
        self.center = np.array(center)
        self.radius = radius
  
    
class Agent:
    """Класс агента, перемещающегося в пространстве"""
    def __init__(self, color: Tuple[float, float, float], pos: Tuple[float, float] = (0, 0), 
                 vec: Tuple[float, float] = (1, 0)):
        """Класс агента

        Args:
            color (Tuple[float, float]): Цвет агента. 
            pos (Tuple[float, float], optional): Позиция агента. Defaults to (0, 0).
            vec (Tuple[float, float], optional): Направляющий вектор движения агента. Defaults to (1, 0).
        """
        self.color = color
        self.pos = np.array(pos)
        self.vec = np.array(vec)
        self.vec = self.vec / np.linalg.norm(self.vec)  
        
    def check_collision(self, circ: Circle) -> bool:
        """Проверяет столкновение с кругом"""
        return np.linalg.norm(circ.center - self.pos) <= circ.radius
    
    def reflect(self, circ: Circle) -> None:
        """Совершает отражение от круга"""
        direction = self.vec / np.linalg.norm(self.vec)
        oc = circ.center - self.pos
        a = np.dot(direction, direction)
        b = -2 * np.dot(oc, direction)
        c = np.dot(oc, oc) - circ.radius ** 2
        
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return  
        
        t = (-b - np.sqrt(discriminant)) / (2 * a)
        intersection_point = self.pos + t * direction

        normal = (intersection_point - circ.center) / circ.radius
        normal = normal / np.linalg.norm(normal)

        self.vec = self.vec - 2 * np.dot(self.vec, normal) * normal
        
    def process_border(self, width: int, height: int):
        if np.abs(self.pos[0]) >= width / 2:
            self.vec *= np.array([-1, 1])
        if np.abs(self.pos[1]) >= height / 2:
            self.vec *= np.array([1, -1])
        
    def step(self, dt: float, circles: List[Circle]):
        """Осуществялет шаг агента

        Args:
            dt (float): Шаг по времени.
            circles (List[Circle]): Круги.
        """
        new_pos = self.pos + dt * self.vec
        
        collision = False
        for circ in circles:
            if np.linalg.norm(circ.center - new_pos) <= circ.radius:

                direction = self.vec / np.linalg.norm(self.vec)
                oc = circ.center - self.pos
                a = np.dot(direction, direction)
                b = -2 * np.dot(oc, direction)
                c = np.dot(oc, oc) - circ.radius**2
                discriminant = b ** 2 - 4 * a * c
                t = (-b - np.sqrt(discriminant)) / (2 * a)
                self.pos = self.pos + t * direction
                
                self.reflect(circ)
                collision = True
                break
        
        if not collision:
            self.pos = new_pos
