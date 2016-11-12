# import rex_utils
# from rexpression import Rexpression, RexTuple
#
#
# ########################################################################################################################
# class RexWriter(object):
#
#     ####################################################################################################################
#     def __init__(self, text=None):
#         self._expression = list()
#         self.text = text
#
#     ####################################################################################################################
#     def expression(self):
#         rexpression = Rexpression(self, text=self.text)
#         return rexpression.expression()
#
#     ####################################################################################################################
#     def add_rex_tuple(self, name, value, is_opener=False, closers=None, condition=None, side_effect=None):
#         r = RexTuple(name=name, value=value, is_opener=is_opener, closers=closers, condition=condition,
#                      side_effect=side_effect, index=len(self._expression))
#         self._expression.append(r)
#
#     ####################################################################################################################
#     def closers(self, closer):
#         raise NotImplementedError("Need to figure out how to do closers")
#
#     ####################################################################################################################
#     @property
#     def group(self):
#         self.add_rex_tuple("group", "(", is_opener=True, closer=self.closers(self.end_group))
#         return self
#
#     ####################################################################################################################
#     @property
#     def end_group(self):
#         self.add_rex_tuple("end_group", ")")
#         return self
#
#     ####################################################################################################################
#     def set_digits_exact_to_true(self):
#         self._digits_exact = True
#
#     ####################################################################################################################
#     @property
#     def exactly(self):
#         self.add_rex_tuple(name="exactly",
#                            value="{",
#                            is_opener=True,
#                            closers=[],
#                            side_effect=None)
#         return self
#
#     ####################################################################################################################
#     def exactly_closer(self):
#         def condition(element):
#             rex_utils.is_not_digit(element.value)
#             pass
#
#         self.add_rex_tuple(name="exactly_closer",
#                            value=",}",
#                            is_opener=False,
#                            closers=None,
#                            condition=condition,
#                            side_effect=None)
#
#     ####################################################################################################################
#     @property
#     def digits_with_exact_length(self):
#         self.add_rex_tuple(name="digits_with_exact_length",
#                            value="\d{",
#                            is_opener=True,
#                            closers=self.digits_with_exact_length_closer,
#                            side_effect=self.set_digits_exact_to_true,
#                            # close_condition=self.end_exact_range)
#                            )
#         return self
#
#     ####################################################################################################################
#     def end_exact_range(self, char, element):
#         # if next char is not a digit and is not the open curly brace
#         # or if the element is the last one in the expression
#         # return True, otherwise, return False
#         is_digit = self.is_digit(char)
#         is_last_element = element == self.last()
#         if any([
#             not is_digit,
#             is_last_element,
#
#         ]):
#         # self.add_rex_tuple("end_exact_range", ",}")
#             self._digits_exact = False
#         return self
#
#     ####################################################################################################################
#     @property
#     def numbers(self):
#         self.add_rex_tuple("numbers", "{{", is_opener=True)
#         return self
#
#     ####################################################################################################################
#     def phone_number_pattern(self, dashes=False, parenthesis=None, dots=None):
#         if dashes:
#             return self.write.group \
#                 .digits_with_exact_length._3 \
#                 .dash.digits_with_exact_length._3 \
#                 .dash.digits_with_exact_length._4 \
#                 .end_group
#         elif dots:
#             return self.write.group \
#                 .digits_with_exact_length._3 \
#                 .dot.digits_with_exact_length._3 \
#                 .dot.digits_with_exact_length._4 \
#                 .end_group
#         elif parenthesis:
#             return self.write.group \
#                 .open_parenthesis.digits_with_exact_length._3.close_parenthesis \
#                 .single_space.digits_with_exact_length._3 \
#                 .dash.digits_with_exact_length._4 \
#                 .end_group
#
#
# # ########################################################################################################################
# # class RexWriter(object):
# #
# #     ####################################################################################################################
# #     @property
# #     def write(self):
# #         rex = ReWriterExpression()
# #         return rex
# #
# #     ####################################################################################################################
# #     @staticmethod
# #     def read(text):
# #         rex = ReWriterExpression(text=text)
# #         return rex
# #
# #
# ########################################################################################################################
# Rex = RexWriter()
