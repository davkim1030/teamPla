import base64
import hashlib

import requests
from Crypto import Random
from Crypto.Cipher import AES
from django.conf import settings

from .models import *
import datetime

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
        #if user_nb == 1:
        #    team
        while user_nb != 4 and user_nb > 3:
            member_list = list()
            for i in range(3):
                member_list.append(team_list.pop())
            Team.objects.create(userList=','.join(member_list), exitVoteList="000",
                                project=prj, dueDate=datetime.date.today().strftime("%Y%m%d"))
            user_nb -= 3
        if len(team_list) == 4:
            Team.objects.create(userList=','.join(team_list), exitVoteList="0000",
                                project=prj, dueDate=datetime.date.today().strftime("%Y%m%d"))
        if len(team_list) == 2:
            Team.objects.create(userList=','.join(team_list), exitVoteList="00",
                                project=prj, dueDate=datetime.date.today().strftime("%Y%m%d"))
        del team_list


def code2token(code):
    url = "https://api.intra.42.fr/oauth/token"
    param = {
        "grant_type": "authorization_code",
        "client_id": "7dbf58940924b902ede1d036e96055852f2556f83841fa9883b10a6dcb3a9bdc",
        "client_secret": "04c11b160f57c5a3d9927146a801e860ece6679499ca44f2048e3dd050777799",
        "code": code,
        "redirect_uri": "http://localhost:8000/login/"
    }
    r = requests.post(url, param)
    data = r.json()
    if "access_token" in data:
        return data["access_token"]
    if "error" in data:
        return "error" + data["error"]
    return "Unknown error"


def token2user(token):
    url = "https://api.intra.42.fr/v2/me"
    headers = {
        "Authorization": "Bearer " + token
    }
    r = requests.get(url=url, headers=headers)
    data = r.json()
    if "login" in data:
        return data["login"]
    if "error" in data:
        return "error" + data["error"]
    return "Unknown error"


class AESCipher:
    """
    AES(CBC) 암호화를 구현한 클래스
    """
    key = bytes()       # 키값을 저장할 클래스 변수

    def __init__(self):
        """
        생성자
        인스턴스 변수들의 값을 초기화해준다
        """
        self.key = hashlib.sha256('TeamPlaKimKimMin'[:16].encode("utf-8")).digest()     # 암복호화 키값 16자리를 맞춰야함
        self.BS = 16                                                                        # 블록 사이즈
        self.pad = lambda s: s + (self.BS - len(s.encode('utf-8')) % self.BS) * '-'         # 패딩
        self.unpad = lambda s: s[:ord(s[len(s) - 1:])]

    def __encrypt__(self, raw):
        """
        암호화 메소드수 내부 함
        :param raw:     bytes, 암호화할 평문 바이트 시퀀스
        :return:        bytes, 암호화된 암호문 바이트 시퀀스
        """
        raw = self.pad(raw)                             # 평문에 패딩 추가
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)    # CBC모드로 암호화
        return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))   # 암호문을 utf-8로 인코딩하고 base64로 인코딩함

    def __decrypt__(self, enc):
        """
        복호화 메소드 내부 함
        :param enc:     bytes, 복호화할 암호문 바이트 시퀀스
        :return:        bytes, 복호화한 평문 바이트 시퀀스
        """
        enc = base64.b64decode(enc)                     # base64 디코드
        iv = enc[:16]                                   # 초기 벡터 추출
        cipher = AES.new(self.key, AES.MODE_CBC, iv)    # 복호화
        return self.unpad(cipher.decrypt(enc[16:]))     # 복호화 결과 패딩 제거하고 리턴

    def encrypt_str(self, raw):
        """
        암호화 메소드
        :param raw:     str, 암호화할 평문 문자열
        :return:        str, 암호화된 암호문 문자열
        """
        return self.__encrypt__(raw).decode("utf-8")

    def decrypt_str(self, enc):
        """
        복호화 메소드
        :param enc:     str, 복호화할 암호문 문자열
        :return:        str, 보호화된 평문 문자열
        """
        return self.__decrypt__(enc).decode("utf-8").replace('-', '')


def set_cookie(response, key, value, sec=1200):
    if sec is None:
        max_age = 20 * 12
    else:
        max_age = sec
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )


def add_user_key_cookie(response, intra_id):
    aes = AESCipher()
    set_cookie(response, "user_key", aes.encrypt_str(intra_id))


def sign_in(intra_id):
    Client.objects.create(intraId=intra_id, status=Client.Status.NONE)


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
    user: Client = Client.objects.get(intraId=intraId)
    if user.team is not None:
        return True
    else:
        return False


def is_project_applied(intraId: str):
    user: Client = Client.objects.get(intraId=intraId)
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
