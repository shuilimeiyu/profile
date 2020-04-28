from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import Region,Tourism,Administrators,Tourism_status,User,Comment,car_status,car,User_information,weathe,HaiNan_chwl,ArticlePost
from django.contrib.auth import authenticate,login,logout
from .forms import CommentForm,AdminFrom
from django.core.paginator import Paginator
from django.conf import settings
import requests
import json
import time
import markdown
from django.contrib.auth.hashers import make_password
# Create your views here.


##============               注册、登录、退出 三件套               ===================##



def User_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']

        if password != password2:
            message = "两次输入的密码不同！"
            return render(request,'register.html',locals())
        else:
            pd_username = User.objects.filter(username=username)
            if pd_username:
                message = "用户名已经存在！"
                return render(request, 'register.html', locals())
            pd_email = User.objects.filter(email=email)
            if pd_email:
                message = "邮箱已经存在！"
                return render(request, 'register.html', locals())
            mpwd = make_password(password, None, 'pbkdf2_sha256')
            User.objects.create(username=username, password=mpwd, email=email, first_name=first_name,last_name=last_name)
            return redirect('/login/')
    # User.objects.create_user('username','email.@qq.com','password')
    return render(request,'register.html',locals())
def User_login(request):
    # user = User.objects.create_user('libai', 'libai@qq.com', "5022")
    # user.save()
    # user = authenticate(username="libai", password="5100")
    # return HttpResponse(user.password)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("/index/")
            else:
                message = "账号或者密码出错"
        else:
            message = "请输入账号或者密码"
    return render(request, 'login.html', locals())

def User_logout(request):
    logout(request)
    return redirect("/index/")


##============               END           ===================##


##============                      首页                        ===================##
def index(request):

    if request.method == 'GET':
        page = request.GET.get('page')
        tese_id = request.GET.get('tese_id')
        tecan_id = request.GET.get('tecan_id')
        xiaochi_id = request.GET.get('xiaochi_id')
        zhaopai_id = request.GET.get('zhaopai_id')
        Region1 = Region.objects.filter()
        tourism1 = Tourism.objects.filter().order_by('-total_views')
        paginator = Paginator(tourism1, 6)

        articles = paginator.get_page(page)

        chwl_tese= HaiNan_chwl.objects.filter(category__contains="海南特色").order_by('id')
        chwl_tecan = HaiNan_chwl.objects.filter(category__contains="海南特产").order_by('id')
        chwl_xiaochi = HaiNan_chwl.objects.filter(category__contains="海南小吃").order_by('id')
        chwl_zhaopai = HaiNan_chwl.objects.filter(category__contains="海南招牌小吃").order_by('id')


        paginator_tese = Paginator(chwl_tese, 6)
        tese_show = paginator_tese.get_page(tese_id)

        paginator_tecan = Paginator(chwl_tecan, 6)
        tecan_show = paginator_tecan.get_page(tecan_id)

        paginator_xiaochi = Paginator(chwl_xiaochi, 6)
        xiaochi_show = paginator_xiaochi.get_page(xiaochi_id)


        paginator_zhaopai = Paginator(chwl_zhaopai, 6)
        zhaopai_show = paginator_zhaopai.get_page(zhaopai_id)
    else:
        return HttpResponse("传输方式不能为POST")


    return render(request,'index.html',locals())

##============                   END            ===================##
##============                      详情页                        ===================##

def detailed(request,id):

    Region=Tourism.objects.get(id=id)
    comments = Comment.objects.filter(Tourism_id=id).order_by('-time')
    article = Tourism.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])

    return render(request,'detailed.html',locals())
##============                     END            ===================##

##============                      地区详情界面                        ===================##
def detailedCity(request,id):

    try:
        region1 = Region.objects.get(id=id)
        print(region1.Region_city)
        name = region1.Region_city
        name = name[0:2]
        get_code = weathe.objects.get(name__contains=name)
        print(get_code.code)
        url = f'http://www.weather.com.cn/data/sk/{get_code.code}.html'
        print(url)
        rb = requests.get(url)
        rb.encoding = 'utf-8'
        data = json.loads(rb.text)
        temp = data['weatherinfo']['temp']
        # print(low,high)
    except:
        pass
    if id>=1 and id<=19:
        region1 = Region.objects.get(id=id)
        cite = region1.Region_city
        car1 = region1.car_set.get_queryset()
        tourism1 = region1.tourism_set.get_queryset().order_by('-total_views')
        if not tourism1:
            message = '当前地区没有景点或者网站还没有收录！'
            print(message)
        paginator = Paginator(tourism1, 6)
        page = request.GET.get('page')
        articles = paginator.get_page(page)
        qian = articles.number - 1
        hou = articles.number + 1
        qian2 = articles.number - 2
        hou2 = articles.number + 2
        return render(request,'detailedCity.html',locals())
    else:

        tourism = Tourism.objects.all().order_by('-total_views')
        paginator = Paginator(tourism, 6)
        page = request.GET.get('page')
        articles = paginator.get_page(page)
        return render(request, 'detailedCity.html', locals())
