from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Node(ABC):
    """
    The Node interface declares an `accept` method that should take the
    base visitor interface as an argument.
    """

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


class ConcreteNodeA(Node):
    """
    Each Concrete Node must implement the `accept` method in such a way
    that it calls the visitor's method corresponding to the Node's class.
    """

    def accept(self, visitor: Visitor) -> None:
        """
        Note that we're calling `visitConcreteNodeA`, which matches the
        current class name. This way we let the visitor know the class of the
        Node it works with.
        """

        visitor.visit_concrete_Node_a(self)

    def uniqueNode_a(self) -> str:
        """
        Concrete Nodes may have special methods that don't exist in their
        base class or interface. The Visitor is still able to use these methods
        since it's aware of the Node's concrete class.
        """

        return "A"


class ConcreteNodeB(Node):
    """
    Same here: visitConcreteNodeB => ConcreteNodeB
    """

    def accept(self, visitor: Visitor):
        visitor.visit_concrete_Node_b(self)

    def uniqueNode_b(self) -> str:
        return "B"


class Visitor(ABC):
    """
    The Visitor Interface declares a set of visiting methods that correspond to
    Node classes. The signature of a visiting method allows the visitor to
    identify the exact class of the Node that it's dealing with.
    """

    @abstractmethod
    def visit_concrete_Node_a(self, element: ConcreteNodeA) -> None:
        pass

    @abstractmethod
    def visit_concrete_Node_b(self, element: ConcreteNodeB) -> None:
        pass


"""
Concrete Visitors implement several versions of the same algorithm, which can
work with all concrete Node classes.

You can experience the biggest benefit of the Visitor pattern when using it with
a complex object structure, such as a Composite tree. In this case, it might be
helpful to store some intermediate state of the algorithm while executing
visitor's methods over various objects of the structure.
"""


class SymTableVisitor(Visitor):
    def visit_concrete_Node_a(self, element: ConcreteNodeA) -> None:
        print(f"{element.uniqueNode_a()} + SymTableVisitor")

    def visit_concrete_Node_b(self, element: ConcreteNodeB) -> None:
        print(f"{element.uniqueNode_b()} + SymTableVisitor")


class SemCheckVisitor(Visitor):
    def visit_concrete_Node_a(self, element: ConcreteNodeA) -> None:
        print(f"{element.uniqueNode_a()} + SemCheckVisitor")

    def visit_concrete_Node_b(self, element: ConcreteNodeB) -> None:
        print(f"{element.uniqueNode_b()} + SemCheckVisitor")


def client_code(Nodes: List[Node], visitor: Visitor) -> None:
    """
    The client code can run visitor operations over any set of elements without
    figuring out their concrete classes. The accept operation directs a call to
    the appropriate operation in the visitor object.
    """

    # ...
    for Node in Nodes:
        Node.accept(visitor)
    # ...


if __name__ == "__main__":
    Nodes = [ConcreteNodeA(), ConcreteNodeB()]

    print("The client code works with all visitors via the base Visitor interface:")
    visitor1 = SymTableVisitor()
    client_code(Nodes, visitor1)

    print("It allows the same client code to work with different types of visitors:")
    visitor2 = SemCheckVisitor()
    client_code(Nodes, visitor2)