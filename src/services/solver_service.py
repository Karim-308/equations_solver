from typing import List, Tuple
import numpy as np
from scipy.optimize import fsolve
from ..models.equation import Equation

class SolverService:
    """Service class for solving and analyzing equations."""
    
    def __init__(self, eq1: Equation, eq2: Equation):
        self.eq1 = eq1
        self.eq2 = eq2
        # Increase range and resolution
        self.x_range = np.linspace(-10, 10, 2000)
        self.intersection_points: List[Tuple[float, float]] = []

    def difference_function(self, x):
        """Returns the difference between the two equations."""
        return self.eq1.evaluate(np.array([x]))[0] - self.eq2.evaluate(np.array([x]))[0]

    def solve(self) -> List[Tuple[float, float]]:
        """Finds intersection points using both sign changes and numerical optimization."""
        y1 = self.eq1.evaluate(self.x_range)
        y2 = self.eq2.evaluate(self.x_range)
        
        # Find rough intersection points using sign changes
        potential_xs = []
        for i in range(len(self.x_range) - 1):
            if np.sign(y1[i] - y2[i]) != np.sign(y1[i+1] - y2[i+1]):
                x_guess = (self.x_range[i] + self.x_range[i+1]) / 2
                potential_xs.append(x_guess)

        # Refine each potential intersection using fsolve
        self.intersection_points = []
        tolerance = 1e-6
        
        for x_guess in potential_xs:
            x_solution = fsolve(self.difference_function, x_guess)[0]
            # Check if it's a valid solution and not a duplicate
            if abs(self.difference_function(x_solution)) < tolerance:
                y_solution = self.eq1.evaluate(np.array([x_solution]))[0]
                if not any(abs(x - x_solution) < tolerance for x, _ in self.intersection_points):
                    self.intersection_points.append((x_solution, y_solution))

        return sorted(self.intersection_points, key=lambda x: x[0])

    def get_plot_data(self) -> tuple:
        """Returns data needed for plotting."""
        y1 = self.eq1.evaluate(self.x_range)
        y2 = self.eq2.evaluate(self.x_range)
        return self.x_range, y1, y2