##============                     END            ===================##

##============                      评论                        ===================##


def post_comment(request,article_id):
    article = get_object_or_404(Tourism, id=article_id)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.Tourism = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(f'/detailed/{article_id}')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")

##============                     END            ===================##

##============                      搜索旅游景点                        ===================##
def search_Scenic(request):
    if request.method == "POST":
        search = request.POST['search_Scenic_car']
        page = request.GET.get('page')
        results = Tourism.objects.filter(Tourism_name__contains=search)
        page_1 = len(results)
        if results:
            message = 1
        else:
            message = 0
    return render(request, 'search.html', locals())

##============                     END            ===================##

##============                      管理员登录验证                        ===================##
def logout_by_admin(request):
    if not request.session.get('is_Adminlogin', None):  # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    # request.session.flush()  # 或者使用下面的方法
    del request.session['is_Adminlogin']
    del request.session['Admin_id']
    del request.session['Admin_username']
    return redirect("/index/")

def AdminLogin(request):
    if request.session.get('is_Adminlogin',None):
        return redirect('/Admin_User/1')
    if request.method == 'POST':
        AdminLoginFrom = AdminFrom(request.POST)
        message = '请检查填写的内容'
        if AdminLoginFrom.is_valid():
            username = AdminLoginFrom.cleaned_data['AdminUsername']
            password = AdminLoginFrom.cleaned_data['AdminPassword']
            try:
                Admin = Administrators.objects.get(AdminUsername=username)
                if Admin.AdminPassWord == password:
                    request.session['is_Adminlogin'] = True
                    request.session['Admin_id'] = Admin.id
                    request.session['Admin_username'] = Admin.AdminUsername
                    return redirect('/AdminMenu/')
                else:
                    message = "密码不正确！"


            except:
                message = "用户不存在！"
                # return render(request,'AdminLogin.html',locals())
    login_form = AdminFrom()
    return render(request, 'AdminLogin.html', locals())

##============                     END            ===================##
##============                      后台管理                        ===================##
def AdminMenu(request):
    # list_url = ['/Admin_Tourism/1','/Admin_User/1','/Admin_car/1','/Admin_car/1']
    # list_name =['旅游管理','用户管理','出租车管理','用户分析']
    # test =  zip(list_url, list_name)

    return render(request, 'AdminHeader.html', locals())

def Admin_User(request,id):
    print(id)
    if id==1:
        if request.method == "GET":
            page = request.GET.get('page')
            user = User.objects.filter()
            paginator3 = Paginator(user, 9)
            User_admin_page = paginator3.get_page(page)
            qian = User_admin_page.number - 1
            hou = User_admin_page.number + 1
            return render(request, 'Admin_User.html', locals())
        else:
            user = User.objects.filter()
            paginator3 = Paginator(user, 9)
            User_admin_page = paginator3.get_page(1)
            return render(request, 'Admin_User.html', locals())

    if id==2:
        if request.method == "GET":
            page = request.GET.get('page')
            user = User_information.objects.filter()
            paginator3 = Paginator(user, 9)
            User_admin_page = paginator3.get_page(page)
            qian = User_admin_page.number - 1
            hou = User_admin_page.number + 1
            return render(request, 'Admin_User.html', locals())
        else:
            user = User_information.objects.filter()
            paginator3 = Paginator(user, 9)
            User_admin_page = paginator3.get_page(1)
            return render(request, 'Admin_User.html', locals())

def User1(request,id):
    if id==1:
        if request.method == 'POST':
            soso = request.POST['user_soso']


            User_admin_page = User.objects.filter(username__contains=soso)
            id_page =0
            user_pd = 1
        return render(request, 'Admin_User.html', locals())
    if id==2:
        if request.method == 'POST':
            soso = request.POST['user_soso']

            User_admin_page = User_information.objects.filter(user_id__username__contains=soso)
            id_page = 0
            user_pd = 1
            return render(request, 'Admin_User.html', locals())
