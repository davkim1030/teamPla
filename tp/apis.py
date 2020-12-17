from models import *

import random

def team_update(team: Team, **kwargs):
    for var, value in kwargs:
        team.var = value


def team_exit(team: Team):
    if 0 not in team.exitVote:
        Team.objects.filter.team.id()

def team_match(self):
    for prj in Project.objects.all():
        team_list = list()
        for usr in User.objects.all():
            if prj.name == usr.project.name:
                team_list.append(usr.intraId)
        random.shuffle(team_list)
        user_nb = len(team_list)
        while user_nb != 4 and user_nb > 0:
            member_list = list()
            for i in range(3):
                member_list.append(team_list.pop())
            Team.objects.create(userList = ','.join(member_list), exitVote = "0000")
            user_nb -= 3
        if len(team_list):
            Team.objects.create(userList = ','.join(team_list), exitVote = "0000", )
        del team_list




    User.object.filter(Project = 프로젝트명)
    팀생성 방법
    :Team.object.create(id = , userList= ,exitVote,project,dueDate,startDate)
    User.object.update(Project=None)


"""
42api 권환 획득
42api 사용법을 알아야한다.
"""
def login():

	pass

"""
팀이 등록되었는지 확인
"""
def isteamMatched():

	pass
"""
팀 매칭 신청 (프로젝트 등록)
"""
def reister(project):
    #프로젝트의 기기간 정보 들고오기

	pass

"""
과제종료
team의 exitVote에 1추가ㅁㅁㄴㅁㄴ
"""
def voteExit(intraId):
    team = Team.objects.get(intraId = intraId)
    userList_str = team.userList
    voteExit()
    userList_list = userList_str.split()
    intraId_list.index(intraId)

    pass

"""
로그아웃
"""
def logout():
	pass

