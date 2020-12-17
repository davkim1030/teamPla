from django.test import TestCase
from .models import *
from django.db import models
from django.utils.translation import gettext_lazy as _

def register_proj(clients, proj: Project):
    for usr in clients:
        Client.objects.filter(intraId=usr.intraId).update(project=proj)


def print_userinfo():
    client_list = Client.objects.all()
    print("id           project         team")
    for client in client_list:
        proj = Client.objects.filter(intraId=client.intraId)[0].project
        team = Client.objects.filter(intraId=client.intraId)[0].team
        if proj is not None:
            proj = proj.name
        if team is not None:
            team = team.id
        print(client.intraId + '         ' + str(proj) + '        ' + str(team))
    print(len(client_list))




# Create your tests here.
