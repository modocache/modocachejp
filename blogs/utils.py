import re
import markdown

from django.template.loader import get_template
from django.template import Context


IMAGE_LINK_REGEX = re.compile('\[!\[(?P<alt_text>.*?)\]\((?P<img_src>.+?)\)\]\((?P<img_link>.+?)\)')


def convert_markdown(text):
    """Add custom CSS styles to linked images in Markdown."""
    matches = re.finditer(IMAGE_LINK_REGEX, text)
    for match in matches:
        print "alt == ", match.group("alt_text")
        replace_tpl = get_template('blogs/rendered/image_link.html')
        context = Context(match.groupdict())
        replacement = replace_tpl.render(context)

        orig = '[![{0}]({1})]({2})'.format(
            match.group('alt_text'),
            match.group('img_src'),
            match.group('img_link'),
        )
        text = text.replace(orig, replacement)

    return markdown.markdown(text, ['codehilite(force_linenos=True)'])

