from django.db import models
from entmt_info.models import Movies, Series, Genres
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings


class Members(AbstractUser):
    u_mobile = models.CharField(max_length=20)    # 전화번호
    u_image = models.ImageField(default='default.jpg',
                                upload_to=settings.MEDIA_ROOT,
                                blank=True,
                                null=True)    # 프로필 이미지


class Mlike(models.Model):
    ml_member = models.ForeignKey(Members,
                              on_delete=models.CASCADE)
    ml_movie = models.ForeignKey(Movies,
                              on_delete=models.CASCADE)
    def __str__(self):
        return str(self.ml_member) + ' + ' + str(self.ml_movie)

# class Mlike(models.Model):
#     ml_member = models.ForeignKey(Members,
#                               on_delete=models.CASCADE)
#     ml_movie = models.IntegerField()

class Slike(models.Model):
    sl_member = models.ForeignKey(Members,
                              on_delete=models.CASCADE)
    sl_series = models.ForeignKey(Series,
                              on_delete=models.CASCADE)


class Ugenres(models.Model):
    ug_member = models.ForeignKey(Members,
                              on_delete=models.CASCADE)
    ug_genre = models.ForeignKey(Genres,
                              on_delete=models.CASCADE)
    def __str__(self):
        return self.ug_genre.g_name
