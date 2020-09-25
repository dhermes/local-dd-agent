import json
import textwrap

import pygments
import pygments.formatters
import pygments.lexers


def printable_json(value, prefix):
    for_terminal = pygments.highlight(
        json.dumps(value, indent=2),
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalTrueColorFormatter(style="solarized-dark"),
    )
    return textwrap.indent(for_terminal, prefix)
