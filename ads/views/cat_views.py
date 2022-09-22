import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from ads.models import Categories


@method_decorator(csrf_exempt, name='dispatch')
class CatView(View):

    def get(self, request):
        response = []
        cats = Categories.objects.all().order_by('name')
        for cat in cats:
            response.append({
                'id': cat.id,
                'name': cat.name,
            })

        return JsonResponse(response, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Categories
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ad = Categories.objects.create(name=ad_data["name"])
        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
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


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):

    model = Categories
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Categories
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data.get("name", self.object.name)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name})