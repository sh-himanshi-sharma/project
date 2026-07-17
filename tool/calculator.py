import ast
import operator as op
import math

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "round": round,
}

def calculator(arguments):  # Changed: now accepts a dictionary
    """Calculator tool that accepts a dictionary with 'expression' key"""
    # Handle both string and dict input for flexibility
    if isinstance(arguments, str):
        expression = arguments
    else:
        expression = arguments.get("expression", "")
    
    if not expression:
        return "Calculator error: No expression provided"
    
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"
    
def _evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid Function")
        func_name = node.func.id
        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")  # Fixed typo
        args = [_evaluate(arg) for arg in node.args]
        return FUNCTIONS[func_name](*args)
    raise ValueError("UNSUPPORTED EXPRESSION")  # Fixed: return → raise

if __name__ == "__main__":
    # Test with both string and dict input
    print(calculator("25*18"))
    print(calculator({"expression": "25*18"}))
    print(calculator("(45+15)/3"))
    print(calculator({"expression": "(45+15)/3"}))
    print(calculator("sqrt(16)"))