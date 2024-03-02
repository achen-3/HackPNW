import sympy as sp
import random

def generate_and_solve_math_problem():
	x = sp.symbols('x')
	operator = random.choice(['+', '-', '*', '/', 'log', 'exp', 'algebra'])
	
	if operator == 'algebra':
		# Generate a, b, c such that b^2 - 4ac is a perfect square
		a = random.randint(1, 10)
		perfect_square = random.choice([i**2 for i in range(1, 11)])  # perfect squares from 1 to 100
		b = random.randint(-10, 10)
		c = (b**2 - perfect_square) // (4*a)
		superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
		equation = f"{a}x{str(2).translate(superscript)} + {b}x + {c} = 0"
		solution = sp.solve(sp.Eq(a * x**2 + b * x + c, 0), x)
		solution = ', '.join([f"x = {round(sol.evalf(), 2)}" for sol in solution])
	else:
		num1 = random.randint(1, 10)
		num2 = random.randint(1, 10)
		if operator == '+':
			equation = f"{num1} + {num2} = "
			solution = round(num1 + num2, 2)
		elif operator == '-':
			equation = f"{num1} - {num2} = "
			solution = round(num1 - num2, 2)
		elif operator == '*':
			equation = f"{num1} x {num2} = "
			solution = round(num1 * num2, 2)
		elif operator == '/':
			equation = f"{num1} ÷ {num2} = "
			solution = round(num1 / num2, 2)
		elif operator == 'log':
			subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
			equation = f"log{str(num1).translate(subscript)}(x) = {num2}"
			solution = round(num1 ** num2, 2)
		elif operator == 'exp':
			superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
			equation = f"{num1}{str(num2).translate(superscript)} ="
			solution = round(num1 ** num2, 2)
		else:
			equation = "Invalid operator"
			solution = "N/A"

	return equation, solution

equation, solution = generate_and_solve_math_problem()
print(f"Equation: {equation}\nAnswer: {solution}")