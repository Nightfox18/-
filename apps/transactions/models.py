from django.db import models
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories', verbose_name="Тип")
    
    class Meta:
        unique_together = ['name', 'type']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    
    def __str__(self):
        return f"{self.name} ({self.type.name})"

class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категория")
    
    class Meta:
        unique_together = ['name', 'category']
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Transaction(models.Model):
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма (руб.)")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
    
    def __str__(self):
        return f"{self.date} - {self.type} - {self.amount} руб."