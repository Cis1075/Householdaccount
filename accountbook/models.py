from django.db import models
from django.utils import timezone
from datetime import date


# カテゴリーデータベース
class Category(models.Model):
    objects = None

    class Meta:
        verbose_name = 'Category Table'
        verbose_name_plural = 'Categories Table'
        db_table = 'category'

    category_id = models.IntegerField()
    category = models.CharField(verbose_name='カテゴリ',max_length=100)
    flag = models.CharField(max_length=100)

    def __str__(self):
        return str(self.category)


# 家計簿データベース
class Account(models.Model):
    class Meta:
        verbose_name = 'Account Table'
        verbose_name_plural = 'Account Table'
        db_table = 'Household Account'

    category = models.ForeignKey(Category, verbose_name='カテゴリ名',
                                 default=None, null=None,
                                 on_delete=models.CASCADE)
    contents = models.CharField(verbose_name='項目', max_length=100, default='', blank=True, null=True)
    date = models.CharField(verbose_name='日付', max_length=100, default='', blank=True, null=True)
    amount = models.IntegerField(verbose_name='金額', null=False)

    def __str__(self):
        return '(' + str(self.category) + ',' + self.contents + ',' + self.date + ',' + str(self.amount) + ')'
