from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage()

@api_view(['GET'])
def searchProduct(request):
    #productList = Product.objects.all()
    productName = request.GET.get('product_name', '')
    categoryId = request.GET.get('category_id', '')
    categoryId = int(categoryId) if categoryId != '' else 0
    priceRange = request.GET.get('price_range', '')
    priceRange = int(priceRange) if priceRange != '' else 0
    
    productList = findProducts(productName, categoryId, priceRange)
    data = ProductSerializer(productList, many=True).data
    return Response({'productList': data})

@api_view(['GET'])
def getCategoryList(request):
    categoryList = Category.objects.all()
    data = CategorySerializer(categoryList, many=True).data
    return Response({'categoryList': data})

@api_view(['GET'])
def getProductDetail(request, pk):
    product = Product.objects.filter(pk=pk).first()
    if product:
        data = ProductSerializer(product).data
        return Response({'product' : data})
    else:
        return Response({'error': 'Not found'})


@api_view(['POST'])
def orderProducts(request):
    try:
        customer = request.data.get('customer', {})
        items = request.data.get('items', [])

        order = Order()
        order.fullname = customer.get('fullname')
        order.phone = customer.get('phone')
        order.address = customer.get('address')
        order.orderDate = datetime.now()
        order.status = Order.Status.PENDING
        order.save()

        for item in items:
            orderline = Orderline()
            orderline.order = order
            orderline.product = Product(id=item.get('productId'))
            orderline.price = item.get('price')
            orderline.qty = item.get('qty')
            orderline.save()

        return Response({'success': True})
    except Exception as e:
        return Response({'success': False, 'error': str(e)})

def findProducts(productName, categoryId, priceRange):
    prices = {
        0:{'min':None, 'max':None},
        1:{'min':None, 'max':10},
        2:{'min':10,   'max': 15},
        3:{'min':15,   'max': 20},
        4:{'min':20,   'max': None},
    }
    minPrice, maxPrice = prices[priceRange]['min'], prices[priceRange]['max']
    productList = Product.objects.all()
    if productName != '':
        productList = productList.filter(name__contains=productName)
    if minPrice != None:
        productList = productList.filter(price__gte=minPrice*1e6)
    if maxPrice:
        productList = productList.filter(price__lte=maxPrice*1e6)
    if categoryId:
        productList = productList.filter(category__id=categoryId)
    return productList

@api_view(['POST'])
def saleProducts(request):
    try:
        productGet = request.data.get('product', {})

        product = Product()
        codeProduct = Product.objects.all().count() + 1
        product.code = 'SP0' + str(codeProduct)
        product.category = productGet.get('categoryId')
        product.name = productGet.get('name')
        product.price = productGet.get('price')
        product.description = productGet.get('description')
        product.image = productGet.files.get('image')
        product.save()
        saved_path = fs.save('static/' + product.image.name, product.image)
        print(product.image)
        return Response({'success': True})
    except Exception as e:
        return Response({'success': False, 'error': str(e)})
