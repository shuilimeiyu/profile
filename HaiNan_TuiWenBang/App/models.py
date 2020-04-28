from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.
##     管理员账号密码
class Administrators(models.Model):
    AdminUsername = models.CharField(max_length=128)
    AdminPassWord = models.CharField(max_length=128)

class ArticleColumn(models.Model):
    title = models.CharField(max_length=100,blank=True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title

class ArticlePost(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    boby = RichTextField()
    created = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


# 3，旅游特色模块：
# 旅游项目于管理：可以针对门票新增、编辑、修改，可以针对旅游项目进行更好的更新，以及帮助推文撰写者更好的接收到最新的数据。
# 旅游项目：展示每个地方的旅游项目，帮助推文撰写者更好的添加推文项目的引用。
# 地方特色：展示海南的各个地方的不同的特色食物，风土人情，帮助推文撰写者能更好的编写推文。

###             旅游特色              ###

class Region(models.Model):#城市地区名字  #三亚 海口  陵水
    Region_city = models.CharField(max_length=128,unique=True)
    Region_Code = models.CharField(max_length=48,unique=True)
    Region_introduce = models.TextField()
    class Meta:
        db_table = "Region"

class Tourism(models.Model):#各个地区旅游景点的详细介绍  三亚>>> ‘大东海’

    image = models.ImageField()
    Tourism_name = models.CharField(max_length=127)
    Tourism_city = models.CharField(max_length=127)
    Tourism_Price = models.CharField(max_length=255)
    Tourism_Number = models.CharField(max_length=128)
    Tourism_by_Region = models.ForeignKey('Region', on_delete=models.CASCADE)
    total_views = models.PositiveIntegerField(default=0)#点击量
    phone = models.CharField(max_length=22)
    yes_no = (('1', '有帮助'), ('0', '没帮助'))
    Tourism_TuiWen = models.IntegerField(yes_no)

    class Meta:
        db_table = "Tourism"

###--------旅游特色----END------------###


###             评论模块              ###


class Comment(models.Model):#评论模块，单体评论
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Tourism = models.ForeignKey(Tourism,on_delete=models.CASCADE)
    body = RichTextField()
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Comment"

class Comment_Article(models.Model):#评论模块，单体评论
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Tourism = models.ForeignKey(ArticlePost,on_delete=models.CASCADE)
    body = RichTextField()
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Comment_Article"

###             评论模块 end              ###



###             旅游门票购买模块              ###
class Tourism_status(models.Model):
    order_number = models.CharField(max_length=64)#订单号
    user = models.ForeignKey(User,on_delete=models.CASCADE)#哪位用户购买
    Tourism = models.ForeignKey(Tourism,on_delete=models.CASCADE)#那个旅游景点门票
    yes_no = (('1', '已购买'), ('0', '未购买'))
    status = models.IntegerField(yes_no,default=0)#购买的状态（0==没有购买，1==已经购买）
    class Meta:
        db_table = "Tourism_status"
###             旅游门票购买模块  end            ###


###             车辆信息模块              ###
class car(models.Model):

    car_number = models.CharField(max_length=100)#车牌号
    car_name = models.CharField(max_length=128)#车主的姓名
    car_color = models.CharField(max_length=128)#车子的颜色
    Vehicle_type = models.CharField(max_length=128)#车辆的类型：宝马，奔驰，大众 =====
    car_Price = models.CharField(max_length=20)#租车的费用
    car_Region = models.ForeignKey(Region,on_delete=models.CASCADE)#租车所在的地区
    total_views = models.PositiveIntegerField(default=0)#点击量
    car_hide = models.IntegerField(default=0)

    class Meta:
        db_table="car"
###             车辆信息模块    end          ###


###             车辆租赁模块              ###
class car_status(models.Model):
    order_number = models.CharField(max_length=64)#订单号
    user = models.ForeignKey(User,on_delete=models.CASCADE)#哪位用户租了
    car_status = models.ForeignKey(car,on_delete=models.CASCADE)#那个汽车
    yes_no = (('1', '已购买'), ('0', '未购买'))
    status = models.IntegerField(yes_no,default=0)#购买的状态（0==没有购买，1==已经购买）
    class Meta:
        db_table = "car_status"

###             车辆租赁模块  end             ###


class User_information(models.Model):

    age = models.IntegerField()
    boy_girl = (('boy', '男'), ('girl', '女'))
    sex = models.TextField(boy_girl)
    autograph = models.TextField()
    city = models.CharField(max_length=78)
    iocn = models.ImageField()
    phone = models.CharField(max_length=22)
    money = models.IntegerField(blank=True, null=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='User_information_set')
    class Meta:
        db_table = "User_information"
class weathe(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
class HaiNan_chwl(models.Model):

    name = models.CharField(max_length=128)
    jpg = models.ImageField()
    category = models.CharField(max_length=120)


