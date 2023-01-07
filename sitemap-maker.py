# import os.path
# from django.core.management.base import BaseCommand, CommandError
# from django.contrib.sitemaps import GenericSitemap
# from django.contrib.sites.models import Site
# from django.template import loader
# from django.utils.encoding import smart_str

# from myproject.models import MyModel


# class Command(BaseCommand):
# help = """Generates the sitemaps for the site, pass in a output directory
# """

#     def handle(self, *args, **options):
#     if len(args) != 1:
#         raise CommandError('You need to specify a output directory')
#     directory = args[0]
#     if not os.path.isdir(directory):
#         raise CommandError('directory %s does not exist' % directory)
#     #modify to meet your needs
#     sitemap = GenericSitemap({'queryset': MyModel.objects.order_by('id'), 'date_field':'modified' })
#     current_site = Site.objects.get_current()

#     index_files = []
#     paginator = sitemap.paginator

#     for page_num in range(1, paginator.num_pages+1):
#         filename = 'sitemap_%s.xml' % page_num
#         file_path = os.path.join(directory,filename)
#         index_files.append("http://%s/%s" % (current_site.domain, filename))
#         print "Generating sitemap %s" % file_path
#         with open(file_path, 'w') as site_mapfile:
#             site_mapfile.write(smart_str(loader.render_to_string('sitemap.xml', {'urlset': sitemap.get_urls(page_num)})))
#     sitemap_index = os.path.join(directory,'sitemap_index.xml')
#     with open(sitemap_index, 'w') as site_index:
#         print "Generating sitemap_index.xml %s" % sitemap_index
#             site_index.write(loader.render_to_string('sitemap_index.xml', {'sitemaps': index_files}))