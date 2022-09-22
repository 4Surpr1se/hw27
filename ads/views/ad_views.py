import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse


from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from ads.models.ad_and_cat import Ad
from hw27.settings import TOTAL_ON_PAGE


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):

    def get(self, request):
        response = []
        ads = Ad.objects.all().order_by('-price')
        page = request.GET.get('page')
        paginator = Paginator(ads, TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)
        for ad in page_obj:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id_id,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
                "category_id": ad.category_id_id
            })

        return JsonResponse({'items': response,
                             'num_pages': paginator.num_pages,
                             'total': paginator.count},
                            status=200,
                            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):

    model = Ad

    fields = ["name", "author_id", "price", "description", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):

        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
                name=ad_data["name"],
                author_id_id=ad_data["author_id"],
                price=ad_data["price"],
                description=ad_data["description"],
                is_published=ad_data["is_published"],
                category_id_id=ad_data["category_id"])

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):

    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "is_published", "image", "category_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data.get("name", self.object.name)
        self.object.author_id_id = ad_data.get("author_id", self.object.author_id)
        self.object.price = ad_data.get("price", self.object.price)
        self.object.description = ad_data.get("description", self.object.description)
        self.object.is_published = ad_data.get("is_published", self.object.is_published)
        self.object.category_id_id = ad_data.get("category_id", self.object.category_id_id)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "category_id": self.object.category_id_id
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
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None,
            "category_id": ad.category_id_id
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdImageAddView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        ad = self.get_object()
        ad.image = request.FILES.get('image', None)

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()

        return JsonResponse({'status': 'Image uploaded'}, status=200)
