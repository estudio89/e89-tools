# -*- coding: utf-8 -*-
from django.db import models
import sys

class KeyValueStore(models.Model):
	''' Classe para armazenamento de pares [key,value].
		Cada key precisa ser único.'''

	key = models.CharField(unique=True,max_length=255)
	value = models.TextField()

	def __unicode__(self):
		return '%s: %s'%(self.key,self.value)

	@staticmethod
	def get_value(key,default=None):
		''' Busca um valor salvo. Caso o mesmo não exista,
			ele é criado com valor igual ao argumento "default"
			e o valor "default" é retornado.'''
		try:
			return KeyValueStore.objects.get(key=key).value
		except KeyValueStore.DoesNotExist:
			KeyValueStore.set_value(key, default)
			return default

	@staticmethod
	def get_int(key,default=None):
		''' Busca um valor no banco e converte-o para um inteiro.'''

		return int(KeyValueStore.get_value(key,default))

	@staticmethod
	def get_list(key,default=None):
		''' Busca um valor no banco e converte-o para uma lista.'''
		val = KeyValueStore.get_value(key,default)
		if (type(val) == type('') or (type(val) == type(u''))):
			return eval(val)
		else:
			return val

	@staticmethod
	def set_value(key,value):
		''' Armazena um valor no banco, ou atualiza-o caso já exista.'''
		value = str(value)
		if KeyValueStore.objects.filter(key=key).exists():
			pair = KeyValueStore.objects.get(key=key)
			pair.value = value
		else:
			pair = KeyValueStore(key=key,value=value)
		pair.save()
