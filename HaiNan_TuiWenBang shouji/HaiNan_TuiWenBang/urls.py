"""HaiNan_TuiWenBang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from App import views
from HaiNan_TuiWenBang import settings
urlpatterns = [
    #登录，注册，退出三件套的URL
    path('admin/', admin.site.urls),
    path('logout/',views.User_logout),
    path('login/',views.User_login),
    path('register/',views.User_register),
    #==============================#
    #====admin Login ======
    path('AdminLogin/',views.AdminLogin),
    path('logout_by_admin/',views.logout_by_admin),
    #================
    path('index/',views.index),#首页
    path('detailed/<int:id>',views.detailed),#详情页
    path('detailedCity/<int:id>',views.detailedCity),
    path('post-comment/<int:article_id>/', views.post_comment),
    path('search_Scenic/',views.search_Scenic),
    path('password-reset/', include('password_reset.urls')),
    path('AdminMenu/',views.AdminMenu),
    path('Admin_Tourism/<int:id>',views.Admin_Tourism),
    path('Admin_User/<int:id>',views.Admin_User),
    path('Admin_car/<int:id>',views.Admin_car),
    path('meishi/<int:id>',views.meishi),
    path('Tourism_soso/<int:id>',views.Tourism1),
    path('Tourism_del/<int:id>',views.Tourism_del),
    path('User_soso/<int:id>',views.User1),
    path('User_del/<int:id>',views.User_del),
    path('Tourism_update/<int:id>',views.Tourism_update),
    path('Tourism_User/<int:id>',views.Tourism_User),
    path('Tourism_Add/',views.Tourism_Add),
    path('edit/',views.edit),
    path('gerenziliao/',views.gerenziliao),
    path('AddMoney/',views.AddMony),
    path('AdminMeishi/<int:id>',views.Admin_meishi),

    path('Article_Add/',views.Article_Add),
    path('Article_List/<int:id>',views.Article_List),
    path('Article_detail/<int:id>',views.Article_detail),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
