#!/usr/bin/env python


from docutils.writers import html4css1
from docutils import nodes
from docutils.core import publish_parts

class MyHTMLWriter(html4css1.Writer):
    """
    This docutils writer will use the MyHTMLTranslator class below.

    """
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = MyHTMLTranslator

class MyHTMLTranslator(html4css1.HTMLTranslator):
    """
    This is a translator class for the docutils system.
    It will produce a minimal set of html output.
    (No extry divs, classes oder ids.)

    """

    def visit_block_quote(self, node):
        self.body.append(self.starttag(node, 'blockquote'))

    def depart_block_quote(self, node):
        self.body.append('</blockquote>\n')

    def visit_paragraph(self, node):
        if self.should_be_compact_paragraph(node):
            self.context.append('')
        else:
            self.body.append(self.starttag(node, 'p', ''))
            self.context.append('</p>\n')

    def depart_paragraph(self, node):
        self.body.append(self.context.pop())
    # add this to the imports: from docutils import nodes

    def should_be_compact_paragraph(self, node):
        if(isinstance(node.parent, nodes.block_quote)):
            return 0
        return html4css1.HTMLTranslator.should_be_compact_paragraph(self, node)

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1


def publish(value):
    parts = publish_parts(source=value, writer=MyHTMLWriter())
    return parts['fragment']

# vim: et sw=4 sts=4