def User_del(request,id):
    if id == 1:
        if request.method == "GET":
            User_id = request.GET.get('User_id')
            page = request.GET.get('page')
            print(User_id,id)
            user = User.objects.get(id=User_id).delete()
            a = f'/Admin_User/{id}?page={page}'

            return redirect(a)
    if id == 2:
        if request.method == "GET":
            User_id = request.GET.get('User_id')
            page = request.GET.get('page')
            user = User_information.objects.get(id=User_id).delete()
            # print(id, user.id)
            a = f'/Admin_User/{id}?page={page}'
            return redirect(a)



def Admin_Tourism(request,id):

    if id:
        Tourism_admin = Tourism.objects.filter().order_by('id')
        paginator1 = Paginator(Tourism_admin, 8)
        Tourism_admin_page = paginator1.get_page(id)
        qian = Tourism_admin_page.number - 1
        hou = Tourism_admin_page.number + 1
        qian2 = Tourism_admin_page.number - 2
        hou2 = Tourism_admin_page.number + 2
        pd = 0
    else:
        Tourism_admin = Tourism.objects.filter()
        paginator1 = Paginator(Tourism_admin, 8)
        Tourism_admin_page = paginator1.get_page(1)
        pd = 0
    return render(request,'Tourism.html',locals())
def Tourism1(request,id):
    if request.method == 'POST':
        soso = request.POST['Tourism_soso']
        Tourism_admin_page = Tourism.objects.filter(Tourism_name__contains=soso)

    return render(request, 'Tourism.html', locals())
def Tourism_del(requets,id):
    Tourism_del_id = Tourism.objects.get(id=id)
    Tourism_del_id.delete()
    page = requets.GET.get('page')
    print(page)
    return redirect(f'/Admin_Tourism/{page}')
def Tourism_update(request,id):
    TourismFron = Tourism.objects.get(id=id)

    if TourismFron.Tourism_TuiWen:
        Tourism_TuiWen_YN = "是"
    else:
        Tourism_TuiWen_YN = "否"
    if request.method=="POST":
        # image, Tourism_name, Tourism_city, Tourism_Price, Tourism_Number, total_views, phone, Tourism_TuiWen, Tourism_by_Region_id
        try:
            file = request.FILES.get('picture', None)
            if file:
                fileDB = "./static/image/" + str(file)
                fname = settings.IMAGE_ROOT + '\\' + file.name
                print(fname, fileDB)
                with open(fname, 'wb') as pic:
                    for c in file.chunks():
                        pic.write(c)
            Tourism_name  = request.POST.get('Tourism_name')
            Tourism_city = request.POST.get('Tourism_city')
            Tourism_Price = request.POST.get('Tourism_Price')
            Tourism_Number = request.POST.get('Tourism_Number')
            phone = request.POST.get('phone')
            Tourism_TuiWen = request.POST.get('Tourism_TuiWen')
            Tourism_by_Region_id = request.POST.get('Tourism_by_Region_id')
            Tourism_by_Region = Region.objects.get(Region_city__contains=Tourism_by_Region_id)
            TourismFron.image = fileDB
            TourismFron.Tourism_name = Tourism_name
            TourismFron.Tourism_city = Tourism_city
            TourismFron.Tourism_Price = Tourism_Price
            TourismFron.Tourism_Number = Tourism_Number
            TourismFron.phone = phone
            TourismFron.Tourism_TuiWen = Tourism_TuiWen
            TourismFron.Tourism_by_Region_id = Tourism_by_Region.id

            TourismFron.save()
        except:
            message = "输入数据不能为空，或者格式不对！"

    return render(request, 'Tourism_Update.html', locals())
def Tourism_Add(request):
    if request.method == "POST":
        image = request.POST.get('image')
        file = request.FILES.get('picture', None)
        if file:
            fileDB = "./static/image/" + str(file)
            fname = settings.IMAGE_ROOT + '\\' + file.name
            print(fname,fileDB)
            with open(fname, 'wb') as pic:
                for c in file.chunks():
                    pic.write(c)

        Tourism_name = request.POST.get('Tourism_name')
        Tourism_city = request.POST.get('Tourism_city')
        Tourism_Price = request.POST.get('Tourism_Price')
        Tourism_Number = request.POST.get('Tourism_Number')
        phone = request.POST.get('phone')
        Tourism_TuiWen = request.POST.get('Tourism_TuiWen')
        Tourism_by_Region_id = request.POST.get('Tourism_by_Region_id')
        for x in Tourism.objects.filter():
            if x.Tourism_name == Tourism_name:
                message = "旅游景点名字已经存在，请不要重覆添加！"
                return render(request,'Tourism_Add.html',locals())
        Tourism_by_Region = Region.objects.get(Region_city__contains=Tourism_by_Region_id)
        Tourism_Add_ = Tourism.objects.create(image=fileDB,Tourism_name=Tourism_name,Tourism_city=Tourism_city,Tourism_Price=Tourism_Price,Tourism_Number=Tourism_Number,phone=phone,Tourism_TuiWen=Tourism_TuiWen,Tourism_by_Region_id=Tourism_by_Region.id)
        return redirect('/Admin_Tourism/1')

    return render(request,'Tourism_Add.html',locals())
