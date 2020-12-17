from django.db import models


class Project(models.Model):
    """
    42Cursus 프로젝트에 관한 클래스
    :name: 프로젝트의 이름, pk
    :recommend_day: 인트라에서 추천하는 소요 기간
    """
    name = models.CharField(max_length=25, primary_key=True)
    recommend_day = models.IntegerField(null=False)
