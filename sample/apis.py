from enum import Enum
from teamPla.models import User

intra_id
team
project

class Auth(Enum):
	USER = 1
	ADMIN = 2


def create(intra_id, team, auth):
	pass
	
def update(intra_id):
	pass

def read(String):
	User.object.all()
	pass

def delete(String):
	pass


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
	"""
	if (team.readbyUser(user) != None)

	"""

"""
팀 매칭 신청 (프로젝트 등록)
"""
def reister(protect):
	pass

"""
과제종료
team의 exitVote에 1추가
"""
def voteExit():
	team.exitVote.apand(1)

"""
로그아웃
"""
def logout():
	pass
