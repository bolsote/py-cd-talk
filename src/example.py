"""
Example:  Recursive implementation
Code extracted from examples of Python Cookbook, chapter 8, case 8.22
"""

from .node import Node, NodeVisitor


class UnaryOperator(Node):  # pylint: disable=too-few-public-methods
    """Operator with a single operand"""
    def __init__(self, operand):
        self.operand = operand


class BinaryOperator(Node):  # pylint: disable=too-few-public-methods
    """Operator with two operands"""
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOperator):  # pylint: disable=too-few-public-methods
    """Addition operation"""
    pass


class Sub(BinaryOperator):  # pylint: disable=too-few-public-methods
    """Substraction operation"""
    pass


class Mul(BinaryOperator):  # pylint: disable=too-few-public-methods
    """Multiplication operation"""
    pass


class Div(BinaryOperator):  # pylint: disable=too-few-public-methods
    """Division operation"""
    pass


class Negate(UnaryOperator):  # pylint: disable=too-few-public-methods
    """Negate operation"""
    pass


class Number(Node):  # pylint: disable=too-few-public-methods
    """Representation of a number"""
    def __init__(self, value):
        self.value = value


class Evaluator(NodeVisitor):
    """ A sample visitor class that evaluates expressions"""

    def visit_number(self, node):  # pylint: disable=no-self-use
        """Visit a number node"""
        return node.value

    def visit_add(self, node):
        """Visit an addition node"""
        return self.visit(node.left) + self.visit(node.right)

    def visit_sub(self, node):
        """Visit a substraction node"""
        return self.visit(node.left) - self.visit(node.right)

    def visit_mul(self, node):
        """Visit a multiplication node"""
        return self.visit(node.left) * self.visit(node.right)

    def visit_div(self, node):
        """Visit a division node"""
        return self.visit(node.left) / self.visit(node.right)

    def visit_negate(self, node):
        """Visit a negation node"""
        # pylint: disable=invalid-unary-operand-type
        return -self.visit(node.operand)


if __name__ == '__main__':

    # 1 + 2*(3-4) / 5
    TERM1 = Sub(Number(3), Number(4))
    TERM2 = Mul(Number(2), TERM1)
    TERM3 = Div(TERM2, Number(5))
    TERM4 = Add(Number(1), TERM3)

    # Evaluate it
    EVAL = Evaluator()
    print(EVAL.visit(TERM4))     # Outputs 0.6

    # Blow it up
    TOTAL = Number(0)
    for n in range(1, 100000):
        TOTAL = Add(TOTAL, Number(n))  # type: ignore

    try:
        print(EVAL.visit(TOTAL))
    except RuntimeError as error:
        print(error)
