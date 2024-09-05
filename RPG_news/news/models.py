from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache
from django.contrib.postgres.fields import ArrayField
from django_resized import ResizedImageField


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default=User)

    Tank = 'TK'
    Hil = 'AR'
    DD = 'DD'
    Torgovci = 'TC'
    GildMaster = 'GD'
    CvestGiver = 'CG'
    Kuznec = 'KZ'
    Kojevnik = 'KJ'
    Zelevar = 'ZV'
    MasterZakinanii = 'MZ'
    CATEGORY_CHOICES = (
        (Tank, 'Танк'),
        (Hil, 'Хил'),
        (DD, 'ДД'),
        (Torgovci, 'Торговец'),
        (GildMaster, 'Гилдмастер'),
        (CvestGiver, 'Квестгивер'),
        (Kuznec, 'Кузнец'),
        (Kojevnik, 'Кожевник'),
        (Zelevar, 'Зельевар'),
        (MasterZakinanii, 'Мастер Заклинаний'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=Torgovci,
                                    verbose_name="Чей ты воин")
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата статьи')
    title = models.CharField(max_length=128, verbose_name="Поиск по названию статьи")
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    files = models.FileField(upload_to='uploads/', blank=True, verbose_name="Загрузи файл")

    def __str__(self):
        return self.title.title()

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = 'Публикации'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

class Comment(models.Model):
    author = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    message = models.ForeignKey(Post, unique=False, on_delete=models.CASCADE)
    text = models.TextField()
    dateComm = models.DateTimeField(auto_now_add=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}:{self.message}:{self.text[:10]}'

    def get_absolute_url(self):
        return reverse('Comments', args=[str(self.message.id)])
