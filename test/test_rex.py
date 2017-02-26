import re
import unittest

from models import Rex


########################################################################################################################
class RexAssertions(unittest.TestCase):

    ####################################################################################################################
    def assert_groups(self, text, rex, re_compiled, expected_groups):
        re_groups = re.search(re_compiled, text).groups()
        self.assertEqual(expected_groups, re_groups)

        print("Rex expression: ", rex.expression())
        rex_groups = re.search(rex.compile(), text).groups()
        self.assertEqual(expected_groups, rex_groups)


########################################################################################################################
class TestRexGroup(RexAssertions):

    ####################################################################################################################
    def test_plain_text(self):
        rex = Rex().group.a.b.c.end_group
        self.assert_groups("abc", rex, re.compile("(abc)"), expected_groups=("abc", ))

    ####################################################################################################################
    def test_single_group_in_parenthesis(self):
        rex = Rex().group.open_parenthesis.a.b.c.close_parenthesis.end_group
        re_compiled = re.compile("(\(abc\))")
        expected_groups = ("(abc)", )

        self.assert_groups("(abc)", rex, re_compiled, expected_groups)
        self.assert_groups("blah(abc)blah", rex, re_compiled, expected_groups)
        self.assert_groups("((blah)(abc)(blah))", rex, re_compiled, expected_groups)

    ####################################################################################################################
    def test_multiple_groups_in_parenthesis(self):
        rex = (Rex().group.open_parenthesis.a.b.c.close_parenthesis.end_group
               .any_character.optional
               .group.open_parenthesis.e.f.g.close_parenthesis.end_group)
        re_compiled = re.compile("(\(abc\)).*?(\(efg\))")
        expected_groups = ("(abc)", "(efg)")

        self.assert_groups("(abc)(efg)", rex, re_compiled, expected_groups)
        self.assert_groups("blah(abc)blah(efg)", rex, re_compiled, expected_groups)
        self.assert_groups("((blah)(abc)(bl(efg)ah))", rex, re_compiled, expected_groups)


########################################################################################################################
class TestRex(RexAssertions):

    ####################################################################################################################
    def assert_expression(self, text, rex, re_compiled):
        self.assertTrue(re.search(re_compiled, text))
        self.assertTrue(re.search(rex.compile(), text))

    ####################################################################################################################
    def test_write(self):
        blah = Rex().b.l.a.h
        self.assert_expression("blergblahb loasdf", blah, re.compile("blah"))

        # since each property returns 'self', calling more will
        # append more characters to _expression/expression()
        blahbloop = blah.b.l.o.o.p
        self.assert_expression("blergblahbloop loasdf", blahbloop, re.compile("blahbloop"))

        carlos = Rex().C.a.r.l.o.s
        self.assert_expression("blergblahbloop loasdf", blahbloop, re.compile("blahbloop"))
        self.assert_expression("blerCarlosp loasdf", carlos, re.compile("Carlos"))

        # blah and blahbloop should be the same object
        self.assertEqual(blah, blahbloop)
        self.assertNotEqual(blah, carlos)

        # Since 'carlos' was instantiated with the 'write' property
        # it should be a distinct object from the others
        self.assertNotEqual(blahbloop, carlos)

    ####################################################################################################################
    def test_datetimes(self):
        re_compiled = re.compile("10-22-2016 7:51 am")
        rex = (Rex()._1._0.dash._2._2.dash._2._0._1._6
               .single_space
               ._7.colon._5._1.single_space.a.m)
        self.assert_expression("The date is 10-22-2016 7:51 am right now.", rex, re_compiled)

    ####################################################################################################################
    def test_5_digit_zip_code(self):
        self.assert_expression("blah73139 blah", Rex()._5.digits, re.compile("\d{5}"))

    ####################################################################################################################
    def test_phone_number_pattern__with_dashes(self):
        self.assert_groups(text="blah405-867-5309 blah 723",
                           rex=Rex().group._3.digits.dash._3.digits.dash._4.digits.end_group,
                           re_compiled=re.compile(r"(\d{3}-\d{3}-\d{4})"),
                           expected_groups=("405-867-5309",))

    ####################################################################################################################
    def test_phone_number_pattern__with_dots(self):
        self.assert_groups(text="blah405.867.5309 blah 723",
                           rex=(Rex().group
                                ._3.digits.dot._3.digits.dot._4.digits
                                .end_group),
                           re_compiled=re.compile("(\d{3}\.\d{3}\.\d{4})"),
                           expected_groups=("405.867.5309",))

    ####################################################################################################################
    def test_phone_number_pattern__with_parenthesis(self):
        self.assert_groups(text="blah(405) 867-5309 blah 723",
                           rex=(Rex().group
                                .open_parenthesis._3.digits.close_parenthesis
                                .single_space._3.digits.dash._4.digits
                                .end_group),
                           re_compiled=re.compile("(\(\d{3}\)\s\d{3}-\d{4})"),
                           expected_groups=("(405) 867-5309",))

    ####################################################################################################################
    def test_phone_number_pattern__with_groups(self):
        rex = (Rex().open_parenthesis
               .group._3.digits.end_group
               .close_parenthesis.single_space
               .group._3.digits.end_group
               .dash
               .group._4.digits.end_group)
        re_compiled = re.compile("\((\d{3})\)\s(\d{3})-(\d{4})")
        self.assert_groups(text="Phone number (405) 867-5309.",
                           rex=rex,
                           re_compiled=re_compiled,
                           expected_groups=("405", "867", "5309"))
