from django.test import TestCase
from .models import *
from django.db import models
from .apis import *
from django.utils.translation import gettext_lazy as _

def register_proj(clients, proj: Project):
    for usr in clients:
        Client.objects.filter(intraId=usr.intraId).update(project=proj)


def print_userinfo():
    client_list = Client.objects.all()
    print("id           project         team            status")
    for client in client_list:
        proj = Client.objects.filter(intraId=client.intraId)[0].project
        team = Client.objects.filter(intraId=client.intraId)[0].team
        if proj is not None:
            proj = proj.name
        if team is not None:
            team = team.id
        print(client.intraId + '         ' + str(proj) + '        ' + str(team)+'       '+str(client.status))
    print(len(client_list))


def ff():
    for i in range(12):
        Client.objects.create(intraId=str(i), status=Client.Status.NONE)
    register_proj(Client.objects.all()[:4], Project.objects.filter(name="gnl")[0])
    register_proj(Client.objects.all()[4:8], Project.objects.filter(name="libft")[0])
    register_proj(Client.objects.all()[8:], Project.objects.filter(name="ft_printf")[0])
    team_match()
    Team.objects.all().update(exitVoteList="1111")
    print_userinfo()

    for i in Team.objects.all():
        team_exit(i)
    print_userinfo()

# Create your tests here.
