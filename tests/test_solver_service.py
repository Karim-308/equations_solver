import pytest
from src.models.equation import Equation
from src.services.solver_service import SolverService

def test_intersection_points():
    eq1 = Equation("x")
    eq2 = Equation("x^2")
    
    solver = SolverService(eq1, eq2)
    points = solver.solve()
    
    assert len(points) == 2
    assert abs(points[0][0]) < 0.1  # Should intersect at x=0
    assert abs(points[1][0] - 1.0) < 0.1  # Should intersect at x=1

def test_no_intersection():
    eq1 = Equation("x + 1")
    eq2 = Equation("x + 2")
    
    solver = SolverService(eq1, eq2)
    points = solver.solve()
    
    assert len(points) == 0
