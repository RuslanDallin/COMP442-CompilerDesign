class Courses_At_GFG:

    def accept(self, visitor):
        visitor.visit(self)

    def teaching(self, visitor):
        print(self, "Taught by ", visitor)

    def studying(self, visitor):
        print(self, "studied by ", visitor)

    def __str__(self):
        return self.__class__.__name__


"""Concrete Courses_At_GFG class: Classes being visited."""
class A(Courses_At_GFG):
    def uniqueA(self):
        print("A")
class B(Courses_At_GFG):
    def uniqueB(self):
        print("B")
class C(Courses_At_GFG):
    def uniqueC(self):
        print("C")


""" Abstract Visitor class for Concrete Visitor classes:
 method defined in this class will be inherited by all
 Concrete Visitor classes."""

class Visitor:
    def __str__(self):
        return self.__class__.__name__
""" Concrete Visitors: Classes visiting Concrete Course objects.
 These classes have a visit() method which is called by the
 accept() method of the Concrete Course_At_GFG classes."""

class Instructor(Visitor):
    def visit(self, concreteNode):
        concreteNode.teaching(self)


class Student(Visitor):
    def visit(self, concreteNode):
        concreteNode.studying(self)


"""creating objects for concrete classes"""
A = A()
B = B()
C = C()

"""Creating Visitors"""
instructor = Instructor()
student = Student()

"""Visitors visiting courses"""
A.accept(instructor)
A.accept(student)

B.accept(instructor)
B.accept(student)

C.accept(instructor)
C.accept(student)