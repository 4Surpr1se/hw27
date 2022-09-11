import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ad


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(View):

    def get(self, request):
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):

    def get(self, request):
        response = []
        ads = Ad.objects.all()
        for ad in ads:
            response.append({
                'Id': ad.Id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'address': ad.address,
                'is_published': ad.is_published,
            })

        return JsonResponse(response, status=200, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author = ad_data["author"]
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.address = ad_data["address"]
        ad.is_published = ad_data["is_published"]

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()

        return JsonResponse({
            "Id": ad.Id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Exception as e:
            return JsonResponse({'error': 'Not found',
                                 'error_name': str(e)}, status=404)

        return JsonResponse({
            'Id': ad.Id,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description,
            'address': ad.address,
            'is_published': ad.is_published,
        })
