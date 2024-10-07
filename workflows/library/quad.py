import math
import random

# Quadratic Equations
def create(context):
    a = random.randint(1, 10)  # Ensure 'a' is not zero
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)

    equation_s = f"{a}x^2"
    
    if b >= 0:
        equation_s += f" + {b}x"
    else:
        equation_s += f" - {-b}x"

    if c >= 0:
        equation_s += f" + {c}"
    else:
        equation_s += f" - {-c}"
    
    equation_s += " = 0"
    
    equation = {
        "type": "quadratic",
        "coefficients": { "a": a, "b": b, "c": c },
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

    if discriminant >= 0:
        sqrt_discriminant = math.sqrt(discriminant)
    else:
        sqrt_discriminant = math.sqrt(-1*discriminant) + "i"

    if sqrt_discriminant == user_input:
        return True, None
    
    return False, "Please provide the correct value for the square root of the discriminant."