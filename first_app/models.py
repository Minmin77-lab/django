from django.db import models
from django.utils import timezone
from datetime import timedelta

class Users(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=20)
    surname = models.CharField('Фамилия', max_length=25)
    birth_date = models.DateField('Дата рождения')
    phone_number = models.CharField('Номер телефона', max_length=20)
    email = models.EmailField('e-mail', max_length=100, unique=True)
    password_hash = models.CharField('Пароль', max_length=255)
    created_at = models.DateTimeField('Дата и время регистрации')
    
    def __str__(self):
        return f"{self.surname} {self.name}"
    
    class Meta: 
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["surname", "name"]
        indexes = [
            models.Index(fields=["surname"])
        ]

class Staff(models.Model):
    POSITION_CHOICES = [
        ('operator', 'Оператор'),
        ('administrator', 'Администратор'),
    ]
    
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    position = models.CharField('Должность', max_length=50, choices=POSITION_CHOICES)  
    phone_number = models.CharField('Номер телефона', max_length=20)
    passport = models.CharField('Паспорт', max_length=13, unique=True)
    
    def __str__(self):
        return f"{self.name} {self.surname} - {self.get_position_display()}"
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["surname", "name"]
        indexes = [
            models.Index(fields=["position"])
        ]

class Attractions(models.Model):
    MIN_HEIGHT_CHOICES = [
        (90, '90 см'),
        (120, '120 см'),
        (150, '150 см'),
        (155, '155 см'), 
        (165, '165 см')       
    ]
    MAX_HEIGHT_CHOICES = [
        (120, '120 см'),
        (190, '190 см'),
        (165, '165 см')      
    ]
    MIN_AGE_CHOICES = [
        (3, '3 года'),
        (6, '6 лет'),
        (14, '14 лет'),
        (16, '16 лет'),
        (18, '18 лет')      
    ]
    CAPACITY_CHOICES = [
        (10, '10 человек'),
        (15, '15 человек'),
        (20, '20 человек')     
    ]
    DURATION_CHOICES = [
        (3, '3 минуты'),
        (6, '6 минут'),
        (10, '10 минут'),
        (8, '8 минут'),
        (15, '15 минут')      
    ]

    name = models.CharField('Название', max_length=100, unique=True)
    min_height = models.IntegerField('Минимальный рост (см)', choices=MIN_HEIGHT_CHOICES)
    max_height = models.IntegerField('Максимальный рост (см)', choices=MAX_HEIGHT_CHOICES)
    min_age = models.IntegerField('Минимальный возраст', choices=MIN_AGE_CHOICES)
    activity_status = models.BooleanField('Статус активности', default=True)
    capacity = models.IntegerField('Вместимость (чел)', choices=CAPACITY_CHOICES)
    duration_minutes = models.IntegerField('Продолжительность (мин)', choices=DURATION_CHOICES, default=5)  
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ответственный сотрудник')
    
    def __str__(self):
        staff_name = f" - {self.staff}" if self.staff else ""
        return f"{self.name}{staff_name}"
    
    class Meta:
        verbose_name = "Аттракцион"
        verbose_name_plural = "Аттракционы"
        ordering = ["name"]

class TicketTypes(models.Model):
    NAME_CHOICES = [
        ('child', 'Детский'),
        ('adult', 'Взрослый'),
        ('family', 'Семейный'),
        ('student', 'Студенческий'),
        ('other', 'Другое')  
    ]
    
    name = models.CharField('Название', max_length=50, choices=NAME_CHOICES)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    validity_duration = models.IntegerField('Срок действия (дни)', default=1)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = "Тип билета"
        verbose_name_plural = "Типы билетов"
        ordering = ["name"]

class Tickets(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    ticket_type = models.ForeignKey(TicketTypes, on_delete=models.CASCADE, verbose_name='Тип билета')
    purchase_date = models.DateTimeField('Дата покупки', auto_now_add=True)
    valid_until = models.DateTimeField('Действителен до')
    usage_time = models.DateTimeField('Время использования', null=True, blank=True)
    
    def __str__(self):
        return f"Билет #{self.id} - {self.user.surname} {self.user.name}"
    
    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        ordering = ["-purchase_date"]
        indexes = [
            models.Index(fields=["user", "ticket_type"]),
            models.Index(fields=["valid_until"]),
        ]

class SituationStage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
        ('delayed', 'Задержано'),
    ]
    
    attraction = models.ForeignKey(Attractions, on_delete=models.CASCADE, verbose_name='Аттракцион')
    start_time = models.DateTimeField('Время начала')
    end_time = models.DateTimeField('Время окончания', null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Сотрудник')
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE, verbose_name='Билет')
    actual_duration = models.IntegerField('Фактическая продолжительность (сек)', null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Сеанс #{self.id} - {self.attraction.name}"
    
    class Meta:
        verbose_name = "Сеанс аттракциона"
        verbose_name_plural = "Сеансы аттракционов"
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=["attraction", "start_time"]),
            models.Index(fields=["status"]),
        ]
