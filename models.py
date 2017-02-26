import re


########################################################################################################################
class Node(object):
    """Base object in a Rex tree"""

    ####################################################################################################################
    def __init__(self, name, literal, prefix="", suffix="", escape=False, parent=None):
        self.name = name
        self.literal = literal
        self.prefix = prefix
        self.suffix = suffix
        self.children = []
        self.parent = parent
        self.escape = escape

    ####################################################################################################################
    def __str__(self):
        s = "<{name}: '{prefix}{literal}{children}{suffix}'>"
        return s.format(name=self.name,
                        prefix=self.prefix,
                        literal=self.literal,
                        children="<children>" if self.children else "",
                        suffix=self.suffix)

    ####################################################################################################################
    def __repr__(self):
        return self.__str__()

    ####################################################################################################################
    def add_child(self, node):
        node.parent = self
        print("\tAdded parent: {}".format(node.parent))
        self.children.append(node)
        print("\tAdded as child node to {}".format(self))

    ####################################################################################################################
    def add_children(self, nodes):
        for n in nodes:
            n.parent = self
            print("\tAdded {} as parent.".format(self))

        self.children.extend(nodes)
        print("\nAdded {} as children to {}".format(nodes, self))

    ####################################################################################################################
    def serialize(self):
        print("SERIALIZING: {}".format(self))

        print("ESCAPING: {}".format(self.escape))
        if self.escape:
            self.prefix = re.escape(self.prefix)
            self.literal = re.escape(self.literal)
            self.suffix = re.escape(self.suffix)

        print("Prefix: {}".format(self.prefix))
        yield self.prefix

        print("Literal: {}".format(self.literal))
        yield self.literal

        for child in self.children:
            yield from child.serialize()

        print("Suffix: {}".format(self.suffix))
        yield self.suffix


