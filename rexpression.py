# import re
# from collections import namedtuple
#
#
# ########################################################################################################################
# RexTuple = namedtuple("RexTuple", "name value is_opener closers condition side_effect index")
#
#
# ########################################################################################################################
# class Rexpression(object):
#
#     ####################################################################################################################
#     def __init__(self, rex, text=None):
#         self.rex = rex
#         self._digits_exact = False
#         self._last_expression = None
#         self._re = None
#         self.text = text
#         self._last_matched_expression = None
#         self._last_match = None
#         # self.closers = []
#         #
#         # self.digits_with_exact_length_closer = RexTuple(name="end_exact_range", value=",}", is_opener=False, closer=None, side_effect=None)
#         # self.group_closers = [
#         #     RexTuple(name="end_group", value=")", is_opener=False, closer=None, side_effect=None),
#         # ]
#         # self.exactly_closers = [
#         #     RexTuple(name="digits", value="\d", is_opener=False, closer=None, side_effect=None),
#         #     RexTuple(name="letters", value="[a-zA-Z]", is_opener=False, closer=None, side_effect=None)
#         # ]
#
#     ####################################################################################################################
#     @property
#     def re(self):
#         if self._re is None:
#             self._re = re
#         return self._re
#
#     ####################################################################################################################
#     def check_for_start_or_end_chars(self, element):
#         start_end_char_map = {
#             "(": ")",
#             "{": "}",
#             "[": "]",
#         }
#         start_chars = []
#         for start, end in start_end_char_map.items():
#             if start == element.value:
#                 start_chars.append(element.value)
#                 return
#
#             elif end == element.value:
#                 if element.value == start_end_char_map[start_chars[-1]]:
#                     start_chars.pop()
#                     return
#                 else:
#                     msg = "Got '{actual}'. Expected '{expected}'."
#                     expected_name = start_end_char_map[start_chars[-1]]
#                     msg = msg.format(actual=element.name, expected=expected_name)
#                     raise TypeError(msg)
#
#     ####################################################################################################################
#     def handle_opening_element(self, element):
#         self.closers.append(element.closers)
#         if element.side_effect:
#             element.side_effect()
#
#     ####################################################################################################################
#     def handle_closing_element(self, element):
#         self.closers.pop()
#         if element.side_effect:
#             element.side_effect()
#
#     ####################################################################################################################
#     def expression(self):
#         self.closers = []
#         expression = r""
#         for element in self.rex._expression:
#             if element.is_opener:
#                 self.handle_opening_element(element)
#
#             elif self.closers:
#                 if element == self.closers[-1] or self.closers[0].condition(element):
#                     self.handle_closing_element(element)
#
#             expression = r"{}{}".format(expression, element.value)
#
#             # raise Exception("This is failing because nothing is checking if _digits_exact is True"
#             #                 "and then closing the bracket if it is.")
#
#             # if element.name == "digits_with_exact_length":
#             #     self._digits_exact = True
#             #     expression = r"{}{}".format(expression, element.value)
#             #     continue
#             #
#             # self.check_for_start_or_end_chars(element)
#             #
#             # if self._digits_exact and \
#             #         (self.ends_with_digits(expression) is False or element == self.last()):
#             #     expression += element.value + r",}"
#             #     self._digits_exact = False
#             # else:
#             #     expression = r"{}{}".format(expression, element.value)
#
#         return expression
#
#     ####################################################################################################################
#     def first_match(self, num=None):
#         if all([self._last_match is not None,
#                 self._last_matched_expression is not None,
#                 self._last_matched_expression == self._expression]):
#             match = self._last_match
#         else:
#             self._last_match = re.search(self.compile(), self.text)
#             self._last_matched_expression = self._expression
#             match = self._last_match
#
#         if num is None:
#             return match
#         else:
#             return match.group(num)
#
#     ####################################################################################################################
#     @staticmethod
#     def is_digit(char):
#         try:
#             int(char)
#             return True
#         except ValueError:
#             return False
#
#     ####################################################################################################################
#     def ends_with_digits(self, expression=None):
#         expression = expression or self.rex._expression[-1].value
#         last = expression[-1]
#         return self.is_digit(last)
#
#     ####################################################################################################################
#     def compile(self):
#         return re.compile(self.expression())
#
#     ####################################################################################################################
#     def last(self):
#         return self.rex._expression[-1]
#
#     ####################################################################################################################
#     def ends_with_open_curly_brace(self):
#         return self.last().value == "{"
#
#     ####################################################################################################################
#     def in_number_range(self):
#         return self.ends_with_digits() or self.ends_with_open_curly_brace()
#
#     ####################################################################################################################
#     def set_digits_exact_to_true(self):
#         self._digits_exact = True
#
#     ####################################################################################################################
#     def insert_digits_symbol(self, expression):
#         return "{expression}{digits}".format(expression=expression, digits="\d")
