from dataclasses import dataclass
from typing import Callable, Optional, Tuple
import numpy as np
from sympy import Symbol, sympify
import re

@dataclass
class Equation:
    """Represents a mathematical equation with validation and parsing capabilities."""
    raw_expression: str
    parsed_function: Optional[Callable] = None
    error_message: Optional[str] = None

    # Constants
    VALID_FUNCTIONS = ['log10', 'sqrt']
    MAX_NESTING_DEPTH = 20
    
    def __post_init__(self):
        self.validate_and_parse()

    def validate_and_parse(self) -> bool:
        """Validates and parses the equation, returns True if successful."""
        if not self._validate_syntax():
            return False
        
        try:
            self.parsed_function = self._create_lambda()
            return True
        except Exception as e:
            self.error_message = f"Parsing error: {str(e)}"
            return False

    def _validate_basic_input(self) -> bool:
        """Validates basic input requirements."""
        if not self.raw_expression or self.raw_expression.isspace():
            self.error_message = "Expression cannot be empty or contain only whitespace"
            return False
        return True

    def _validate_parentheses(self) -> bool:
        """Validates parentheses structure and nesting."""
        stack = []
        for i, char in enumerate(self.raw_expression):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if not stack:
                    self.error_message = f"Unmatched closing parenthesis at position {i}"
                    return False
                stack.pop()

        if stack:
            self.error_message = f"Unmatched opening parenthesis at position {stack[0]}"
            return False

        # Check nesting depth
        depth = 0
        max_depth = 0
        for char in self.raw_expression:
            if char == '(':
                depth += 1
                max_depth = max(max_depth, depth)
            elif char == ')':
                depth -= 1

        if max_depth > self.MAX_NESTING_DEPTH:
            self.error_message = f"Parentheses nesting too deep (max allowed: {self.MAX_NESTING_DEPTH})"
            return False

        return True

    def _validate_operators(self) -> bool:
        """Validates operator usage."""
        # Check for consecutive operators
        if re.search(r'[\+\-\*/\^]{2,}', self.raw_expression):
            self.error_message = "Invalid consecutive operators found"
            return False

        # Check operators at start/end
        if re.match(r'^\s*[\+\*/\^]', self.raw_expression):
            self.error_message = "Expression cannot start with an operator (except - for negation)"
            return False

        if re.search(r'[\+\-\*/\^]\s*$', self.raw_expression):
            self.error_message = "Expression cannot end with an operator"
            return False

        # Check operators around parentheses
        if re.search(r'$$\s*[\+\-\*/\^]', self.raw_expression):
            self.error_message = "Operator cannot follow directly after opening parenthesis"
            return False

        if re.search(r'[\+\-\*/\^]\s*$$', self.raw_expression):
            self.error_message = "Operator cannot precede closing parenthesis"
            return False

        return True

    def _validate_variables(self) -> bool:
        """Validates variable usage."""

        # Check for missing operators between terms
        if re.search(r'\d[x]|[x]\d', self.raw_expression):
            self.error_message = "Missing multiplication operator (use '*' between numbers and variables)"
            return False

        return True

    def _validate_functions(self) -> bool:
        """Validates mathematical function usage."""
        # Find all function-like patterns
        found_functions = re.findall(r'[a-zA-Z]+(?=\()', self.raw_expression)
        invalid_functions = [f for f in found_functions if f not in self.VALID_FUNCTIONS]
        
        if invalid_functions:
            self.error_message = (
                f"Invalid function(s): {', '.join(invalid_functions)}. "
                f"Only {', '.join(self.VALID_FUNCTIONS)} are supported"
            )
            return False

        return True

    def _validate_syntax(self) -> bool:
        """Validates equation syntax with comprehensive error checking."""
        # Order of validation is important
        validators = [
            self._validate_basic_input,
            self._validate_parentheses,
            self._validate_operators,
            self._validate_variables,
            self._validate_functions
        ]

        for validator in validators:
            if not validator():
                return False

        # Final sympy validation
        try:
            x = Symbol('x')
            sympify(self.raw_expression.replace('^', '**'))
            return True
        except Exception as e:
            self.error_message = f"Invalid mathematical expression: {str(e)}"
            return False

    def _create_lambda(self) -> Callable:
        """Creates a lambda function from the validated expression."""
        expr = self.raw_expression.replace('^', '**')
        expr = expr.replace('log10', 'np.log10')
        expr = expr.replace('sqrt', 'np.sqrt')
        return lambda x: eval(expr)

    def evaluate(self, x_values: np.ndarray) -> np.ndarray:
        """Evaluates the equation for given x values."""
        if not self.parsed_function:
            raise ValueError("Equation not properly parsed")
        return self.parsed_function(x_values)