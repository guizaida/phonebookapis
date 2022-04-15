from phonebookapi.models import phonebook
from phonebookapi.serializers import PhonebookSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from phonebookapi import models
import hashlib
import time
from django.http import JsonResponse
from phonebookapi.log_write import Setup_Logger
# Create your views here.
logger = Setup_Logger('Main_Api_Log','MainApiLog.log')
class PhonebookViewSet(viewsets.ModelViewSet):
    queryset = phonebook.objects.all()
    serializer_class = PhonebookSerializer

class errorcode:
    errorcode= {
        503:{
            'code':503,
            'msg':'請求異常'
        },
        1000:{
            'code':1000,
            'msg':'此帳號尚未註冊或密碼錯誤'
        },
        1001:{
            'code':1001,
            'msg':'帳號或密碼錯誤'
        },
        1002:{
            'code':1002,
            'msg':'用戶攔是必須的'
        },
        1003:{
            'code':1003,
            'msg':'用戶已存在'
        },
        1004:{
            'code':1004,
            'msg':'非法電話號碼'
        },
        1005:{
            'code':1005,
            'msg':'無此帳號或以刪除'
        },
        1006:{
            'code':1006,
            'msg': '密碼錯誤'
        },
        1007:{
            'code':1007,
            'msg': '未登入'
        },
    }
    
class AuthView(APIView):
    #登入api
    def post(self, request, *args, **kwargs):
        ret = {'code': 201, 'msg': '成功登入'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            # 驗證此帳號是否已存在資料庫
            obj = models.phonebook.objects.filter(UserName=user, Password=pwd).first()
            if not obj:
                ret = errorcode.errorcode[1000]
            else:
                # 存在就創建或更新token
                token = md5(user)
                ret['token'] = token
                models.UserToken.objects.update_or_create(defaults={'token': token}, user=obj)
        except Exception as e:
            ret = errorcode.errorcode[503]
            logger.info('Auth Error - {0}'.format(e))   
        return JsonResponse(ret)
    
class updateView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 201, 'msg': '成功修改'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            pwdd = request._request.POST.get('VerifyPassword')
            npnb = request._request.POST.get('NewPhoneNumber')
            if pwd == pwdd:
                obj = models.phonebook.objects.filter(UserName=user, Password=pwd)
                if not obj:
                    ret = errorcode.errorcode[1001]
                else:
                    obj.update(PhoneNumber=npnb)
        except Exception as e:
            ret = errorcode.errorcode[503]
            logger.info('update Error - {0}'.format(e))   
        return JsonResponse(ret)
    
    
class registerView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 201, 'msg': '成功註冊'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            phnb = request._request.POST.get('PhoneNumber')
            try:
                int(phnb)
                obj = models.phonebook.objects.filter(UserName=user).first()
                if not obj:
                    models.phonebook.objects.update_or_create(UserName =user,Password = pwd,PhoneNumber = phnb)
                else:
                    if not user:
                        ret = errorcode.errorcode[1002]
                    else:
                        ret = errorcode.errorcode[1003]
            except:
                ret = errorcode.errorcode[1004]
                logger.info('register Error - {0}'.format(e)) 
            # 驗證資料庫是否存在此用戶
            
        except Exception as e:
            ret = errorcode.errorcode[503]
        return JsonResponse(ret)

class DeleteView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 201, 'msg': '成功刪除帳號'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            pwdd = request._request.POST.get('VerifyPassword')
            if pwd == pwdd:
                obj = models.phonebook.objects.filter(UserName =user,Password = pwd).first()
                if not obj:
                    ret = errorcode.errorcode[1005]
                else:
                    models.phonebook.objects.filter(UserName =user).delete()
            else:
                ret = errorcode.errorcode[1006]
                
        except Exception as e:
            ret = errorcode.errorcode[503]
            logger.info('Delete Error - {0}'.format(e)) 
        return JsonResponse(ret)
    
class tkcheckView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 201, 'msg': '驗證成功'}
        try:
            tk = request._request.POST.get('Token')
            obj = models.UserToken.objects.filter(token = tk).first()
            if not obj:
                ret = errorcode.errorcode[1007]
        except Exception as e:
            ret = errorcode.errorcode[503]
            logger.info('tkcheck Error - {0}'.format(e)) 
        return JsonResponse(ret)
    
    
    
def md5(user):
    # 生成随机字符串
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()
