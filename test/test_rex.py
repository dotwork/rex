import re
import unittest
from models import Rex, Node


########################################################################################################################
class TestRex(unittest.TestCase):

    ####################################################################################################################
    def test_write(self):
        # set an initial value for expression
        blah = "blah"
        rex = Rex.write.b.l.a.h
        self.assertEqual(blah, rex.expression())

        # since each property returns 'self', calling more will
        # append more characters to _expression/expression()
        blahbloop = blah + "bloop"
        rex = rex.b.l.o.o.p
        self.assertEqual(blahbloop, rex.expression())

        carlos = "Carlos"
        rex2 = rex.write.C.a.r.l.o.s
        self.assertEqual(blahbloop, rex.expression())
        self.assertEqual(carlos, rex2.expression())

        # if 'write' property is called_expression should be reset to empty string
        # making more calls to properties after that will result in a new expression
        timestamp = re.compile("10-22-2016 7:51 am")
        rex3 = rex.write._1._0.dash._2._2.dash._2._0._1._6.single_space._7.colon._5._1.single_space.a.m
        self.assertEqual(blahbloop, rex.expression())
        self.assertEqual(carlos, rex2.expression())
        self.assertEqual(timestamp, rex3.expression())

        # each rex object should be the same
        self.assertNotEquals(rex, rex2, rex3)

    ####################################################################################################################
    def test_5_digit_zip_code(self):
        expected_expression = r"\d{5}"
        pattern = re.compile(expected_expression)

        zip_code = "73139"
        text_with_zip_code = "blah{} blah".format(zip_code)

        result = re.search(pattern, text_with_zip_code).group()
        self.assertEqual(zip_code, result)

        # 5 digits
        rex = Rex.write._5.digits
        expression = rex.expression()
        self.assertEqual(expected_expression, expression)

        result = re.search(rex.compile(), text_with_zip_code).group()
        self.assertEqual(zip_code, result)

    ####################################################################################################################
    def assert_expression(self, text, value, rex, re_compiled):
        result = re.search(re_compiled, text).groups()
        self.assertEqual(value, result)

        rex_result = re.search(rex.compile(), text).groups()
        self.assertEqual(value, rex_result)

    ####################################################################################################################
    def test_phone_number_pattern__with_dashes(self):
        rex = Rex.write.group._3.digits.dash._3.digits.dash._4.digits.end_group
        self.assert_expression(text="blah405-867-5309 blah 723", value=("405-867-5309", ),
                               rex=rex, re_compiled=re.compile(r"(\d{3}-\d{3}-\d{4})"))

    ####################################################################################################################
    def test_phone_number_pattern__with_dots(self):
        rex = Rex.write.group._3.digits.dot._3.digits.dot._4.digits.end_group
        self.assert_expression(text="blah405.867.5309 blah 723", value=("405.867.5309", ),
                               rex=rex, re_compiled=re.compile("(\d{3}\.\d{3}\.\d{4})"))

    ####################################################################################################################
    def test_phone_number_pattern__with_parenthesis(self):
        rex = Rex.write.group.open_parenthesis._3.digits.close_parenthesis.\
            single_space._3.digits.dash._4.digits.end_group
        self.assert_expression(text="blah(405) 867-5309 blah 723", value=("(405) 867-5309", ),
                               rex=rex, re_compiled=re.compile("(\(\d{3}\)\s\d{3}-\d{4})"))

    ####################################################################################################################
    def test_phone_number_pattern__extract_digits(self):
        phone_number = "(405) 867-5309"
        text_with_phone_number = "blah{} blah 723".format(phone_number)

        expected_expression = r"\((\d{3,})\)\s(\d{3,})\-(\d{4,})"
        pattern = re.compile(expected_expression)

        match = re.search(pattern, text_with_phone_number)
        self.assertEqual(phone_number, match.group())
        self.assertEqual("405", match.group(1))
        self.assertEqual("867", match.group(2))
        self.assertEqual("5309", match.group(3))

        rex = Rex.read(phone_number).write \
            .open_parenthesis.group.digits_with_exact_length._3.end_group.close_parenthesis \
            .single_space.group.digits_with_exact_length._3.end_group \
            .dash.group.digits_with_exact_length._4.end_group

        match = re.search(rex.compile(), text_with_phone_number)
        self.assertEqual(phone_number, match.group())
        self.assertEqual("405", match.group(1))
        self.assertEqual("867", match.group(2))
        self.assertEqual("5309", match.group(3))

        self.assertEqual(phone_number, rex.first_match(0))
        self.assertEqual("405", rex.first_match(1))
        self.assertEqual("867", rex.first_match(2))
        self.assertEqual("5309", rex.first_match(3))

    ####################################################################################################################
    def test_phone_(self):
        expected_expression = r"(\d{3,}\-\d{3,}\-\d{4,})"
        pattern = re.compile(expected_expression)

        rex = Rex.write.group\
            .exactly._3.digits\
            .dash.exactly._3.digits\
            .dash.exactly._4.digits\
            .end_group

        expression = rex.expression()
        self.assertEqual(expected_expression, expression)
