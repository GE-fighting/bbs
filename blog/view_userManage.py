# ----------------------用户中心管理视图-------------------------#
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from blog import models
from django.contrib import auth
import json
import random
from untils.testRedis import getCode


def userManager(request):
    return render(request, "backend/user_manage.html")


def edit_userProfile(request):
    ret = {"status": 0, "msg": "保存成功"}
    user = request.user
    new_profile = request.POST.get("new_profile")
    try:
        models.UserInfo.objects.filter(nid=user.pk).update(profile=new_profile)
    except Exception as e:
        print(e)
        ret["status"] = 1
        ret["msg"] = "保存失败"
    return JsonResponse(ret)


def edit_pwd(request):
    ret = {"status": 0, "msg": "密码重置成功"}
    old_pwd = request.POST.get("old_pwd")
    new_pwd = request.POST.get("new_pwd")
    user = request.user
    if user.check_password(old_pwd):
        user.set_password(new_pwd)
        user.save()
    else:
        ret["status"] = 1
        ret["msg"] = "原密码错误，请重新填写"
    return JsonResponse(ret)


def found_pwd(request):
    ret={"status":0,"msg":"密码找回成功"}
    if request.method == "GET":
        return render(request, "foundPwd.html")
    else:
        phone=request.POST.get("phone")
        code=request.POST.get("code")
        codeKey = "phone:" + phone
        if getCode(codeKey) != code:
            ret["status"]=1
            ret["msg"]="验证码错误，请再次尝试"
            return JsonResponse(ret)
        else:
            user_obj=models.UserInfo.objects.filter(phone=phone).first()
            strCode = ""
            for i in range(0, 6):
                strCode = strCode + str(random.randint(0, 9))
            user_obj.set_password(strCode)
            user_obj.save()
            ret["msg"]="您的密码已重置为"+strCode
            return JsonResponse(ret)

def rem_user(request):
    ret = {"status": 0, "msg": "记住密码成功"}
    username = request.POST.get("username")
    password = request.POST.get("password")
    saveFlag = request.POST.get("saveFlag")
    user = auth.authenticate(username=username, password=password)
    response = HttpResponse()
    if user:
        if saveFlag == "true":
            response.set_signed_cookie('login', username + ',' + password, salt='hello', max_age=24 * 3600 * 7)
            response.content = json.dumps(ret)
            return response
        else:
            ret["status"] = 1
            ret["msg"] = "不记住密码成功"
            print(type(ret))
            print(type(json.dumps(ret)))
            response.content = json.dumps(ret)
            response.delete_cookie("login")
            return response
    else:
        if saveFlag == "true":
            ret["status"] = 2
            ret["msg"] = "用户名或密码错误，不建议保存密码"
            response.content = json.dumps(ret)
            response.delete_cookie("login")
            return response
        else:
            ret["status"] = 3
            ret["msg"] = "用户名或密码不正确，也未保存密码"
            response.content = json.dumps(ret)
            response.delete_cookie("login")
            return response

# ----------------------！用户中心管理视图-------------------------#
