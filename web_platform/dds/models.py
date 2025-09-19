from django.db import models
from django.utils import timezone


class Status(models.Model):
    status_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Статус операции',
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статус'

    def __str__(self):
        return self.status_name


class Type(models.Model):
    type_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Тип операции',
    )

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Тип'

    def __str__(self):
        return self.type_name


class Category(models.Model):
    type = models.ForeignKey(
        to=Type,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип операции',
    )
    category_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категория'

    def __str__(self):
        return f'{self.category_name}'


class Subcategory(models.Model):
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория',
    )
    subcategory_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Подкатегория',
    )

    class Meta:
        verbose_name = 'Подкатегорию'
        verbose_name_plural = 'Подкатегория'

    def __str__(self):
        return self.subcategory_name


class CashFlow(models.Model):
    creation_date = models.DateField(
        default=timezone.now,
        editable=True,
        verbose_name='Дата создания',
    )
    status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        verbose_name='Статус операции',
        related_name='status_cash_flows'
    )
    type = models.ForeignKey(
        to=Type,
        on_delete=models.CASCADE,
        verbose_name='Тип операции',
        related_name='type_cash_flows'
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='category_cash_flows'
    )
    subcategory = models.ForeignKey(
        to=Subcategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
        related_name='subcategory_cash_flows'
    )
    amount = models.DecimalField(
        default=0.00,
        max_digits=30,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name='Сумма',
    )

    comment = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Комментарий'
    )

    class Meta:
        verbose_name = 'Движение денежных средств'
        verbose_name_plural = 'Движение денежных средств'


    def __str__(self):
        return f'Операция: {self.type} на сумму: {self.amount} от {self.creation_date}'
