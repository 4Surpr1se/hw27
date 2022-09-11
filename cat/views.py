import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import Resolver404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from cat.models import Categories


@method_decorator(csrf_exempt, name='dispatch')
class CatView(View):

    def get(self, request):
        response = []
        cats = Categories.objects.all()
        for cat in cats:
            response.append({
                'id': cat.id,
                'name': cat.name,
            })

        return JsonResponse(response, status=200, safe=False)

    def post(self, request):
        cat_data = json.loads(request.body)

        cat = Categories()
        cat.name = cat_data["name"]

        try:
            cat.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        cat.save()

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        })


class CatDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):

        try:
            cat = self.get_object()
        except Exception as e:
            return JsonResponse({"error": "Not found",
                                 'error_name': str(e)}, status=404)

        return JsonResponse({
            'id': cat.id,
            'name': cat.name
        })
