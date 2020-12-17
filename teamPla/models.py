from enum import Enum
from django.db import models

class Auth(Enum):
	USER = 1
	ADMIN = 2

class Project(models.Model):
    """
    42Cursus 프로젝트에 관한 클래스
    :name: 프로젝트의 이름, pk
    :recommend_day: 인트라에서 추천하는 소요 기간
    """
    name = models.CharField(max_length=25, primary_key=True)
    recommend_day = models.IntegerField(null=False)

class Team(models.Model):
	pass


class User(models.Model):
	"""
    42Cursus 프로젝트에 관한 클래스
    :intraId 유저의 로그인 Id
    :team 테이블의 외래키
	:auth 유저의 권한
	:project 푸로제트 관련 정보
    """
	intraId = models.CharField(max_length=10, primary_key=True)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	auth = models.CharField(max_length=1, choices = Auth)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
