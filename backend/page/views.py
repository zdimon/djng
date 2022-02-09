from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from page.forms import StaticPageForm
from page.models import StaticPage


def index(request):
    'Index page'
    return render(request, 'page/index.html')


class PageStaticView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, alias):
        static_page = StaticPage.objects.filter(alias=alias).values('title', 'content').first()
        form = StaticPageForm(static_page)
        # replace template name
        rendered_page = render_to_string(template_name='test.html', context={'form': form})
        return Response({'page': rendered_page})
