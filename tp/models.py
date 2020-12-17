from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """
    42Cursus 프로젝트에 관한 클래스
    :name: 프로젝트의 이름, pk
    :recommend_day: 인트라에서 추천하는 소요 기간
    """
    name = models.CharField(max_length=25, primary_key=True)
    recommend_day = models.IntegerField(null=False)


class Team(models.Model):
    """
    42 매칭되는 팀에 관한 class
    id : Team의 key value
    project : team이 진행중인 project
    duedate : team의 project 완료일자
    startDate : team이 project를 시작한 날짜
    """
    id = models.AutoField(primary_key=True)
    userList = models.CharField(max_length=50, null=False)
    exitVoteList = models.CharField(max_length=4, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    dueDate = models.DateField(null=False)


class Client(models.Model):
    """
    서비스 사용자에 관한 클래스
    :intraId 유저의 로그인 Id
    :team 테이블의 외래키
    :status 유저의 팀 매칭 상태
    :project 푸로제트 관련 정보
    """
    class Status(models.TextChoices):
        NONE = "NONE", _("None")
        WAITING = "WAITING", _("Waiting")
        MATCHED = "MATCHED", _("Matched")
        FAIL = "FAIL", _("Fail")
    intraId = models.CharField(max_length=10, primary_key=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    auth = models.CharField(max_length=7, choices=Status.choices)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