def Admin_car(request,id):
    car_admin = car.objects.filter()
    paginator2 = Paginator(car_admin, 6)
    car_admin_page = paginator2.get_page(id)
    qian = car_admin_page.number - 1
    hou = car_admin_page.number + 1
    return render(request,'car.html',locals())

def Admin_meishi(request,id):
    if id == 1:
        title = '海南特色'
        meishi = HaiNan_chwl.objects.filter(category__contains="海南特色")
    if id == 2:
        title = "海南特产"
        meishi = HaiNan_chwl.objects.filter(category__contains="海南特产")
    if id == 3:
        title = "海南小吃"
        meishi = HaiNan_chwl.objects.filter(category__contains="海南小吃")
    if id == 4:
        title = "海南招牌小吃"
        meishi = HaiNan_chwl.objects.filter(category__contains="海南招牌小吃")
    if request.method =="GET":
        page = request.GET.get('page')
        paginator2 = Paginator(meishi, 9)
        meishi_page = paginator2.get_page(page)
        qian = meishi_page.number - 1
        hou = meishi_page.number + 1
        qian2 = meishi_page.number - 2
        hou2 = meishi_page.number + 2
    else:
        # page = request.GET.get('page')
        paginator2 = Paginator(meishi, 9)
        meishi_page = paginator2.get_page(1)
        qian = meishi_page.number - 1
        hou = meishi_page.number + 1
        qian2 = meishi_page.number - 2
        hou2 = meishi_page.number + 2


    return  render(request, 'AdminMeishi.html', locals())

##============                     END            ===================##

##============                      美食                        ===================##

def meishi(request,id):
    if id == 1:
        title = '海南特色'
        meishi = HaiNan_chwl.objects.filter(category__contains="海南特色")
    if id == 2:
        title = "海南特产"
        meishi = HaiNan_chwl.objects.filter(category__contains="海南特产")
    if id == 3:
        title = "海南小吃"
        meishi = HaiNan_chwl.objects.filter(category__contains="海南小吃")
    if id == 4:
        title = "海南招牌小吃"
        meishi = HaiNan_chwl.objects.filter(category__contains="海南招牌小吃")
    if request.method =="GET":
        page = request.GET.get('page')
        paginator2 = Paginator(meishi, 12)
        meishi_page = paginator2.get_page(page)
        qian = meishi_page.number - 1
        hou = meishi_page.number + 1
        qian2 = meishi_page.number - 2
        hou2 = meishi_page.number + 2
    else:
        # page = request.GET.get('page')
        paginator2 = Paginator(meishi, 12)
        meishi_page = paginator2.get_page(1)
        qian = meishi_page.number - 1
        hou = meishi_page.number + 1
        qian2 = meishi_page.number - 2
        hou2 = meishi_page.number + 2

    return  render(request,'meishi.html',locals())
##============                     END            ===================##

##============                      美食                        ===================##

def Tourism_User(request,id):
    if request.user.id:
        if request.method == 'GET':
            User_id = get_object_or_404(User,id=request.user.id)
            User_Money = get_object_or_404(User_information,user_id_id=User_id.id)
            Tourism_money = Tourism.objects.get(id=id)
            if User_Money.money !=None and int(User_Money.money)>0:
                money = int(User_Money.money) - int(Tourism_money.Tourism_Price)
                if int(money) >= 0:
                    for x in Tourism_status.objects.all():
                        if x.Tourism_id == id and x.user_id==request.user.id:
                            return HttpResponse("当前你已经购买了！请不要重覆购买！")
                    x6 = Tourism_status.objects.create(user_id=request.user.id, order_number=get_order_code(), Tourism_id=id,status=1)

                    User_information.objects.filter(user_id_id=User_id.id).update(money=money)
                    # models.User.objects.filter(id=edit_id).update(name=username, password=password)
                    return redirect('/gerenziliao/')
            else:
                return HttpResponse("账户没有钱请你充值！")

        else:
            return HttpResponse("仅支持GET链接!")
    else:
        return HttpResponse("你还没有登录！")
