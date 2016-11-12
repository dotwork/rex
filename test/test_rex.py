import re
import unittest
from models import Rex


########################################################################################################################
class TestReWrite(unittest.TestCase):

    ####################################################################################################################
    def test_write(self):
        # set an initial value for expression
        blah = "blah"
        rex = Rex.write.b.l.a.h
        self.assertEqual(blah, rex.expression())

        # since each property returns 'self', calling more will
        # append more characters to _expression/expression()
        carlos = "Carlos"
        rex2 = rex.write.C.a.r.l.o.s
        self.assertEqual(blah, rex.expression())
        self.assertEqual(carlos, rex2.expression())

        # if 'write' property is called_expression should be reset to empty string
        # making more calls to properties after that will result in a new expression
        rex3 = rex.write.s.c.a.r
        self.assertEqual(blah, rex.expression())
        self.assertEqual(carlos, rex2.expression())

        # each rex object should be the same
        self.assertNotEquals(rex, rex2, rex3)

    ####################################################################################################################
    def test_5_digit_zip_code(self):
        expected_expression = r"\d{5,}"
        pattern = re.compile(expected_expression)

        zip_code = "73139"
        text_with_zip_code = "blah{} blah".format(zip_code)

        result = re.search(pattern, text_with_zip_code).group()
        self.assertEqual(zip_code, result)

        rex = Rex.write.exactly._5.digits
        expression = rex.expression()
        self.assertEqual(expected_expression, expression)

        result = re.search(rex.compile(), text_with_zip_code).group()
        self.assertEqual(zip_code, result)

    ####################################################################################################################
    def test_phone_number_pattern__with_dashes(self):
        expected_expression = r"(\d{3,}\-\d{3,}\-\d{4,})"
        pattern = re.compile(expected_expression)

        rex = Rex.write.phone_number_pattern(dashes=True)
        expression = rex.expression()
        self.assertEqual(expected_expression, expression)

        phone_number = "405-867-5309"
        text_with_phone_number = "blah{} blah 723".format(phone_number)

        result = re.search(pattern, text_with_phone_number).group()
        self.assertEqual(phone_number, result)

        result = re.search(rex.compile(), text_with_phone_number).group()
        self.assertEqual(phone_number, result)

    ####################################################################################################################
    def test_phone_number_pattern__with_dots(self):
        expected_expression = r"(\d{3,}\.\d{3,}\.\d{4,})"
        pattern = re.compile(expected_expression)

        rex = Rex.write.phone_number_pattern(dots=True)
        self.assertEqual(expected_expression, rex.expression())

        phone_number = "405.867.5309"
        text_with_phone_number = "blah{} blah 723".format(phone_number)

        result = re.search(pattern, text_with_phone_number).group()
        self.assertEqual(phone_number, result)

        result = re.search(rex.compile(), text_with_phone_number).group()
        self.assertEqual(phone_number, result)

    ####################################################################################################################
    def test_phone_number_pattern__with_parenthesis(self):
        phone_number = "(405) 867-5309"
        text_with_phone_number = "blah{} blah 723".format(phone_number)

        expected_expression = r"(\(\d{3,}\)\s\d{3,}\-\d{4,})"
        pattern = re.compile(expected_expression)

        result = re.search(pattern, text_with_phone_number).group()
        self.assertEqual(phone_number, result)

        rex = Rex.write.phone_number_pattern(parenthesis=True)
        self.assertEqual(expected_expression, rex.expression())

        result = re.search(rex.compile(), text_with_phone_number).group()
        self.assertEqual(phone_number, result)

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

    ####################################################################################################################
    def test_(self):
        self.assertEqual(("blah", ), Rex.add_rex_tuple.closer)
