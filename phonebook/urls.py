from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from phonebookapi import views

router = DefaultRouter()
router.register(r'phonebook', views.PhonebookViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/v1/Login/$', views.AuthView.as_view()),
    url(r'^api/v1/Register/$', views.registerView.as_view()),
    url(r'^api/v1/Deleteacc/$', views.DeleteView.as_view()),
    url(r'^api/v1/tokencheck/$', views.tkcheckView.as_view()),
    url(r'^api/v1/pnbupdate/$', views.updateView.as_view()),
]