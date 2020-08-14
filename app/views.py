from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage()

@api_view(['POST'])
def signup(request):
    phone = request.data.get('phone')
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    password2 = request.data.get('password2', '')

    errors = {}

    if username == '':
        errors['username'] = 'Tên đăng nhập không được trống'

    if User.objects.filter(username=username):
        errors['username'] = 'Tài khoản đã tồn tại'
    
    if phone == '':
        errors['phone'] = 'Số điện thoại không được trống'

    if len(password) < 6:
        errors['password'] = 'Mật khẩu phải có độ dài tổi thiểu 6 kí tự'

    if password.isdigit():
        errors['password'] = 'Mật khẩu không thể chứa toàn chữ số'

    if password2 != password:
        errors['password2'] = 'Mật khẩu xác thực không đúng'
    
    if len(errors) == 0:
        user = User.objects.create_user(username=username, password=password)
        return Response({'success' : True})
    
    return Response({'success' : False, 'errors': errors})

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

def validateSaleProduct(data):
  
    errors = {}
    if not data.get('categoryId'):
        errors['categoryId'] = "Bạn phải chọn loại sản phẩm"

    if not data.get("name"):
        errors['name'] = "Bạn phải chọn tên sản phẩm"

    if not data.get("price", "").isdigit():
        errors['price'] = "Giá sản phẩm không hợp lệ"
    
    if not data.get('image'):
        errors['image'] = "Bạn phải chọn ảnh sản phẩm"

    return errors

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def saleProducts(request):
    try:
        data = request.data
        errors = validateSaleProduct(data)
        if len(errors) > 0:
            return Response({'success': False, 'errors': errors})

        product = Product()
        codeProduct = Product.objects.all().count() + 1
        product.code = 'SP0' + str(codeProduct)
        product.category = Category(id=data.get('categoryId'))
        product.name = data.get('name')
        product.price = data.get('price')
        product.description = data.get('description')
        product.image = data.get('image')
        product.postUser = request.user
        product.save()
    
        return Response({'success': True})
    except Exception as e:
        return Response({'success': False, 'errors': {'all': str(e)}})
