from django import template
from django.template import Template
from django.core.urlresolvers import resolve

from breadcrumbs.models import Crumb

from breadcrumbs.resolve_to_name_snippet import resolve_to_name

register = template.Library()

class CrumbNode(template.Node):
	def render(self, context):
		request = context['request']
		crumb = None
		try:
			url = resolve_to_name(request.path)
			crumb = Crumb.objects.get(url=url)
		except Crumb.DoesNotExist:
			try:
				crumb = Crumb.objects.get(url=request.path)
			except Crumb.DoesNotExist:
				pass


		if crumb:
			breadcrumb_string = "%s" % crumb.template_logic
			if crumb.parent:
				this_crumb = crumb.parent
				max = 2
				tries = 0
				while tries <= max:
					breadcrumb_string = "%s / %s" % (this_crumb.template_logic,breadcrumb_string)
					if not this_crumb.parent:
						break

					this_crumb = this_crumb.parent
					tries += 1

			breadcrumb_template = Template(breadcrumb_string)

			context['breadcrumbs'] = breadcrumb_template.render(context)
		return '' 
	
@register.tag()
def breadcrumb_populate(parser,token):
	return CrumbNode()
