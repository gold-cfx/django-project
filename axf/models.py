from django.db import models

# Create your models here.


class Main(models.Model):

    id = models.AutoField(primary_key=True)
    img = models.CharField(max_length=255)    # 分类图片
    name = models.CharField(max_length=255)   # 分类名称
    trackid = models.CharField(max_length=10) # 通用id

    class Meta:
        abstract = True  # 把这个类设置为可以继承的类(父类)


class MainWheel(Main):
    # 轮播banner
    class Meta:
        db_table= 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table= 'axf_mustbuy'


class MainShop(Main):
    # 展示
    class Meta:
        db_table= 'axf_shop'


# 主要展示的商品
class MainShow(Main):

    categoryid = models.CharField(max_length=16,default=' ')   #
    brandname = models.CharField(max_length=100, default=' ')

    img1 = models.CharField(max_length=200)        # 图片1
    longname1 = models.CharField(max_length=100)   # 名称1
    price1 = models.FloatField(default=0)          # 优惠价格1
    marketprice1 = models.FloatField(default=1)    # 原始价格1
    childcid1 = models.CharField(max_length=16, default=' ')
    productid1 = models.CharField(max_length=16, default=' ')

    img2 = models.CharField(max_length=200)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    childcid2 = models.CharField(max_length=16, default=' ')
    productid2 = models.CharField(max_length=16, default=' ')

    img3 = models.CharField(max_length=200)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)
    childcid3 = models.CharField(max_length=16, default=' ')
    productid3 = models.CharField(max_length=16, default=' ')

    class Meta:
        db_table = 'axf_mainshow'


# 闪购（左侧导航栏）
class FoodType(models.Model):

    id = models.AutoField(primary_key=True)
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):

    id = models.AutoField(primary_key=True)
    productid = models.CharField(max_length=16)        # 商品id
    productimg = models.CharField(max_length=200)      # 商品图片地址
    productname = models.CharField(max_length=100)     # 商品名称
    productlongname = models.CharField(max_length=200) # 商品规格
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100, default=' ')
    specifics = models.CharField(max_length=100)       # 规格
    price = models.FloatField(default=0)               # 折扣价
    marketprice = models.FloatField(default=1)         # 原件
    categoryid = models.CharField(max_length=16)       # 分类id
    childcid = models.CharField(max_length=16)         # 子分类id
    childcidname = models.CharField(max_length=100)    # 名称
    dealerid = models.CharField(max_length=16, default=' ')
    storenums = models.IntegerField(default=1)         # 排序
    productnum = models.IntegerField(default=1)        # 销量排序


class UserModel(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)  # 用户名
    password = models.CharField(max_length=256)              # 密码
    email = models.CharField(max_length=64, unique=True)     # 邮件
    sex = models.BooleanField(default=False)                 # 性别，Flase表示女
    icon = models.ImageField(upload_to='icons')              # 头像
    is_delete = models.BooleanField(default=False)           # 是否删除

    class Meta:
        db_table = 'axf_users'


class UserTicket(models.Model):

    ticket = models.CharField(max_length=255)
    outtime = models.DateTimeField()
    u = models.OneToOneField(UserModel)

    class Meta:
        db_table = 'user_ticket'


class CartModel(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel)            # 关联用户
    goods = models.ForeignKey(Goods)               # 关联商品
    c_num = models.IntegerField(default=1)         # 商品数量
    is_select = models.BooleanField(default=True)  # 是否选择

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel)                  # 关联用户
    o_num = models.CharField(max_length=64)              # 数量
    o_status = models.IntegerField(default=0)            # 状态，0代表已下单但是未付款1已付款未发货2已付款已发货
    o_create = models.DateTimeField(auto_now_add=True)   # 订单生成时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):

    id = models.AutoField(primary_key=True)
    goods = models.ForeignKey(Goods)            # 关联商品
    order = models.ForeignKey(OrderModel)       # 关联订单
    goods_num = models.IntegerField(default=1)  # 商品个数

    class Meta:
        db_table = 'axf_order_goods'


