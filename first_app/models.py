from django.db import models
from django.utils import timezone
from datetime import timedelta

class Users(models.Model):
    first_name = models.CharField('Имя', max_length=80)
    last_name = models.CharField('Фамилия', max_length=60)
    phone_number = models.CharField('Номер телефона', max_length=20)
    email = models.EmailField('e-mail', max_length=100, unique=True)
    password_hash = models.CharField('Пароль', max_length=255)
    birth_date = models.DateField('Дата рождения')
    created_at = models.DateTimeField('Дата и время регистрации')
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta: 
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name"])
        ]

class Position(models.Model):
    POSITION_CHOICES = [
        ('operator', 'Оператор'),
        ('administrator', 'Администратор'),
        ('manager', 'Менеджер'),
        ('technician', 'Техник'),
    ]
    
    name = models.CharField('Название должности', max_length=50, choices=POSITION_CHOICES)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

class Staff(models.Model):
    first_name = models.CharField('Имя', max_length=80)
    last_name = models.CharField('Фамилия', max_length=60)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')
    phone_number = models.CharField('Номер телефона', max_length=20)
    passport = models.CharField('Паспорт', max_length=15, unique=True)
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name", "first_name"]

class Attractions(models.Model):
    MIN_HEIGHT_CHOICES = [
        (90, '90 см'),
        (100, '100 см'),
        (110, '110 см'),
        (120, '120 см'),
        (130, '130 см'),
        (140, '140 см'),
        (150, '150 см'),
    ]
    MAX_HEIGHT_CHOICES = [
        (140, '140 см'),
        (150, '150 см'),
        (160, '160 см'),
        (170, '170 см'),
        (180, '180 см'),
        (190, '190 см'),
        (200, '200 см'),
    ]
    MIN_AGE_CHOICES = [
        (3, '3 года'),
        (6, '6 лет'),
        (8, '8 лет'),
        (10, '10 лет'),
        (12, '12 лет'),
        (14, '14 лет'),
        (16, '16 лет'),
        (18, '18 лет'),
    ]
    CAPACITY_CHOICES = [
        (1, '1 человек'),
        (2, '2 человека'),
        (4, '4 человека'),
        (6, '6 человек'),
        (8, '8 человек'),
        (10, '10 человек'),
        (15, '15 человек'),
        (20, '20 человек'),
    ]
    DURATION_CHOICES = [
        (60, '1 минута'),
        (120, '2 минуты'),
        (180, '3 минуты'),
        (240, '4 минуты'),
        (300, '5 минут'),
        (420, '7 минут'),
        (600, '10 минут'),
        (900, '15 минут'),
    ]

    name = models.CharField('Название', max_length=100, unique=True)
    min_height = models.IntegerField('Минимальный рост (см)', choices=MIN_HEIGHT_CHOICES)
    max_height = models.IntegerField('Максимальный рост (см)', choices=MAX_HEIGHT_CHOICES)
    min_age = models.IntegerField('Минимальный возраст', choices=MIN_AGE_CHOICES)
    activity_status = models.BooleanField('Статус активности', default=True)
    capacity = models.IntegerField('Вместимость (чел)', choices=CAPACITY_CHOICES)
    duration_seconds = models.IntegerField('Продолжительность (сек)', choices=DURATION_CHOICES)
    
    def __str__(self):
        return self.name
    
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
        ('vip', 'VIP'),
        ('season', 'Сезонный'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField('Название', max_length=80, choices=NAME_CHOICES)
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
    
    def save(self, *args, **kwargs):
        # Автоматически рассчитывает valid_until на основе validity_duration из ticket_type
        if not self.valid_until and self.ticket_type:
            self.valid_until = timezone.now() + timedelta(days=self.ticket_type.validity_duration)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Билет #{self.id} - {self.user.last_name} {self.user.first_name}"
    
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