from django.utils.deprecation import MiddlewareMixin
from axf.models import UserTicket
from datetime import datetime
from django.http.response import HttpResponseRedirect


class LoginConfig(MiddlewareMixin):
    """ 自定义中间件"""

    def process_request(self, request):
        """在每次请求前验证用户是否登陆"""

        ticket = request.COOKIES.get('ticket', None)
        if ticket:

            if UserTicket.objects.filter(ticket=ticket).exists():
                # 验证当前ticket是否存在
                ticket = UserTicket.objects.get(ticket=ticket)

                if ticket.outtime.replace(tzinfo=None) > datetime.utcnow():
                    # 验证ticket是否失效
                    # 注意，数据库存时间时会少8个小时，但是用浏览器取出来又会自动加上8个小时，
                    # 但是在pycharm中，取出来的时间不会自动加上8个小时，用ticket.outtime.replace(tzinfo=None)取出数据少8个小时的时间
                    # 再用datetime.utcnow()取出0时区的时间后进行比较

                    user = ticket.u
                    request.user = user
                    # 如果登陆了给就把user添加到相应请求中。以便在页面中使用user相关时间

                    return None
                else:
                    UserTicket.objects.filter(ticket=ticket).delete()
                    # 对过期的ticket进行删除

        else:
            if request.path == '/axf/cart/':
                # 用户点击购物车时需要登陆
                return HttpResponseRedirect('/axf/login')
            else:
                return None



