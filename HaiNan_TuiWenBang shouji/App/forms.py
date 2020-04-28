from django import forms
from .views import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
class AdminFrom(forms.Form):
    AdminUsername = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"请输入管理账号"}))
    AdminPassword = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"请输入管理密码"}))
