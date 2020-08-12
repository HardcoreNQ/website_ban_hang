from django.db import models

class Category(models.Model):
    code = models.CharField(max_length=20,verbose_name='Mã', unique=True)
    name = models.CharField(max_length=100, verbose_name='Tên')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Nhóm sản phẩm", 
                            on_delete=models.PROTECT)
    code = models.CharField(max_length=20, verbose_name="Mã", unique=True)
    name = models.CharField(max_length=100, verbose_name="Tên")
    price = models.IntegerField(verbose_name="Giá")
    description = models.CharField(max_length=300, verbose_name="Mô tả", blank=True)
    image = models.ImageField(upload_to='static/images', blank=True,
                            null=True, verbose_name="Ảnh")

class Order(models.Model):
    class Status:
        PENDING = 0
        DELIVERED = 1
        CANCELED = 2
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    #product = models.ForeignKey(Product, on_delete=models.PROTECT)
    orderDate = models.DateTimeField()
    deliverDate = models.DateTimeField(null=True)
    status = models.IntegerField()

class Orderline(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()