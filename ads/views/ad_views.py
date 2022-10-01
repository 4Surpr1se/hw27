import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse


from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models.ad_and_cat import Ad
from ads.permissions import DeleteOrUpdateAdPermission
from ads.serializers import AdSerializer
from hw27.settings import TOTAL_ON_PAGE


# TODO ПЕРЕДЕЛАТЬ CATEGORY_ID ID ID ID ID ID ID и AUTHOR_ID ID ID ID ID ID ID
@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        response = []
        ads = Ad.objects.all().order_by('-price')

        if cat_id := request.GET.get('cat'):
            ads = ads.filter(category__id__exact=cat_id)

        if name_field := request.GET.get('text'):
            ads = ads.filter(name__icontains=name_field)

        if location_field := request.GET.get('location'):
            ads = ads.filter(author__location__name__icontains=location_field)

        if price_from := request.GET.get('price_from'):
            ads = ads.filter(price__gte=price_from)

        if price_to := request.GET.get('price_to'):
            ads = ads.filter(price__lte=price_to)

        page = request.GET.get('page')
        paginator = Paginator(ads, TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)
        for ad in page_obj:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
                "category_id": ad.category_id
            })

        return JsonResponse({'items': response,
                             'num_pages': paginator.num_pages,
                             'total': paginator.count},
                            status=200,
                            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):

    model = Ad

    fields = ["name", "user", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):

        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
                name=ad_data["name"],
                user_id=ad_data["user"],
                price=ad_data["price"],
                description=ad_data["description"],
                is_published=ad_data["is_published"],
                category_id=ad_data["category"])

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


# @method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    # fields = ["name", "author", "price", "description", "is_published", "image", "category"]
    permission_classes = [IsAuthenticated, DeleteOrUpdateAdPermission]

    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #
    #     ad_data = json.loads(request.body)
    #     self.object.name = ad_data.get("name", self.object.name)
    #     self.object.author_id = ad_data.get("author_id", self.object.author_id)
    #     self.object.price = ad_data.get("price", self.object.price)
    #     self.object.description = ad_data.get("description", self.object.description)
    #     self.object.is_published = ad_data.get("is_published", self.object.is_published)
    #     self.object.category_id = ad_data.get("category", self.object.category_id)
    #
    #     try:
    #         self.object.full_clean()
    #     except ValidationError as e:
    #         return JsonResponse(e.message_dict, status=422)
    #
    #     self.object.save()
    #     return JsonResponse({
    #         "id": self.object.id,
    #         "name": self.object.name,
    #         "author": self.object.author_id,
    #         "price": self.object.price,
    #         "description": self.object.description,
    #         "is_published": self.object.is_published,
    #         "image": self.object.image.url if self.object.image else None,
    #         "category": self.object.category_id
    #     })


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)
    # model = Ad
    #
    # def get(self, request, *args, **kwargs):
    #     try:
    #         ad = Ad.get_object()
    #     except Exception as e:
    #         return JsonResponse({'error': 'Not found',
    #                              'error_name': str(e)}, status=404)
    #
    #     return JsonResponse({
    #         "id": ad.id,
    #         "name": ad.name,
    #         "author": ad.author_id,
    #         "price": ad.price,
    #         "description": ad.description,
    #         "is_published": ad.is_published,
    #         "image": ad.image.url if ad.image else None,
    #         "category": ad.category_id
    #     })


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
