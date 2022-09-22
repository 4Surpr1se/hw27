import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from ads.geo_helper import GeoFinder
from ads.models.loc_and_user import Author, Location
from hw27.settings import TOTAL_ON_PAGE


@method_decorator(csrf_exempt, name='dispatch')
class AuthorView(View):

    def get(self, request):
        response = []
        ads = Author.objects.all().annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))

        page = request.GET.get('page')
        paginator = Paginator(ads, TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)

        for ad in page_obj:
            response.append({
                "id": ad.id,
                "first_name": ad.first_name,
                "last_name": ad.last_name,
                "username": ad.username,
                "password": ad.password,
                "role": ad.role,
                "age": ad.age,
                "location_id": ad.location_id_id,
                "total_ads": ad.total_ads
            })

        return JsonResponse({'items': response,
                             'num_pages': paginator.num_pages,
                             'total': paginator.count},
                            status=200,
                            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorCreateView(CreateView):

    model = Author

    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def post(self, request, *args, **kwargs):

        ad_data = json.loads(request.body)

        location = f'{ad_data["location"][0]}, {ad_data["location"][1]}'

        right_location = Location.objects.all().filter(name=location)
        # TODO НАПИШИТЕ, ПОЖАЛУЙСТА, КУДА ЛУЧШЕ СКЛАДЫВАТЬ ВСЮ ЭТУ ЛОГИКУ

        if right_location.first() is not None:
            location_id_id = right_location.first().id
        else:
            lat, lng = GeoFinder(location).get_lat_lng()
            created_location = Location.objects.create(name=location, lat=lat, lng=lng)
            location_id_id = created_location.id

        ad = Author.objects.create(
                first_name=ad_data["first_name"],
                last_name=ad_data["last_name"],
                username=ad_data["username"],
                password=ad_data["password"],
                role=ad_data["role"],
                age=ad_data["age"],
                location_id_id=location_id_id)

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": ad.id,
            "name": ad.username,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AuthorDeleteView(DeleteView):

    model = Author
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorUpdateView(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        if ad_data.get('location'):
            location = f'{ad_data["location"][0]}, {ad_data["location"][1]}'

            right_location = Location.objects.all().filter(name=location)
            # TODO НАПИШИТЕ, ПОЖАЛУЙСТА, КУДА ЛУЧШЕ СКЛАДЫВАТЬ ВСЮ ЭТУ ЛОГИКУ
            if right_location.first():
                location_id_id = right_location.first().id
            else:
                lat, lng = GeoFinder(location).get_lat_lng()
                created_location = Location.objects.create(name=location, lat=lat, lng=lng)
                location_id_id = created_location.id

            self.object.location_id_id = location_id_id

        self.object.first_name = ad_data.get("first_name", self.object.first_name)
        self.object.last_name = ad_data.get("last_name", self.object.last_name)
        self.object.username = ad_data.get("username", self.object.username)
        self.object.password = ad_data.get("password", self.object.password)
        self.object.role = ad_data.get("role", self.object.role)
        self.object.age = ad_data.get("age", self.object.age)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "location_id": self.object.location_id_id
        })


class AuthorDetailView(DetailView):

    model = Author

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Exception as e:
            return JsonResponse({'error': 'Not found',
                                 'error_name': str(e)}, status=404)

        return JsonResponse({
                "id": ad.id,
                "first_name": ad.first_name,
                "last_name": ad.last_name,
                "username": ad.username,
                "password": ad.password,
                "role": ad.role,
                "age": ad.age,
                "location_id": ad.location_id_id,
                "total_ads": ad.total_ads
            })
