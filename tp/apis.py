from .models import *
from datetime import datetime
import random


def team_exit(team: Team):
    if "0" not in team.exitVoteList:
        target_list = Team.objects.filter(id=team.id)
        user_list = target_list[0].userList.split(',')
        for user_id in user_list:
            Client.objects.filter(intraId=user_id).update(project=None)
        target_list.delete()


def team_match():
    for prj in Project.objects.all():
        team_list = list()
        for usr in Client.objects.all():
            if prj.name == usr.project.name:
                team_list.append(usr.intraId)
        random.shuffle(team_list)
        user_nb = len(team_list)
        while user_nb != 4 and user_nb > 0:
            member_list = list()
            for i in range(3):
                member_list.append(team_list.pop())
            Team.objects.create(userList=','.join(member_list), exitVote="0000", project=prj, dueDate=datetime.date.today().strftime("%Y%m%d"))
            user_nb -= 3
        if len(team_list):
            Team.objects.create(userList=','.join(team_list), exitVote="0000", project=prj, dueDate=datetime.date.today().strftime("%Y%m%d"))
        del team_list

