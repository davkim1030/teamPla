from .models import *
from datetime import datetime
import random


def team_exit(team: Team):
    if "0" not in team.exitVote:
        target_list = Team.objects.filter(id=team.id)
    user_list = target_list[0].userList.split(seq=',')
    for user_id in user_list:
        users = User.objects.filter(intraId=user_id)
        for user in users:
            user.objects.update(Project=None)
    Team.objects.delete(id=target_list[0].id)


def team_match():
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
            Team.objects.create(userList=','.join(member_list), exitVote="0000", project=prj,
                                dueDate=datetime.date.today().strftime("%Y%m%d"))
            user_nb -= 3
        if len(team_list):
            Team.objects.create(userList=','.join(team_list), exitVote="0000", project=prj,
                                dueDate=datetime.date.today().strftime("%Y%m%d"))
        del team_list


"""
42api 권환 획득
42api 사용법을 알아야한다.
"""


def login():
    pass


"""
팀이 등록되었는지 확인
"""


def is_team_matched(intraId: str):
    user: User = User.objects.get(intraId=intraId)
    if user.team is not None:
        return True
    else:
        return False

def is_project_applied(intraId: str):
    user: User = User.objects.get(intraId=intraId)
    if user.project is not None:
        return True
    else:
        return False

"""
팀 매칭 신청 (프로젝트 등록)
"""


def reister(project_name: str):
    # 프로젝트의 기간 정보 들고오기
    project: Project = Project.objects.get(project_name)

    pass


"""
과제종료 신청
"""


def voteExit(intraId: str):
    team: Team = Team.objects.get(intraId=intraId)
    user_list_str: str = team.userList
    user_list_list = user_list_str.split()
    exit_vote_str = team.exitVote
    index: int = user_list_list.index(intraId)
    if exit_vote_str[index] == '0':
        exit_vote_str = exit_vote_str[0:index] + '1' + exit_vote_str[index:]
        if exit_vote_str == "111":
            team_exit(team)
    else:
        print("hello")


"""
로그아웃
"""


def logout():
    pass
