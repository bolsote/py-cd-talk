"""
Base class and non-recursive visitor implementation.
Code extracted from examples of Python Cookbook, chapter 8, case 8.22
"""

import types


class Node:  # pylint: disable=too-few-public-methods
    """Node base class"""
    pass


class NodeVisitor:
    """Non-recursive visitor implementation"""

    def visit(self, node):
        """Visit the different nodes"""
        stack = [node]
        last_result = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    stack.append(last.send(last_result))
                    last_result = None
                elif isinstance(last, Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    last_result = stack.pop()
            except StopIteration:
                stack.pop()

        return last_result

    def _visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):  # pylint: disable=no-self-use
        """Generic visit function"""
        raise RuntimeError(
            'No {} method'.format(
                'visit_' + type(node).__name__
            )
        )
