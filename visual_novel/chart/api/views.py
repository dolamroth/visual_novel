from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.exceptions import NotFound

from chart.models import ChartItem


class ChartView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chart/item.html'

    def get(self, request, vn_alias):
        try:
            chart_item = ChartItem.objects.get(visual_novel__alias=vn_alias)
        except ChartItem.DoesNotExist:
            raise NotFound
        return Response(status=200)

