'''
bbs用到的form类
'''

from django import forms
from django.core.exceptions import ValidationError
from blog import models
import re
from untils.testRedis import getCode


# 定义一个form类
class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="用户名",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control', "id": "id-username"}),
        error_messages={
            "max_length": "用户名最长16位",
            "required": "用户名不能为空"
        }
    )
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control', "id": "id-password"}, render_value=True),
        error_messages={
            "min_length": "密码最少6位",
            "required": "密码不能为空"
        }
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control', "id": "id-re_password"}, render_value=True),
        error_messages={
            "min_length": "密码最少6位",
            "required": "确认密码不能为空"
        }
    )
    email = forms.EmailField(
        label="邮箱",
        widget=forms.widgets.EmailInput(attrs={'class': 'form-control', "id": "id-email"}),
        error_messages={
            "invalid": "邮箱格式不正确",
            "required": "邮箱不能为空"
        }
    )
    phone = forms.CharField(
        label="手机号",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control', "id": "id-phone"}),
        error_messages={
            "required": "手机号不能为空"
        }
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control', "id": "id-code"}),
        error_messages={
            "required": "验证码不能为空"
        }
    )

    # 重写username字段的局部钩子
    def clean_username(self):
        username = self.cleaned_data.get("username")
        test_str = re.search(r"\W",username)
        print(test_str)
        is_exist = models.UserInfo.objects.filter(username=username)
        if test_str!=None:
            self.add_error("username", ValidationError("用户名格式错误！,不能包含特殊字符"))
        elif is_exist:
            self.add_error("username", ValidationError("该用户已存在！"))
        else:  # 不传返回值服务器会报错
            return username

    # 重写email字段的局部钩子
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            self.add_error("email", ValidationError("该邮箱已存在！"))
        else:
            return email

    # 重写username字段的局部钩子
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        ret = re.match(r"^1[35678]\d{9}$", phone)
        is_exist = models.UserInfo.objects.filter(phone=phone)
        if is_exist:
            self.add_error("phone", ValidationError("该手机号已存在"))
        if len(phone) != 11:
            self.add_error("phone", ValidationError("手机号位数错误"))
        elif not ret:
            self.add_error("phone", ValidationError("手机号格式错误"))
        else:  # 不传返回值服务器会报错
            return phone

    def clean_code(self):
        code = self.cleaned_data.get("code")
        phone = self.cleaned_data.get("phone")
        codeKey = "phone:" + phone
        print(codeKey)
        if getCode(codeKey) != code:
            self.add_error("code", ValidationError("验证码错误"))
        else:
            return code

    # 重写全局的钩子函数，对确认密码进行校验
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if re_password and password != re_password:
            self.add_error("re_password", ValidationError("两次密码不一致"))
        else:
            return self.cleaned_data
