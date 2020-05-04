# ----------------------用户中心管理视图-------------------------#
from django.http import JsonResponse
from django.shortcuts import render
from blog import models

def userManager(request):
    print("-------------------------------------")
    return render(request,"backend/user_manage.html")

def edit_userProfile(request):
    ret = {"status": 0, "msg":"保存成功"}
    user = request.user
    new_profile = request.POST.get("new_profile")
    try:
        models.UserInfo.objects.filter(nid=user.pk).update(profile=new_profile)
    except Exception as e:
        print(e)
        ret["status"]=1
        ret["msg"]="保存失败"
    return JsonResponse(ret)
# ----------------------！用户中心管理视图-------------------------#