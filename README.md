# rex
WARNING: This library is not production-ready and should only be used for practice and exploration.

Provides a class 'Rex' for describing regular expression patterns in normal english. This is a pet-project that I hope to develop into a reliable tool over time. In the future, I aim to add some powerful debugging features to introspect the Rex expression and notify the developer of bugs in the expression. Ultimately, I intend for this library to allow new programmers to use regular expressions in their projects and educate them on what they are and how they work. Contributions are most welcome.

Here is a brief example of how Rex can be used to describe a regular expression pattern.

        rex = Rex().group.open_parenthesis.a.b.c.close_parenthesis.end_group
        rex.compile()

This produces the same results as:

        re_compiled = re.compile("(\(abc\))")

See the `test_rex.py` file for more examples.
