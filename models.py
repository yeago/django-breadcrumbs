from django.db import models

class Crumb(models.Model):
	url = models.CharField(max_length=255,help_text="Can be a url name or a path. Paths must begin with '/'")
	title = models.CharField(max_length=255)
	template_logic = models.TextField(null=True,blank=True,help_text="")
	parent = models.ForeignKey('breadcrumbs.Crumb',null=True,blank=True)
	def __unicode__(self):
		if not self.parent:
			return self.title

		this_crumb = self.parent
		parent_text = "%s" % self.title

		while 1 == 1:
			parent_text = "%s / %s" % (this_crumb.title,parent_text)
			if not this_crumb.parent:
				break

			this_crumb = this_crumb.parent

		return parent_text
