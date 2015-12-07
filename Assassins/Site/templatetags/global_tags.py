import re

from django import template
from django.core.urlresolvers import reverse
from django.template.base import TextNode
from django.template import Node, TemplateSyntaxError
from django.template import engines
from bs4 import BeautifulSoup

register = template.Library()


# certain tags encounter issues if spaces are added to their contents.
# we clean those up using this replacement method that can strip spaces
# from the contents of any tag.
def make_replacement(html, tag):
	start_tag_pattern = "<{0}([^>]*)>".format(tag)
	end_tag_pattern = "</{0}>".format(tag)
	full_pattern = "{0}([^<]*){1}".format(start_tag_pattern, end_tag_pattern)

	def replacement_callback(match):
		return '<{0}{1}>{2}</{3}>'.format(tag, match.group(1), match.group(2).strip(), tag)

	return re.sub(
		pattern=full_pattern,
		repl=replacement_callback,
		string=html,
		flags=re.DOTALL | re.IGNORECASE
	)


@register.simple_tag(takes_context=True)
def link(context, reverse_string, display):
	uri = reverse(reverse_string)
	current = context.request.get_full_path()
	if current == uri:
		return """
                <li class="active"><a href="{0}">{1}</a></li>
               """.format(uri, display)
	else:
		return """
                <li><a href="{0}">{1}</a></li>
               """.format(uri, display)


class PrettyPrintNode(Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist

	def render(self, context):
		html = BeautifulSoup(self.nodelist.render(context), 'html5lib')
		cleaned = html.prettify(formatter='html')
		cleaned = make_replacement(cleaned, 'textarea')
		cleaned = make_replacement(cleaned, 'a')
		return cleaned


@register.tag()
def pretty(parser, token):
	nodelist = parser.parse(('endpretty',))
	parser.delete_first_token()
	return PrettyPrintNode(nodelist)


@register.filter(name='class')
def add_class(field, css):
	return field.as_widget(attrs={"class": css})


@register.tag()
def include_raw(parser, token):
	bits = token.split_contents()
	if len(bits) != 2:
		raise TemplateSyntaxError(
			"{0} tag takes one argument: the name of the template to be included".format(bits[0]))
	template_name = bits[1]
	if template_name[0] in ('"', "'") and template_name[-1] == template_name[0]:
		template_name = template_name[1:-1]

	from django.template.loaders import filesystem, app_directories

	try:
		source, path = filesystem.Loader(engine=engines['django']).load_template_source(
			template_name)
	except filesystem.TemplateDoesNotExist:
		try:
			source, path = app_directories.Loader(engine=engines['django']).load_template_source(
				template_name)
		except app_directories.TemplateDoesNotExist:
			raise app_directories.TemplateDoesNotExist(
				"The template {0}, could not be found.".format(template_name))
	return TextNode(source)


class CaptureNode(Node):
	def __init__(self, nodelist, varname):
		self.nodelist = nodelist
		self.varname = varname

	def render(self, context):
		output = self.nodelist.render(context)
		context.dicts[0][self.varname] = output
		return ''


@register.tag('capture')
def do_capture(parser, token):
	try:
		tag_name, args = token.contents.split(None, 1)
	except ValueError:
		raise template.TemplateSyntaxError("'capture' node requires a variable name.")
	nodelist = parser.parse(('endcapture',))
	parser.delete_first_token()
	return CaptureNode(nodelist, args)
