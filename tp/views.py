from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .apis import *


def main(request):
    client = get_client(request)
    param = {}
    if client is None:
        param['user'] = None
        param['title'] = '로그인'
        param['link'] = "https://api.intra.42.fr/oauth/authorize?client_id" \
                        "=7dbf58940924b902ede1d036e96055852f2556f83841fa9883b10a6dcb3a9bdc&redirect_uri=http%3A%2F" \
                        "%2Flocalhost%3A8000%2Flogin%2F&response_type=code"
    else:
        param['user'] = client[0].intraId
        if client[0].team is not None:
            param['title'] = "팀정보"
            param['link'] = "/team_info/"
        else:
            if client[0].project is None:
                param['title'] = "플젝 신청"
                param['link'] = '/register_team/'
            else:
                param['title'] = "신청 수정"
                param['link'] = "/pending_team/"
    return render(request, 'main.html', param)


def login(request):
    if "code" in request.GET:
        code = request.GET["code"]
        if code is not None:
            token = code2token(code)
            if "error" in token:
                return HttpResponse(status=500)
            intra_id = token2user(token)
            if "error" in intra_id:
                return HttpResponse(status=500)
            user = Client.objects.filter(intraId=intra_id)
            if len(user) == 0:
                sign_in(intra_id)
            response = redirect('main')
            aes = AESCipher()
            set_cookie(response, "user_key", aes.encrypt_str(intra_id))
            return response
        return HttpResponseNotFound()
    return redirect('main')


@csrf_protect
def register_team(request):
    client = get_client(request)
    if client is None:
        return HttpResponse(status=403)
    if len(client) == 0:
        return HttpResponse(status=403)
    if client[0].status == Client.Status.WAITING:
        return redirect('pending_team')
    if client[0].status == Client.Status.MATCHED:
        return redirect('team_info')
    if request.method == "POST":
        project = request.POST["project"]
        project = Project.objects.filter(name=project)
        if len(project) == 0:
            return HttpResponse(status=400)
        project = project[0]
        register(client[0].intraId, project)
        return redirect('main')
    else:
        param = {'prjs': list(Project.objects.all())}
        return render(request, 'register_team.html', param)


@csrf_protect
def pending_team(request):
    client = get_client(request)
    if client is None:
        return HttpResponse(status=403)
    if client[0].status == Client.Status.NONE:
        return redirect('register_team')
    if client[0].status == Client.Status.MATCHED:
        return redirect('team_info')
    if request.method == "POST":
        project = request.POST["project"]
        project = Project.objects.filter(name=project)
        if len(project) == 0:
            return HttpResponse(status=400)
        project = project[0]
        register(client[0].intraId, project)
        return redirect('main')
    else:
        sel = client[0].project
        param = {'prjs': list(Project.objects.all()), "sel": sel.name}
        return render(request, 'pending_team.html', param)


@csrf_protect
def team_info(request):
    client = get_client(request)
    if client is None:
        return HttpResponse(status=403)
    if client[0].status != Client.Status.MATCHED:
        return HttpResponse(status=403)
    if request.method == "POST":
        voteExit(client[0].intraId)
        return redirect('team_info')
    else:
        team = Team.objects.filter(id=client[0].team.id)[0]
        param = {
            'project': team.project.name,
            'team_list': team.userList.split(","),
            'due_date': team.dueDate
        }
        return render(request, 'team_info.html', param)


def logout(request):
    response = redirect('main')
    sign_out(response)
    return response
