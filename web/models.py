# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# =======================================================

class Engine(models.Model):
	slug = models.SlugField()
	title = models.CharField('Название', max_length=200)
	
	def __unicode__(self):
		return self.title

# =======================================================

class Map(models.Model):
	title = models.CharField('Название', max_length=200)
	engine = models.ForeignKey(Engine, related_name='maps', verbose_name='Движок')
	width = models.IntegerField('Ширина')
	height = models.IntegerField('Высота')
	textMap = models.TextField('Текстовая карта')

# =======================================================

LANG_TYPE_V = (
	(1, 'Интерпретируемый'),
	(2, 'Компилируемый'),
	)

class Language(models.Model):
	slug = models.SlugField()
	title = models.CharField('Название', max_length=200)
	type = models.SmallIntegerField('Тип', choices=LANG_TYPE_V)
	compile = models.BooleanField('Компиляция')
	compiler = models.CharField('Компилятор', max_length=200, blank=1)
	option = models.CharField('Опции', max_length=100, blank=1)

	def __unicode__(self):
		return self.title

# =======================================================

class Bot(models.Model):
	owner = models.ForeignKey(User, related_name='bots', verbose_name='Владелец')
	title = models.CharField('Название', max_length=200)
	engine = models.ForeignKey(Engine, related_name='bots', verbose_name='Движок')
	lang = models.ForeignKey(Language, related_name='bots', verbose_name='Язык')
	compiled = models.BooleanField('Откомпилирован', default=False)

	def __unicode__(self):
		return u'%s %s' % (self.title, self.lang.title)

	def source(self):
		return '/var/bla-bla-bla/%d.source' % self.id
	
	def exe(self):
		return '/var/bla-bla-bla/%d.source' % self.id

# =======================================================

BATTLE_TYPE_V = (
	(1, 'Поединок'),
	(2, 'Автоматический'),
	(3, 'Не помню'),
	)

BATTLE_STAGE_V = (
	(1, 'Не запущен'),
	(2, 'В очереди'),
	(3, 'В процессе'),
	(4, 'Закончен'),
	(5, 'Ошибка'),
	)

class Battle(models.Model):
	type = models.SmallIntegerField('Тип', choices=BATTLE_TYPE_V)
	engine = models.ForeignKey(Engine, related_name='battles', verbose_name='Движок')
	map = models.ForeignKey(Map, related_name='battles', verbose_name='Карта')
	bots = models.ManyToManyField(Bot, related_name='battles', verbose_name='Боты')
	stage = models.SmallIntegerField('Стадия', choices=BATTLE_STAGE_V)
	time = models.DateTimeField('Создание', auto_now_add=1)

# =======================================================

class Virtual(models.Model):
	IP = models.IPAddressField()
	username = models.CharField(max_length=50)
	compiler = models.BooleanField('Для компиляции')

# #######################################################

class EngineAdmin(admin.ModelAdmin):
	pass

class LanguageAdmin(admin.ModelAdmin):
	pass

class BotAdmin(admin.ModelAdmin):
	pass

class BattleAdmin(admin.ModelAdmin):
	pass

class VirtualAdmin(admin.ModelAdmin):
	pass

# =======================================================

admin.site.register(Engine, EngineAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Bot, BotAdmin)
admin.site.register(Battle, BattleAdmin)
admin.site.register(Virtual, VirtualAdmin)
