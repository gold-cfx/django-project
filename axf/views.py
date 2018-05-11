
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from axf import models


# Create your views here.
from utils.fun import myticket


def home(request):

    if request.method == 'GET':
        data = {
            'banners':models.MainWheel.objects.all(),
            'navs':models.MainNav.objects.all(),
            'mustbuys':models.MainMustBuy.objects.all(),
            'shops':models.MainShop.objects.all(),
            'mainshow':models.MainShow.objects.all()
        }
        return render(request, 'home/home.html',data)


def login(request):

    if request.method == 'GET':

        return render(request, 'user/user_login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if models.UserModel.objects.filter(username=username).exists():

            user = models.UserModel.objects.get(username=username)

            if check_password(password, user.password):

                response = HttpResponseRedirect('/axf/home/')
                outtime = datetime.now() + timedelta(days=1)
                ticket = myticket()
                response.set_cookie('ticket', ticket, expires=outtime)


                if models.UserTicket.objects.filter(u_id=user.id).exists():

                    u_ticket = models.UserTicket.objects.get(u_id=user.id)
                    u_ticket.ticket = ticket
                    u_ticket.outtime = outtime
                    u_ticket.save()
                else:
                    models.UserTicket.objects.create(
                        ticket=ticket,
                        outtime=outtime,
                        u_id=user.id)

                return response
            else:
                return render(request, 'user/user_login.html', {'ps':'用户密码错误'})
        else:
            return render(request, 'user/user_login.html', {'us':'用户名错误'})


def register(request):

    if request.method == 'GET':

        return render(request, 'user/user_register.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)
        icon = request.FILES.get('icon')

        models.UserModel.objects.create(username=username,
                                 email=email,
                                 password=password,
                                 icon = icon)

        return HttpResponseRedirect('/axf/login/')


def myself(request):

    if request.method == 'GET':

        date = {}
        unpayed, payed = 0, 0
        user = request.user
        if user and user.id:
            orders = user.ordermodel_set.all() # 找到OrderModel中user的所有订单,注意ordermodel_set全为小写
            for order in orders:
                if order.o_status == 0:
                    unpayed += 1
                elif order.o_status == 1:
                    payed += 1

            date['unpayed'] = unpayed
            date['payed'] = payed

        return render(request, 'mine/mine.html', date)


def logout(request):

    user = request.user
    models.UserTicket.objects.filter(u_id=user.id).delete()
    response = HttpResponseRedirect('/axf/home/')
    response.delete_cookie('ticket')
    return response


def cart(request):

    if request.method == 'GET':

        cart = models.CartModel.objects.all()

        return render(request,'cart/cart.html', {'cart':cart})


def market(request):

    if request.method == 'GET':

        return HttpResponseRedirect(reverse('axf:marketinfo',args=(104749, 0, 0)))


def marketinfo(request, typeid, childcids, sort):

    if request.method == 'GET':

        data = {}
        types = models.FoodType.objects.all()
        type1 = models.FoodType.objects.filter(typeid=typeid).all()

        if childcids == '0':
            goods2 = models.Goods.objects.filter(categoryid=typeid).all()
        else:
            goods2 = models.Goods.objects.filter(categoryid=typeid).filter(childcid=childcids).all()

        goods21 = goods2.order_by('-storenums')
        goods22 = goods2.order_by('-productnum')
        goods23 = goods2.order_by('-price')
        goods24 = goods2.order_by('price')

        if sort == '0':
            goods = goods2
        elif sort == '1':
            goods = goods21
        elif sort == '2':
            goods = goods22
        elif sort == '3':
            goods = goods23
        else:
            goods = goods24

        childs = type1.first().childtypenames.split('#')
        child = []
        for i in childs:
            child.append(i.split(':'))

        data['typesid'] = typeid
        data['types'] = types
        data['goods'] = goods
        data['child'] = child
        data['childcids'] = childcids

        return render(request, 'market/market.html', data)


def addgood(request):

    if request.method == 'POST':
        user = request.user

        if user and user.id:
            data = {
                'msg': '添加成功',
                'code': 200,
            }
            goods_id = request.POST.get('good_id')
            good = models.CartModel.objects.filter(user_id=user.id, goods_id=goods_id).all()
            if good:
                good[0].c_num += 1
                good[0].save()
                data['c_num'] = good[0].c_num
            else:
                c_num = 1
                models.CartModel.objects.create(
                    user=user,
                    goods_id= goods_id,
                )
                data['c_num'] = c_num

            return JsonResponse(data)
        else:
            return HttpResponseRedirect('/axf/login/')


def subgood(request):
    if request.method == 'POST':
        user = request.user

        if user and user.id:

            goods_id = request.POST.get('good_id')
            good = models.CartModel.objects.filter(user_id=user.id, goods_id=goods_id).all()

            if good:
                data = {
                    'msg': '删除成功',
                    'code': 200,
                }
                if good[0].c_num == 1:
                    good.first().delete()
                    data['c_num'] = 0
                else:
                    good[0].c_num -= 1
                    good[0].save()
                    data['c_num'] = good[0].c_num

                return JsonResponse(data)
            else:
                return JsonResponse({'msg': '没有商品可以删除','code': 200,})
        else:
            return HttpResponseRedirect('/axf/login/')


def goodselect(request):

    if request.method == 'POST':

        goodid = request.POST.get('id')

        good = models.CartModel.objects.filter(id=goodid)[0]

        if good.is_select:

            good.is_select = False
        else:
            good.is_select = True

        good.save()

        data = {
            'msg': '更改成功',
            'code': 200,
            'status': good.is_select
        }

        return JsonResponse(data)


def allselect(request):

    if request.method == 'POST':


        goods = models.CartModel.objects.all()

        for good in goods:

            good.is_select = True

        data = {
            'msg': '更改成功',
            'code': 200,
            'status': True
        }
        return JsonResponse(data)


def order(request):

    if request.method == 'GET':

        user = request.user
        if user and user.id:

            cart_good = models.CartModel.objects.filter(user_id=user.id).filter(is_select=True).all()
            if cart_good:
                # 创建订单
                order = models.OrderModel.objects.create(user=user, o_status=0)
                # 创建详细订单
                for good in cart_good:
                    models.OrderGoodsModel.objects.create(goods=good.goods, order=order, goods_num=good.c_num)
                # 删除购物车
                models.CartModel.objects.all().delete()
                order_info = models.OrderGoodsModel.objects.filter(order_id=order.id)

                return render(request, 'order/order_info.html', {'orderid': order.id, 'order_info': order_info})
            else:
                return HttpResponseRedirect('/axf/cart/')


def pay(request, orderid):

    if request.method == 'GET':
        order = models.OrderModel.objects.get(id=orderid)
        order.o_status = 1
        order.save()
        return HttpResponseRedirect('/axf/myself')


def waitpay(request):

    if request.method == 'GET':

        orders = models.OrderModel.objects.filter(o_status=0).all()

        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


def payed(request):
    if request.method == 'GET':
        orders = models.OrderModel.objects.filter(o_status=1).all()

        return render(request, 'order/order_list_payed.html', {'orders': orders})


def deleteorder(request, orderid):

    if request.method == 'GET':

        models.OrderGoodsModel.objects.filter(order_id=orderid).all().delete()
        models.OrderModel.objects.filter(id=orderid).all().delete()

        return HttpResponseRedirect('/axf/myself/')

