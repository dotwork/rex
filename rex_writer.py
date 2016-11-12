import rex_utils
from rexpression import Rexpression, RexTuple


########################################################################################################################
class RexWriter(object):

    ####################################################################################################################
    def __init__(self, text=None):
        self._expression = list()
        self.text = text

    ####################################################################################################################
    @property
    def write(self):
        self._expression = []
        return self

    ####################################################################################################################
    def expression(self):
        rexpression = Rexpression(self, text=self.text)
        return rexpression.expression()

    ####################################################################################################################
    def add_rex_tuple(self, name, value, is_opener=False, closers=None, condition=None, side_effect=None):
        r = RexTuple(name=name, value=value, is_opener=is_opener, closers=closers, condition=condition,
                     side_effect=side_effect, index=len(self._expression))
        self._expression.append(r)

    ####################################################################################################################
    def closers(self, closer):
        raise NotImplementedError("Need to figure out how to do closers")

    ####################################################################################################################
    @property
    def group(self):
        self.add_rex_tuple("group", "(", is_opener=True, closer=self.closers(self.end_group))
        return self

    ####################################################################################################################
    @property
    def end_group(self):
        self.add_rex_tuple("end_group", ")")
        return self

    ####################################################################################################################
    @property
    def start(self):
        failure_message = "Cannot add 'start' to an existing expression. Current expression: {}"
        assert self.expression() == r"", failure_message.format(self.expression())
        self.add_rex_tuple("start", "^")
        return self

    ####################################################################################################################
    @property
    def end(self):
        self.add_rex_tuple("end", "$")
        return self

    ####################################################################################################################
    def set_digits_exact_to_true(self):
        self._digits_exact = True

    ####################################################################################################################
    @property
    def exactly(self):
        self.add_rex_tuple(name="exactly",
                           value="{",
                           is_opener=True,
                           closers=[],
                           side_effect=None)
        return self

    ####################################################################################################################
    def exactly_closer(self):
        def condition(element):
            rex_utils.is_not_digit(element.value)
            pass

        self.add_rex_tuple(name="exactly_closer",
                           value=",}",
                           is_opener=False,
                           closers=None,
                           condition=condition,
                           side_effect=None)

    ####################################################################################################################
    @property
    def digits(self):
        self.add_rex_tuple(name="digits",
                           value="\d",
                           is_opener=False,
                           closers=None,
                           side_effect=None)
        return self

    ####################################################################################################################
    @property
    def digits_with_exact_length(self):
        self.add_rex_tuple(name="digits_with_exact_length",
                           value="\d{",
                           is_opener=True,
                           closers=self.digits_with_exact_length_closer,
                           side_effect=self.set_digits_exact_to_true,
                           # close_condition=self.end_exact_range)
                           )
        return self

    ####################################################################################################################
    def end_exact_range(self, char, element):
        # if next char is not a digit and is not the open curly brace
        # or if the element is the last one in the expression
        # return True, otherwise, return False
        is_digit = self.is_digit(char)
        is_last_element = element == self.last()
        if any([
            not is_digit,
            is_last_element,

        ]):
        # self.add_rex_tuple("end_exact_range", ",}")
            self._digits_exact = False
        return self

    ####################################################################################################################
    @property
    def zero_or_more_numbers(self):
        self.add_rex_tuple("zero_or_more_numbers", "\d*")
        return self

    ####################################################################################################################
    @property
    def one_or_more_numbers(self):
        self.add_rex_tuple("one_or_more_numbers", "\d+")
        return self

    ####################################################################################################################
    @property
    def numbers(self):
        self.add_rex_tuple("numbers", "{{", is_opener=True)
        return self

    ####################################################################################################################
    @property
    def thru(self):
        self.add_rex_tuple("thru", "\-")
        return self

    ####################################################################################################################
    @property
    def backtick(self):
        self.add_rex_tuple("backtick", "`")
        return self

    ####################################################################################################################
    @property
    def tilde(self):
        self.add_rex_tuple("tilde", "~")
        return self

    ####################################################################################################################
    @property
    def exclamation_point(self):
        self.add_rex_tuple("exclamation_point", "!")
        return self

    ####################################################################################################################
    @property
    def at(self):
        self.add_rex_tuple("at", "@")
        return self

    ####################################################################################################################
    @property
    def hash(self):
        self.add_rex_tuple("hash", "#")
        return self

    ####################################################################################################################
    @property
    def dollar(self):
        self.add_rex_tuple("dollar", "\$")
        return self

    ####################################################################################################################
    @property
    def percent(self):
        self.add_rex_tuple("percent", "%")
        return self

    ####################################################################################################################
    @property
    def caret(self):
        self.add_rex_tuple("caret", "\^")
        return self

    ####################################################################################################################
    @property
    def ampersand(self):
        self.add_rex_tuple("ampersand", "&")
        return self

    ####################################################################################################################
    @property
    def asterisk(self):
        self.add_rex_tuple("asterisk", "\*")
        return self

    ####################################################################################################################
    @property
    def dash(self):
        self.add_rex_tuple("dash", "\-")
        return self

    ####################################################################################################################
    @property
    def underscore(self):
        self.add_rex_tuple("underscore", "_")
        return self

    ####################################################################################################################
    @property
    def plus(self):
        self.add_rex_tuple("plus", "\+")
        return self

    ####################################################################################################################
    @property
    def equal(self):
        self.add_rex_tuple("equal", "=")
        return self

    ####################################################################################################################
    @property
    def dot(self):
        self.add_rex_tuple("dot", "\.")
        return self

    ####################################################################################################################
    @property
    def backslash(self):
        self.add_rex_tuple("backslash", "\\")
        return self

    ####################################################################################################################
    @property
    def forwardslash(self):
        self.add_rex_tuple("forwardslash", "\/")
        return self

    ####################################################################################################################
    @property
    def open_bracket(self):
        self.add_rex_tuple("open_bracket", "\[")
        return self

    ####################################################################################################################
    @property
    def close_bracket(self):
        self.add_rex_tuple("close_bracket", "\]")
        return self

    ####################################################################################################################
    @property
    def pipe(self):
        self.add_rex_tuple("pipe", "\|")
        return self

    ####################################################################################################################
    @property
    def open_parenthesis(self):
        self.add_rex_tuple("open_parenthesis", "\(")
        return self

    ####################################################################################################################
    @property
    def close_parenthesis(self):
        self.add_rex_tuple("close_parenthesis", "\)")
        return self

    ####################################################################################################################
    @property
    def single_space(self):
        self.add_rex_tuple("single_space", "\s")
        return self

    ####################################################################################################################
    @property
    def question_mark(self):
        self.add_rex_tuple("question_mark", "\?")
        return self

    ####################################################################################################################
    @property
    def a(self):
        self.add_rex_tuple("a", "a")
        return self

    ####################################################################################################################
    @property
    def b(self):
        self.add_rex_tuple("b", "b")
        return self

    ####################################################################################################################
    @property
    def c(self):
        self.add_rex_tuple("c", "c")
        return self

    ####################################################################################################################
    @property
    def d(self):
        self.add_rex_tuple("d", "d")
        return self

    ####################################################################################################################
    @property
    def e(self):
        self.add_rex_tuple("e", "e")
        return self

    ####################################################################################################################
    @property
    def f(self):
        self.add_rex_tuple("f", "f")
        return self

    ####################################################################################################################
    @property
    def g(self):
        self.add_rex_tuple("g", "g")
        return self

    ####################################################################################################################
    @property
    def h(self):
        self.add_rex_tuple("h", "h")
        return self

    ####################################################################################################################
    @property
    def i(self):
        self.add_rex_tuple("i", "i")
        return self

    ####################################################################################################################
    @property
    def j(self):
        self.add_rex_tuple("j", "j")
        return self

    ####################################################################################################################
    @property
    def k(self):
        self.add_rex_tuple("k", "k")
        return self

    ####################################################################################################################
    @property
    def l(self):
        self.add_rex_tuple("l", "l")
        return self

    ####################################################################################################################
    @property
    def m(self):
        self.add_rex_tuple("m", "m")
        return self

    ####################################################################################################################
    @property
    def n(self):
        self.add_rex_tuple("n", "n")
        return self

    ####################################################################################################################
    @property
    def o(self):
        self.add_rex_tuple("o", "o")
        return self

    ####################################################################################################################
    @property
    def p(self):
        self.add_rex_tuple("p", "p")
        return self

    ####################################################################################################################
    @property
    def q(self):
        self.add_rex_tuple("q", "q")
        return self

    ####################################################################################################################
    @property
    def r(self):
        self.add_rex_tuple("r", "r")
        return self

    ####################################################################################################################
    @property
    def s(self):
        self.add_rex_tuple("s", "s")
        return self

    ####################################################################################################################
    @property
    def t(self):
        self.add_rex_tuple("t", "t")
        return self

    ####################################################################################################################
    @property
    def u(self):
        self.add_rex_tuple("u", "u")
        return self

    ####################################################################################################################
    @property
    def v(self):
        self.add_rex_tuple("v", "v")
        return self

    ####################################################################################################################
    @property
    def w(self):
        self.add_rex_tuple("w", "w")
        return self

    ####################################################################################################################
    @property
    def x(self):
        self.add_rex_tuple("x", "x")
        return self

    ####################################################################################################################
    @property
    def y(self):
        self.add_rex_tuple("y", "y")
        return self

    ####################################################################################################################
    @property
    def z(self):
        self.add_rex_tuple("z", "z")
        return self

    ####################################################################################################################
    @property
    def A(self):
        self.add_rex_tuple("A", "A")
        return self

    ####################################################################################################################
    @property
    def B(self):
        self.add_rex_tuple("B", "B")
        return self

    ####################################################################################################################
    @property
    def C(self):
        self.add_rex_tuple("C", "C")
        return self

    ####################################################################################################################
    @property
    def D(self):
        self.add_rex_tuple("D", "D")
        return self

    ####################################################################################################################
    @property
    def E(self):
        self.add_rex_tuple("E", "E")
        return self

    ####################################################################################################################
    @property
    def F(self):
        self.add_rex_tuple("F", "F")
        return self

    ####################################################################################################################
    @property
    def G(self):
        self.add_rex_tuple("G", "G")
        return self

    ####################################################################################################################
    @property
    def H(self):
        self.add_rex_tuple("H", "H")
        return self

    ####################################################################################################################
    @property
    def I(self):
        self.add_rex_tuple("I", "I")
        return self

    ####################################################################################################################
    @property
    def J(self):
        self.add_rex_tuple("J", "J")
        return self

    ####################################################################################################################
    @property
    def K(self):
        self.add_rex_tuple("K", "K")
        return self

    ####################################################################################################################
    @property
    def L(self):
        self.add_rex_tuple("L", "L")
        return self

    ####################################################################################################################
    @property
    def M(self):
        self.add_rex_tuple("M", "M")
        return self

    ####################################################################################################################
    @property
    def N(self):
        self.add_rex_tuple("N", "N")
        return self

    ####################################################################################################################
    @property
    def O(self):
        self.add_rex_tuple("O", "O")
        return self

    ####################################################################################################################
    @property
    def P(self):
        self.add_rex_tuple("P", "P")
        return self

    ####################################################################################################################
    @property
    def Q(self):
        self.add_rex_tuple("Q", "Q")
        return self

    ####################################################################################################################
    @property
    def R(self):
        self.add_rex_tuple("R", "R")
        return self

    ####################################################################################################################
    @property
    def S(self):
        self.add_rex_tuple("S", "S")
        return self

    ####################################################################################################################
    @property
    def T(self):
        self.add_rex_tuple("T", "T")
        return self

    ####################################################################################################################
    @property
    def U(self):
        self.add_rex_tuple("U", "U")
        return self

    ####################################################################################################################
    @property
    def V(self):
        self.add_rex_tuple("V", "V")
        return self

    ####################################################################################################################
    @property
    def W(self):
        self.add_rex_tuple("W", "W")
        return self

    ####################################################################################################################
    @property
    def X(self):
        self.add_rex_tuple("X", "X")
        return self

    ####################################################################################################################
    @property
    def Y(self):
        self.add_rex_tuple("Y", "Y")
        return self

    ####################################################################################################################
    @property
    def Z(self):
        self.add_rex_tuple("Z", "Z")
        return self

    ####################################################################################################################
    @property
    def _0(self):
        self.add_rex_tuple("_0", "0")
        return self

    ####################################################################################################################
    @property
    def _1(self):
        self.add_rex_tuple("_1", "1")
        return self

    ####################################################################################################################
    @property
    def _2(self):
        self.add_rex_tuple("_2", "2")
        return self

    ####################################################################################################################
    @property
    def _3(self):
        self.add_rex_tuple("_3", "3")
        return self

    ####################################################################################################################
    @property
    def _4(self):
        self.add_rex_tuple("_4", "4")
        return self

    ####################################################################################################################
    @property
    def _5(self):
        self.add_rex_tuple("_5", "5")
        return self

    ####################################################################################################################
    @property
    def _6(self):
        self.add_rex_tuple("_6", "6")
        return self

    ####################################################################################################################
    @property
    def _7(self):
        self.add_rex_tuple("_7", "7")
        return self

    ####################################################################################################################
    @property
    def _8(self):
        self.add_rex_tuple("_8", "8")
        return self

    ####################################################################################################################
    @property
    def _9(self):
        self.add_rex_tuple("_9", "9")
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

    ####################################################################################################################
    def phone_number_pattern(self, dashes=False, parenthesis=None, dots=None):
        if dashes:
            return self.write.group \
                .digits_with_exact_length._3 \
                .dash.digits_with_exact_length._3 \
                .dash.digits_with_exact_length._4 \
                .end_group
        elif dots:
            return self.write.group \
                .digits_with_exact_length._3 \
                .dot.digits_with_exact_length._3 \
                .dot.digits_with_exact_length._4 \
                .end_group
        elif parenthesis:
            return self.write.group \
                .open_parenthesis.digits_with_exact_length._3.close_parenthesis \
                .single_space.digits_with_exact_length._3 \
                .dash.digits_with_exact_length._4 \
                .end_group


# ########################################################################################################################
# class RexWriter(object):
#
#     ####################################################################################################################
#     @property
#     def write(self):
#         rex = ReWriterExpression()
#         return rex
#
#     ####################################################################################################################
#     @staticmethod
#     def read(text):
#         rex = ReWriterExpression(text=text)
#         return rex
#
#
########################################################################################################################
Rex = RexWriter()
