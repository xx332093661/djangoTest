# coding: utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def user_verify_middleware(get_response):
    # 初始化操作
    # print('init操作')  # debug运行模式会初始化两次

    def middleware(request):
        # 调用视图函数之前的逻辑处理
        # print('调用视图函数之前的逻辑处理')
        print(request.path)
        if request.path not in ['/fanxiangce/unconfirmed', '/fanxiangce/resend_confirmation'] \
                and request.user.is_authenticated and not request.user.profile.confirmed:
            print('没验证')
            return HttpResponseRedirect(reverse('fanxiangce:unconfirmed'))
        response = get_response(request)  # 调用视图函数
        # 调用视图函数之后的处理逻辑
        # print('调用视图函数之后的处理逻辑')
        return response

    return middleware