##============                     END            ===================##




def get_order_code(): #生成订单号！
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
    return order_no

##============                      用户完善信息                        ===================##


# 总结：用__告诉orm，要连接那个表
#      一对一： 正向：按字段  反向：按表名小写
#      一对多：  正向：按字段  反向：按表名小写
#      多对多：  正向：按
#      字段  反向：按表名小写

def edit(request):
    if request.user.id:
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        autograph = request.POST.get('autograph')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        # sex1 = request.POST.get('sex1')
        # print(sex1)
        try:
            User_edit = User_information.objects.get(user_id=request.user.id)
            User_id =User_information.objects.get(user_id=request.user.id)
            if User_id.user_id_id==request.user.id:
                file = request.FILES.get('picture', None)
                if file:
                    fileDB = "media/" + str(file)
                    F = settings.MEDIA_ROOT + '\\' + file.name
                    with open(F, 'wb') as IOCN:
                        for c in file.chunks():
                            IOCN.write(c)
                            print("修改")
                            User_information.objects.filter(user_id_id=request.user.id).update(age=age, sex=sex,
                                                                                               autograph=autograph,
                                                                                               city=city, phone=phone,
                                                                                               iocn=fileDB,
                                                                                               user_id_id=request.user.id)
                            return redirect('/gerenziliao/')
        except:
            file = request.FILES.get('picture', None)
            if file:
                fileDB = "media/" + str(file)
                fname = settings.MEDIA_ROOT + '\\' + file.name
                print(fname)
                with open(fname, 'wb') as pic:
                    for c in file.chunks():
                        pic.write(c)
                        print("新增")
                        User_information.objects.create(age=age, sex=sex, autograph=autograph, phone=phone, city=city,iocn=fileDB, user_id_id=request.user.id)
                        return redirect('/gerenziliao/')

    return render(request, 'User_information.html', locals())
def gerenziliao(request):
    if request.user.id:
        try:
            User_edit = User_information.objects.get(user_id=request.user.id)
            Tourism_status_dingdan = Tourism_status.objects.filter(user_id=request.user.id)
            ArticlePost_page = ArticlePost.objects.filter(author_id=request.user.id)
            Comment_page = Comment.objects.filter(user_id=request.user.id)
            if User_edit.sex=='男':
                sex_pd=1
            elif User_edit.sex =="女":
                sex_pd=2
            else:
                sex_pd=3
            if User_edit.money == None:
                yue = 0
            else:
                yue = User_edit.money
        except:
            return render(request, 'User_information.html', locals())

    else:
        return render(request, 'login.html', locals())
    return render(request,'gerenziliao.html',locals())
def AddMony(request):
    if request.method == "POST":
        Money = request.POST['money']
        User_edit = User_information.objects.get(user_id=request.user.id)
        User_edit.money = Money
        User_edit.save()
        newmoney = User_edit.money
        if User_edit.money == Money:
            return redirect('/index/')
    return render(request,'AddMony.html',locals())



##============                               END            ===================##



##============                      文章                        ===================##


def Article_Add(request):
    if request.user.id:
        if request.method == "POST":
            title = request.POST['title']
            body = request.POST['body']
            ArticlePost.objects.create(title=title,boby=body,author_id=request.user.id)
            return redirect(f'/Article_List/{request.user.id}')
        else:
            return render(request, 'Article_Add.html', locals())
    else:
        return HttpResponse('请你登录网站！')
def Article_List(request,id):
    x = ['secondary','danger','warning']
    article = ArticlePost.objects.filter(author_id=id).order_by("-total_views")
    page = request.GET.get('page')
    paginator2 = Paginator(article, 3)
    article_page = paginator2.get_page(page)
    qian = article_page.number - 1
    hou = article_page.number + 1
    qian2 = article_page.number - 2
    hou2 = article_page.number + 2
    zipArticle = zip(x,article_page)
    return render(request, 'Article_List.html', locals())
def Article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    return render(request,'Article_Detail.html',locals())





##============                          END            ===================##

##============                      旅游全套                         ===================##










##============                      旅游全套          END            ===================##



##============                      租车全套                         ===================##










##============                      租车全套          END            ===================##


