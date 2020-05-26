import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Category


# CRUD - Category model


# Category List - GET
# Create new Category - POST
@csrf_exempt
def categories_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        categories_json = [category.short() for category in categories]
        return JsonResponse(categories_json, safe=False)
    elif request.method == 'POST':
        request_body = json.loads(request.body)
        # validate request body

        # # Option 1
        # category = Category(name=request_body['name'])
        # category.save()

        # Option 2
        category = Category.objects.create(name=request_body.get('name', 'default name'))

        return JsonResponse(category.short())


# Get selected Category - GET
# Update selected Category - PUT
# Delete selected Category - DELETE
@csrf_exempt
def category_detail(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist as e:
        return JsonResponse({'error': str(e)})

    if request.method == 'GET':
        return JsonResponse(category.short())

    elif request.method == 'PUT':
        request_body = json.loads(request.body)
        # validate request body
        category.name = request_body.get('name', category.name)
        category.save()

        return JsonResponse(category.short())

    elif request.method == 'DELETE':
        category.delete()

        return JsonResponse({'deleted': True})


def category_products(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist as e:
        return JsonResponse({'error': str(e)})

    products = category.products.all()
    products_json = [product.full() for product in products]

    return JsonResponse(products_json, safe=False)
