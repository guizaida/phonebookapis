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
    
    
class AuthView(APIView):
    #登入api
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '成功登入'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            # 驗證此帳號是否已存在資料庫
            obj = models.phonebook.objects.filter(UserName=user, Password=pwd).first()
            if not obj:
                ret['code'] = 1000
                ret['msg'] = '此帳號尚未註冊或密碼錯誤'
            else:
                # 存在就創建或更新token
                token = md5(user)
                ret['token'] = token
                models.UserToken.objects.update_or_create(defaults={'token': token}, user=obj)
        except Exception as e:
            ret['code'] = 503
            ret['msg'] = '請求異常'
            logger.info('Auth Error - {0}'.format(e))   
        return JsonResponse(ret)
    
class updateView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '成功修改'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            pwdd = request._request.POST.get('VerifyPassword')
            npnb = request._request.POST.get('NewPhoneNumber')
            if pwd == pwdd:
                obj = models.phonebook.objects.filter(UserName=user, Password=pwd)
                if not obj:
                    ret['code'] = 1001
                    ret['msg'] = '帳號或密碼錯誤'
                else:
                    obj.update(PhoneNumber=npnb)
        except Exception as e:
            ret['code'] = 503
            ret['msg'] = '請求異常'
            logger.info('update Error - {0}'.format(e))   
        return JsonResponse(ret)
    
    
class registerView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '成功註冊'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            phnb = request._request.POST.get('PhoneNumber')
            print(user)
            print(pwd)
            print(phnb)
            try:
                int(phnb)
                obj = models.phonebook.objects.filter(UserName=user).first()
                if not obj:
                    models.phonebook.objects.update_or_create(UserName =user,Password = pwd,PhoneNumber = phnb)
                else:
                    if not user:
                        ret['code'] = 1002
                        ret['msg'] = '用戶攔是必須的'
                    else:
                        ret['code'] = 1003
                        ret['msg'] = '用戶已存在'
            except:
                ret['code'] = 1004
                ret['msg'] = '非法電話號碼'
                logger.info('register Error - {0}'.format(e)) 
            # 驗證資料庫是否存在此用戶
            
        except Exception as e:
            ret['code'] = 503
            ret['msg'] = '請求異常'
        return JsonResponse(ret)

class DeleteView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '成功刪除帳號'}
        try:
            user = request._request.POST.get('UserName')
            pwd = request._request.POST.get('Password')
            pwdd = request._request.POST.get('VerifyPassword')
            if pwd == pwdd:
                obj = models.phonebook.objects.filter(UserName =user,Password = pwd).first()
                if not obj:
                    ret['code'] = 1005
                    ret['msg'] = '無此帳號或以刪除'
                else:
                    models.phonebook.objects.filter(UserName =user).delete()
            else:
                ret['code'] = 1006
                ret['msg'] = '密碼錯誤'
                
        except Exception as e:
            ret['code'] = 503
            ret['msg'] = '請求異常'
            logger.info('Delete Error - {0}'.format(e)) 
        return JsonResponse(ret)
    
class tkcheckView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '驗證成功'}
        try:
            tk = request._request.POST.get('Token')
            print(tk)
            obj = models.UserToken.objects.filter(token = tk).first()
            if not obj:
                ret['code'] = 1007
                ret['msg'] = '未登入'
        except Exception as e:
            ret['code'] = 503
            ret['msg'] = '請求異常'
            logger.info('tkcheck Error - {0}'.format(e)) 
        return JsonResponse(ret)
    
    
    
def md5(user):
    # 生成随机字符串
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()