########################################################################################################################
class Rex(object):
    """Builds elements of a regular expression into a tree data structure
    using Node objects. The primary node is stored on the attribute 'root'."""

    ####################################################################################################################
    def __init__(self):
        self.root = Node("root", "")
        self.last_added = self.root
        self.parent = self.root
        self.modifiers = []

    ####################################################################################################################
    def compile(self):
        return re.compile(self.expression())

    ####################################################################################################################
    def expression(self):
        return "".join(self.root.serialize())

    ####################################################################################################################
    def add_node(self, name, literal, prefix="", suffix="", parent=None):
        node = Node(name, literal, prefix=prefix, suffix=suffix)
        print("\nCreating new node: {}".format(node))

        self.last_added = node
        self.parent.add_child(node)

        if self.modifiers:
            print("\nAdding modifiers: {}".format(self.modifiers))
            self.parent.add_children(self.modifiers)
            self.modifiers = []

    ####################################################################################################################
    @property
    def start(self):
        self.add_node("start", "^")
        return self

    ####################################################################################################################
    @property
    def end(self):
        self.add_node("end", "$")
        return self

    ####################################################################################################################
    @property
    def group(self):
        self.add_node("group", "(", suffix=")")
        self.parent = self.last_added
        return self

    ####################################################################################################################
    @property
    def end_group(self):
        original_parent = self.parent
        self.parent = self.parent.parent
        print("\nModifier node 'end_group':\n\tChanged parent from {original} to {new}".format(original=original_parent, new=self.parent))
        return self

    ####################################################################################################################
    @property
    def any_character(self):
        self.add_node("any_character", ".")
        return self

    ####################################################################################################################
    @property
    def optional(self):
        self.add_node("optional", "?")
        return self

    ####################################################################################################################
    @property
    def digits(self):
        print("digits: adding prefix and suffix.")
        self.last_added.prefix = "\d{"
        self.last_added.suffix = "}"
        return self

    ####################################################################################################################
    @property
    def numbers(self):
        return self.digits

    ####################################################################################################################
    @property
    def exactly(self):
        self.add_node("exactly", "{", suffix="}", parent=self.last_added)
        return self

    ####################################################################################################################
    @property
    def zero_or_more_of(self):
        node = Node("zero_or_more_of", "*")
        self.modifiers.append(node)
        return self

    ####################################################################################################################
    @property
    def zero_or_more_of_any_character(self):
        self.add_node("zero_or_more_of_any_character", ".*")
        return self

    ####################################################################################################################
    @property
    def zero_or_more_numbers(self):
        self.add_node("zero_or_more_numbers", "\d*")
        return self

    ####################################################################################################################
    @property
    def one_or_more_numbers(self):
        self.add_node("one_or_more_numbers", "\d+")
        return self

    ####################################################################################################################
    @property
    def thru(self):
        self.add_node("thru", "\-")
        return self

    ####################################################################################################################
    @property
    def backtick(self):
        self.add_node("backtick", "`")
        return self

    ####################################################################################################################
    @property
    def tilde(self):
        self.add_node("tilde", "~")
        return self

    ####################################################################################################################
    @property
    def exclamation_point(self):
        self.add_node("exclamation_point", "!")
        return self

    ####################################################################################################################
    @property
    def at(self):
        self.add_node("at", "@")
        return self

    ####################################################################################################################
    @property
    def hash(self):
        self.add_node("hash", "#")
        return self

    ####################################################################################################################
    @property
    def dollar(self):
        self.add_node("dollar", "\$")
        return self

    ####################################################################################################################
    @property
    def percent(self):
        self.add_node("percent", "%")
        return self

    ####################################################################################################################
    @property
    def caret(self):
        self.add_node("caret", "\^")
        return self

    ####################################################################################################################
    @property
    def ampersand(self):
        self.add_node("ampersand", "&")
        return self

    ####################################################################################################################
    @property
    def asterisk(self):
        self.add_node("asterisk", "\*")
        return self

    ####################################################################################################################
    @property
    def dash(self):
        self.add_node("dash", "-")
        return self

    ####################################################################################################################
    @property
    def underscore(self):
        self.add_node("underscore", "_")
        return self

    ####################################################################################################################
    @property
    def colon(self):
        self.add_node("colon", ":")
        return self

    ####################################################################################################################
    @property
    def plus(self):
        self.add_node("plus", "\+")
        return self

    ####################################################################################################################
    @property
    def equal(self):
        self.add_node("equal", "=")
        return self

    ####################################################################################################################
    @property
    def dot(self):
        self.add_node("dot", "\.")
        return self

    ####################################################################################################################
    @property
    def backslash(self):
        self.add_node("backslash", "\\")
        return self

    ####################################################################################################################
    @property
    def forwardslash(self):
        self.add_node("forwardslash", "\/")
        return self

    ####################################################################################################################
    @property
    def open_bracket(self):
        self.add_node("open_bracket", "\[")
        return self

    ####################################################################################################################
    @property
    def close_bracket(self):
        self.add_node("close_bracket", "\]")
        return self

    ####################################################################################################################
    @property
    def less_than_sign(self):
        self.add_node("less_than_sign", "<")
        return self

    ####################################################################################################################
    @property
    def greater_than_sign(self):
        self.add_node("greater_than_sign", ">")
        return self

    ####################################################################################################################
    @property
    def pipe(self):
        self.add_node("pipe", "\|")
        return self

    ####################################################################################################################
    @property
    def open_parenthesis(self):
        self.add_node("open_parenthesis", "\(")
        return self

    ####################################################################################################################
    @property
    def close_parenthesis(self):
        self.add_node("close_parenthesis", "\)")
        return self

    ####################################################################################################################
    @property
    def single_space(self):
        self.add_node("single_space", "\s")
        return self

    ####################################################################################################################
    @property
    def question_mark(self):
        self.add_node("question_mark", "\?")
        return self

    ####################################################################################################################
    @property
    def single_quote(self):
        self.add_node("single_quote", "'")
        return self

    ####################################################################################################################
    @property
    def double_quote(self):
        self.add_node("double_quote", '"')
        return self

    ####################################################################################################################
    @property
    def a(self):
        self.add_node("a", "a")
        return self

    ####################################################################################################################
    @property
    def b(self):
        self.add_node("b", "b")
        return self

    ####################################################################################################################
    @property
    def c(self):
        self.add_node("c", "c")
        return self

    ####################################################################################################################
    @property
    def d(self):
        self.add_node("d", "d")
        return self

    ####################################################################################################################
    @property
    def e(self):
        self.add_node("e", "e")
        return self

    ####################################################################################################################
    @property
    def f(self):
        self.add_node("f", "f")
        return self

    ####################################################################################################################
    @property
    def g(self):
        self.add_node("g", "g")
        return self

    ####################################################################################################################
    @property
    def h(self):
        self.add_node("h", "h")
        return self

    ####################################################################################################################
    @property
    def i(self):
        self.add_node("i", "i")
        return self

    ####################################################################################################################
    @property
    def j(self):
        self.add_node("j", "j")
        return self

    ####################################################################################################################
    @property
    def k(self):
        self.add_node("k", "k")
        return self

    ####################################################################################################################
    @property
    def l(self):
        self.add_node("l", "l")
        return self

    ####################################################################################################################
    @property
    def m(self):
        self.add_node("m", "m")
        return self

    ####################################################################################################################
    @property
    def n(self):
        self.add_node("n", "n")
        return self

    ####################################################################################################################
    @property
    def o(self):
        self.add_node("o", "o")
        return self

    ####################################################################################################################
    @property
    def p(self):
        self.add_node("p", "p")
        return self

    ####################################################################################################################
    @property
    def q(self):
        self.add_node("q", "q")
        return self

    ####################################################################################################################
    @property
    def r(self):
        self.add_node("r", "r")
        return self

    ####################################################################################################################
    @property
    def s(self):
        self.add_node("s", "s")
        return self

    ####################################################################################################################
    @property
    def t(self):
        self.add_node("t", "t")
        return self

    ####################################################################################################################
    @property
    def u(self):
        self.add_node("u", "u")
        return self

    ####################################################################################################################
    @property
    def v(self):
        self.add_node("v", "v")
        return self

    ####################################################################################################################
    @property
    def w(self):
        self.add_node("w", "w")
        return self

    ####################################################################################################################
    @property
    def x(self):
        self.add_node("x", "x")
        return self

    ####################################################################################################################
    @property
    def y(self):
        self.add_node("y", "y")
        return self

    ####################################################################################################################
    @property
    def z(self):
        self.add_node("z", "z")
        return self

    ####################################################################################################################
    @property
    def A(self):
        self.add_node("A", "A")
        return self

    ####################################################################################################################
    @property
    def B(self):
        self.add_node("B", "B")
        return self

    ####################################################################################################################
    @property
    def C(self):
        self.add_node("C", "C")
        return self

    ####################################################################################################################
    @property
    def D(self):
        self.add_node("D", "D")
        return self

    ####################################################################################################################
    @property
    def E(self):
        self.add_node("E", "E")
        return self

    ####################################################################################################################
    @property
    def F(self):
        self.add_node("F", "F")
        return self

    ####################################################################################################################
    @property
    def G(self):
        self.add_node("G", "G")
        return self

    ####################################################################################################################
    @property
    def H(self):
        self.add_node("H", "H")
        return self

    ####################################################################################################################
    @property
    def I(self):
        self.add_node("I", "I")
        return self

    ####################################################################################################################
    @property
    def J(self):
        self.add_node("J", "J")
        return self

    ####################################################################################################################
    @property
    def K(self):
        self.add_node("K", "K")
        return self

    ####################################################################################################################
    @property
    def L(self):
        self.add_node("L", "L")
        return self

    ####################################################################################################################
    @property
    def M(self):
        self.add_node("M", "M")
        return self

    ####################################################################################################################
    @property
    def N(self):
        self.add_node("N", "N")
        return self

    ####################################################################################################################
    @property
    def O(self):
        self.add_node("O", "O")
        return self

    ####################################################################################################################
    @property
    def P(self):
        self.add_node("P", "P")
        return self

    ####################################################################################################################
    @property
    def Q(self):
        self.add_node("Q", "Q")
        return self

    ####################################################################################################################
    @property
    def R(self):
        self.add_node("R", "R")
        return self

    ####################################################################################################################
    @property
    def S(self):
        self.add_node("S", "S")
        return self

    ####################################################################################################################
    @property
    def T(self):
        self.add_node("T", "T")
        return self

    ####################################################################################################################
    @property
    def U(self):
        self.add_node("U", "U")
        return self

    ####################################################################################################################
    @property
    def V(self):
        self.add_node("V", "V")
        return self

    ####################################################################################################################
    @property
    def W(self):
        self.add_node("W", "W")
        return self

    ####################################################################################################################
    @property
    def X(self):
        self.add_node("X", "X")
        return self

    ####################################################################################################################
    @property
    def Y(self):
        self.add_node("Y", "Y")
        return self

    ####################################################################################################################
    @property
    def Z(self):
        self.add_node("Z", "Z")
        return self

    ####################################################################################################################
    @property
    def _0(self):
        self.add_node("_0", "0")
        return self

    ####################################################################################################################
    @property
    def _1(self):
        self.add_node("_1", "1")
        return self

    ####################################################################################################################
    @property
    def _2(self):
        self.add_node("_2", "2")
        return self

    ####################################################################################################################
    @property
    def _3(self):
        self.add_node("_3", "3")
        return self

    ####################################################################################################################
    @property
    def _4(self):
        self.add_node("_4", "4")
        return self

    ####################################################################################################################
    @property
    def _5(self):
        self.add_node("_5", "5")
        return self

    ####################################################################################################################
    @property
    def _6(self):
        self.add_node("_6", "6")
        return self

    ####################################################################################################################
    @property
    def _7(self):
        self.add_node("_7", "7")
        return self

    ####################################################################################################################
    @property
    def _8(self):
        self.add_node("_8", "8")
        return self

    ####################################################################################################################
    @property
    def _9(self):
        self.add_node("_9", "9")
        return self

    ####################################################################################################################
    @property
    def exclamation_mark(self):
        return self.exclamation_point

    ####################################################################################################################
    @property
    def at_symbol(self):
        return self.at

    ####################################################################################################################
    @property
    def at_sign(self):
        return self.at

    ####################################################################################################################
    @property
    def at_mark(self):
        return self.at

    ####################################################################################################################
    @property
    def hashtag(self):
        return self.hash

    ####################################################################################################################
    @property
    def pound(self):
        return self.hash

    ####################################################################################################################
    @property
    def number_sign(self):
        return self.hash

    ####################################################################################################################
    @property
    def dollar_sign(self):
        return self.dollar

    ####################################################################################################################
    @property
    def percent_sign(self):
        return self.percent

    ####################################################################################################################
    @property
    def percentage(self):
        return self.percent

    ####################################################################################################################
    @property
    def percentage_sign(self):
        return self.percent

    ####################################################################################################################
    @property
    def up_arrow(self):
        return self.caret

    ####################################################################################################################
    @property
    def and_sign(self):
        return self.ampersand

    ####################################################################################################################
    @property
    def star(self):
        return self.star

    ####################################################################################################################
    @property
    def plus_sign(self):
        return self.plus

    ####################################################################################################################
    @property
    def equals(self):
        return self.equal

    ####################################################################################################################
    @property
    def equal_sign(self):
        return self.equal

    ####################################################################################################################
    @property
    def period(self):
        return self.dot

    ####################################################################################################################
    @property
    def decimal_point(self):
        return self.dot
