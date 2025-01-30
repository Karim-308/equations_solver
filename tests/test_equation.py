import pytest
import numpy as np
from src.models.equation import Equation


def test_valid_equation():
    eq = Equation("2*x + 1")
    assert eq.error_message is None
    assert eq.parsed_function is not None
    
    x = np.array([1, 2, 3])
    result = eq.evaluate(x)
    np.testing.assert_array_almost_equal(result, np.array([3, 5, 7]))

def test_valid_multiplication():
    eq = Equation("5*x")
    assert eq.error_message is None
    assert eq.parsed_function is not None

    x = np.array([0, 1, 2])
    expected = np.array([0, 5, 10])
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_valid_exponentiation():
    eq = Equation("x**3 + x**2")
    assert eq.error_message is None

    x = np.array([0, 1, 2])
    expected = np.array([0, 2, 12])  # 0^3 + 0^2, 1^3 + 1^2, 2^3 + 2^2
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_valid_logarithm():
    eq = Equation("log10(x)")
    assert eq.error_message is None

    x = np.array([1, 10, 100])
    expected = np.log10(x)
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_valid_trigonometric():
    eq = Equation("sin(x) + cos(x)")
    assert eq.error_message is None

    x = np.array([0, np.pi/2, np.pi])
    expected = np.sin(x) + np.cos(x)
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_valid_square_root():
    eq = Equation("sqrt(x)")
    assert eq.error_message is None

    x = np.array([0, 1, 4])
    expected = np.sqrt(x)
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_valid_mixed_functions():
    eq = Equation("log10(x) + sqrt(x) + sin(x)")
    assert eq.error_message is None

    x = np.array([1, 10])
    expected = np.log10(x) + np.sqrt(x) + np.sin(x)
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_valid_constants():
    eq = Equation("3.14*x + 2.71")
    assert eq.error_message is None

    x = np.array([1, 2])
    expected = 3.14*x + 2.71
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_valid_hyperbolic_functions():
    eq = Equation("sinh(x) + cosh(x)")
    assert eq.error_message is None

    x = np.array([0, 1])
    expected = np.sinh(x) + np.cosh(x)
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)


def test_invalid_equation_missing_operator():
    eq = Equation("2x + 1")  # Missing multiplication operator
    assert eq.error_message is not None
    assert eq.parsed_function is None

def test_invalid_equation_syntax_error():
    eq = Equation("2*x +")  # Incomplete expression
    assert eq.error_message is not None

def test_invalid_unknown_function():
    eq = Equation("unknown_func(x)")
    assert eq.error_message is not None

def test_invalid_division_by_zero():
    eq = Equation("1/(x - x)")
    x = np.array([1, 2, 3])
    with pytest.raises(ZeroDivisionError):
        eq.evaluate(x)

def test_invalid_log_of_negative():
    eq = Equation("log10(-x)")
    x = np.array([1, 2, 3])
    with pytest.raises(ValueError):  # Should raise an error for negative log
        eq.evaluate(x)

def test_invalid_sqrt_of_negative():
    eq = Equation("sqrt(-x)")
    x = np.array([1, 2, 3])
    with pytest.raises(ValueError):  # Should raise an error for negative sqrt
        eq.evaluate(x)

def test_invalid_empty_string():
    eq = Equation("")
    assert eq.error_message is not None

def test_invalid_special_characters():
    eq = Equation("2*x + @#")
    assert eq.error_message is not None

def test_invalid_mixed_variables():
    eq = Equation("x + y")
    assert eq.error_message is not None

def test_invalid_excessive_parentheses():
    eq = Equation("((2*x) + 3))")
    assert eq.error_message is not None

def test_large_numbers():
    eq = Equation("x**10")
    assert eq.error_message is None

    x = np.array([10, 100])
    expected = x**10
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_small_numbers():
    eq = Equation("x**(-2)")
    assert eq.error_message is None

    x = np.array([1, 0.1])
    expected = x**-2
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_large_negative_numbers():
    eq = Equation("x**3")
    assert eq.error_message is None

    x = np.array([-10, -100])
    expected = x**3
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_infinity_handling():
    eq = Equation("1/x")
    assert eq.error_message is None

    x = np.array([1e-100, 1e100])
    expected = 1 / x
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_nan_input():
    eq = Equation("x + 1")
    x = np.array([np.nan])
    result = eq.evaluate(x)
    assert np.isnan(result).all()

def test_zero_handling():
    eq = Equation("1/(x + 1)")
    x = np.array([-1])
    with pytest.raises(ZeroDivisionError):
        eq.evaluate(x)


def test_spaces_in_equation():
    eq = Equation("  2  * x  +  1 ")
    assert eq.error_message is None

    x = np.array([1, 2])
    expected = 2 * x + 1
    np.testing.assert_array_almost_equal(eq.evaluate(x), expected)

def test_tab_characters():
    eq = Equation("\t2*x+1")
    assert eq.error_message is None

def test_mixed_spaces_and_tabs():
    eq = Equation("  \t x^2 \t + 2 ")
    assert eq.error_message is None

def test_trailing_and_leading_whitespace():
    eq = Equation("   x^2 + 1   ")
    assert eq.error_message is None


