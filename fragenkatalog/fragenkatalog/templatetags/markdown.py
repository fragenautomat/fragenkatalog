"""Markdown Package.

To provide dynamic Markdown rendering, we use the Markdown package.

.. _Markdown package:
   https://pypi.python.org/pypi/Markdown

.. _Markdown package extensions
   https://python-markdown.github.io/extensions/
"""

from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from markdown import Markdown
from markdown.extensions.codehilite import CodeHiliteExtension

from django import template

import bleach

"""
Default whitelist of allowed HTML tags. Any other HTML tags will be escaped or
stripped from the text. This applies to the html output that Markdown produces.
"""
ALLOWED_TAGS = [
    'ul',
    'ol',
    'li',
    'p',
    'pre',
    'code',
    'blockquote',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr',
    'br',
    'strong',
    'em',
    'a',
    'img'
]

"""
Default whitelist of attributes. It allows the href and title attributes for <a>
tags and the src, title and alt attributes for <img> tags. Any other attribute
will be stripped from its tag.
"""
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'title', 'alt']
}

"""
Default whitelist of styles is an empty list. If you allow the style attribute,
you will also need to whitelist styles users are allowed to set, for example
color and background-color.
"""
ALLOWED_STYLES = []

"""
If you allow tags that have attributes containing a URI value
(like the href attribute of an anchor tag,) you may want to adapt
the accepted protocols. The default list only allows http, https and mailto.
"""
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


register = template.Library()
convert = Markdown(output_format="html5", extensions=[
    "markdown.extensions.toc",
    "markdown.extensions.smarty",
    "markdown.extensions.fenced_code",
    "markdown.extensions.tables",
    CodeHiliteExtension(use_pygments=False),
]).convert


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(bleach.clean(
        convert(value),
        tags=ALLOWED_TAGS,
        styles=ALLOWED_STYLES,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS
    ))
