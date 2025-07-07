import numpy as np
from py5 import Sketch
from colorsys import hsv_to_rgb
from typing import Tuple, List
from sub_classes import Agent, Circle


class App(Sketch):
    """Основное приложение"""
    def __init__(self, cmap: Tuple[float] | List[Tuple[float]], 
                 width: int, height: int, dt: float = 1, 
                 circ_visible: bool = False, border_reflect: bool = True) -> None:
        """Инициализирует приложение на py5

        Args:
            cmap (Tuple[float] | List[Tuple[float]]): Цветовая палитра.
            width (int): Ширина экрана.
            height (int): Высота экрана.
            dt (float, optional): Шаг по времени. Defaults to 1.
            circ_visible (bool, optional): Отображать ли круги. Defaults to False.
        """
        super().__init__()
        
        self.canvas_size = (width, height)
        self.circles = [
            Circle(c, r) for c, r in [
                [(0, 400), 80], [(0, -400), 80], 
                [(400, 400), 80], [(-400, -400), 80], 
                [(-400, 400), 80], [(400, -400), 80], 
                [(-400, 0), 80], [(400, 0), 80], 
                [(200, 200), 80], [(-200, -200), 80], 
                [(-200, 200), 80], [(200, -200), 80], 
                [(600, 200), 80], [(-600, -200), 80], 
                [(-600, 200), 80], [(600, -200), 80],
                [(800, 400), 80], [(-800, -400), 80], 
                [(-800, 400), 80], [(800, -400), 80], 
                [(-800, 0), 80], [(800, 0), 80], 
            ]
        ]
        self.max_life = 450
        self.cmap = cmap
        self.agents = self.gen_agents_at_circle(200)
        self.dt = dt
        self.particles = []
        self.frame_counter = 0
        self.circ_visible = circ_visible
        self.border_reflect = border_reflect
        
    def gen_agents_at_circle(self, num_agents: int) -> List[Agent]:
        """Инициализирует агентов с различными направляющими векторами

        Args:
            num_agents (int): Количество агентов.

        Returns:
            agents (List[Agent]): Список агентов
        """
        agents = []
        for idx in range(num_agents):
            angle = 2 * np.pi * idx / num_agents
            vec = (np.sin(angle), np.cos(angle))
            agents.append(Agent(self.get_color(idx), (0, 0), vec))
        return agents

    def to_screen_coord(self, point: np.ndarray) -> np.ndarray:
        """Перевод в экранные координаты

        Args:
            point (np.ndarray): Координаты точки.

        Returns:
            np.ndarray: Экранные координаты точки.
        """
        x, y = point
        return np.array([x + self.width / 2, self.height / 2 - y])
    
    def draw_circles(self) -> None:
        """Отображает окружности"""
        self.no_stroke()
        self.fill("#cccccc")
        for circ in self.circles:
            self.circle(*self.to_screen_coord(circ.center), 2 * circ.radius) 
        
    def process_agents(self) -> None:
        """Делает один шаг по времени и отображает агентов"""
        for agent in self.agents:
            self.particles.append({
                'color': agent.color, 
                'pos': agent.pos.copy(),
                'life': self.max_life,
            })  
            
            if self.border_reflect:
                agent.process_border(self.width, self.height)
            
            agent.step(self.dt, self.circles) 
        self.update_particles()
        
    def update_particles(self) -> None:
        """Обнавляет частицы"""
        for p in self.particles[:]:
            self.stroke(*p['color'], p['life'])
            self.stroke_weight(3)
            self.point(*self.to_screen_coord(p['pos']))
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)
                
    def get_color(self, idx: int) -> Tuple[float, float, float]:
        """Генерирует цвет в градиенте

        Args:
            idx (int): Позиция в градиенте.

        Returns:
            color (Tuple[float, float, float]): Цвет
        """
        if len(self.cmap) == 2:
            start_color = np.array([0, 0.8, 0.9])
            end_color = np.array([1, 0.8, 0.9])
            color = start_color + (end_color - start_color) * idx / self.max_life
        else:
            color = self.cmap
              
        r, g, b = hsv_to_rgb(*color)
        
        return 255 * r, 255 * g, 255 * b

    def settings(self) -> None:
        """Устанавливает размер окна"""
        self.size(*self.canvas_size)

    def setup(self) -> None:
        """Устанавливает настрокий py5"""
        self.rect_mode(self.CORNERS)
        self.background('#000000')

    def draw(self) -> None:
        """Выполняет итерацию приложения"""
        self.background('#000000')
        self.process_agents()
        if self.circ_visible:
            self.draw_circles()
        
        # self.save_frame(f'outp/frame_{self.frame_counter}.png')
        self.frame_counter += 1
        

if __name__ == '__main__':
    app = App(width=1600, height=900, cmap=(130 / 360, 0.9, 0.9), 
              circ_visible=False, border_reflect=True)
    app.run_sketch()
