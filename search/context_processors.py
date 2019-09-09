from search.models import DataSource

def datasouce_pages(request):
    return {
        ds.slug: ds for ds in DataSource.objects.all()
    }

