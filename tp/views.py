from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .apis import *


def main(request):
    return render(request, 'main.html')


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


def register_team(request):
    request.META['Bearer'] = "298a9ead836455ebcfd8dcc75c7872117532d055fbfb460580052d67c6f06dea"
    return redirect("https://api.intra.42.fr/v2/users/hyukim")


def pending_team(request):
    return render(request, 'pending_team.html')


def team_info(request):
    return render(request, 'team_info.html')

