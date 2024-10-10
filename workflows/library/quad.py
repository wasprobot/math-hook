import math
import random

# Quadratic Equations
def create(context):
    a = random.randint(1, 10)  # Ensure 'a' is not zero
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    sol1 = random.randint(-10, 10)
    sol2 = random.randint(-10, 10)

    # create a quadratic equation using sol1 and sol2
    a = 1
    b = -sol1 - sol2
    c = sol1 * sol2

    equation_s = f"x^2"
    
    if b > 0:
        equation_s += f" + {b}x"
    elif b < 0:
        equation_s += f" - {-b}x"

    if c > 0:
        equation_s += f" + {c}"
    elif c < 0:
        equation_s += f" - {-c}"
    
    equation_s += " = 0"
    
    equation = {
        "coefficients": { "a": a, "b": b, "c": c },
        "solutions": [sol1, sol2],
        "text": equation_s
    }

    context["equation"] = equation

    return f"Let's learn to solve {equation_s}. What is the value of a?"

def match_a(context, user_input):
    print(f"quad_match_a: {user_input}, ctx: {context["equation"]["coefficients"]["a"]}")
    if context["equation"]["coefficients"]["a"] == int(user_input):
        return True, None
    return False, "Please provide the correct value for a."

def match_b(context, user_input):
    if context["equation"]["coefficients"]["b"] == int(user_input):
        return True, None
    return False, "Please provide the correct value for b."

def match_c(context, user_input):
    if context["equation"]["coefficients"]["c"] == int(user_input):
        return True, None
    return False, "Please provide the correct value for c."

def match_discriminant(context, user_input):
    a = context["equation"]["coefficients"]["a"]
    b = context["equation"]["coefficients"]["b"]
    c = context["equation"]["coefficients"]["c"]
    discriminant = b**2 - 4*a*c

    if discriminant == int(user_input):
        return True, None
    return False, "Please provide the correct value for the discriminant."

def match_sqrt_discriminant(context, user_input):
    discriminant = int(context["calculate_discriminant"])

    sqrt_discriminant = str(int(math.sqrt(discriminant)))

    if sqrt_discriminant == user_input:
        return True, None
    
    print(f"match_sqrt_discriminant: {sqrt_discriminant}, {user_input}")
    
    return False, "Please provide the correct value for the square root of the discriminant."

def match_solutions(context, user_input):
    solutions = context["equation"]["solutions"]

    print(f"match_solutions: {sorted(solutions)}, {sorted([float(x) for x in user_input.split(',')])}")

    if sorted(solutions) == sorted([float(x) for x in user_input.split(',')]):
        return True, None

    return False, "Please try again. What are the solutions to this equation?"