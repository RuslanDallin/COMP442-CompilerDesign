from anytree import Node, RenderTree


class myNode(Node):  # Add Node feature
    def __init__(self, name, length, width, parent=None, children=None):
     self.name = name
     self.length = length
     self.width = width
     self.parent = parent
     if children:
         self.children = children

    def __str__(self):
        return "[%s, %s]" % (self.name, self.parent)



my0 = myNode('my0', 0, 0)
my1 = myNode('my1', 1, 0, parent=my0)
my2 = myNode('my2', 0, 2, parent=my0)

for pre, _, node in RenderTree(my0):
    treestr = u"%s%s" % (pre, node.name)
    print(treestr.ljust(8), node.length, node.width)


print("")
class varDeclNode(Node):  # Add Node feature
    def __init__(self, dimList=None, parent=None, children=None):
     self.name = "varDecl"
     if children:
         self.children = children
     self.type = children[1]
     self.id = children[0]
     self.dimList = dimList
     self.parent = parent


    def __str__(self):
        return "[%s, %s, %s]" % (self.name, self.type, self.id)

class typeNode(Node):  # Add Node feature
    def __init__(self, type):
     self.type = type

    def __str__(self):
        return "%s" % (self.type)

class idNode(Node):  # Add Node feature
    def __init__(self, id):
     self.id = id

    def __str__(self):
        return "%s" % (self.id)


# stack = []
type = typeNode("V")
id = idNode("int")

# stack.append(type)
# stack.append(id)
varDecl = varDeclNode(children=[type,id])

for pre, fill, node in RenderTree(varDecl):
    print("%s%s" % (pre, node))

print("")

class arraySizeNode(Node):  # Add Node feature
    def __init__(self, parent=None, children=None):
     self.name = "arraySize"
     if children:
         self.children = children


    def __str__(self):
        return "[%s]" % (self.name)

class intNode(Node):  # Add Node feature
    def __init__(self, int):
     self.int = int

    def __str__(self):
        return "%s" % (self.int)

int = intNode(2)
int2 = intNode(3)
arraySize = arraySizeNode(children=[int,int2])

for pre, fill, node in RenderTree(arraySize):
    print("%s%s" % (pre, node))

print("")

type = typeNode("V")
id = idNode("int")

int = intNode(2)
int2 = intNode(3)
arraySizeNode = arraySizeNode(children=[int,int2])

varDeclNode2 = varDeclNode(children=[typeNode("V"),id,arraySizeNode])

for pre, fill, node in RenderTree(varDeclNode2):
    print("%s%s" % (pre, node))









class progNode(Node):  # Add Node feature
    def __init__(self, dimList=None, parent=None, children=None):
        self.name = "varDecl"
        if children:
            self.children = children
        self.type = children[1]
        self.id = children[0]
        self.dimList = dimList
        self.parent = parent

    def __str__(self):
        return "[%s, %s]" % (self.name, self.parent)

c = Node("ClassList")

PROG = Node("PROG")
Assign = Node("Assign", parent=PROG)
var = Node("var", parent=Assign)
exp = Node("exp", parent=Assign)


for pre, fill, node in RenderTree(PROG):
    print("%s%s" % (pre, node.name))

print("")

# from anytree import NodeMixin, RenderTree
# class MyBaseClass(object):  # Just an example of a base class
#      foo = 4
#
# class MyClass(MyBaseClass, NodeMixin):  # Add Node feature
#     def __init__(self, name, length, width, parent=None, children=None):
#      super(MyClass, self).__init__()
#      self.name = name
#      self.length = length
#      self.width = width
#      self.parent = parent
#      if children:
#          self.children = children
#
#     def __str__(self):
#         return "[%s, %s]" % (self.name, self.parent)
#
# my0 = MyClass('my0', 0, 0)
# my1 = MyClass('my1', 1, 0, parent=my0)
# my2 = MyClass('my2', 0, 2, parent=my0)
#
# for child in my2.siblings:
#     print(child)
#
# for pre, _, node in RenderTree(my0):
#     treestr = u"%s%s" % (pre, node.name)
#     print(treestr.ljust(8), node.length, node.width)