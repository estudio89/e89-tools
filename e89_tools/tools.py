# -*- coding: utf-8 -*-
from __future__ import print_function
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models.query import QuerySet
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template import loader
from django.contrib.staticfiles import finders
from django.conf import settings
from dateutil import parser
from sys import getsizeof
import sys
import re
from itertools import chain
from collections import deque
from PIL import Image, ImageFilter
from email.MIMEImage import MIMEImage

try:
    from reprlib import repr
except ImportError:
    pass

import os,json,sys

def camelcase_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def print_console(msg):
    try:
        sys.stderr.write(msg + "\n")
    except UnicodeError:
        pass

def format_iso_date(date):
    date = date.isoformat()
    if date.endswith('+00:00'):
        date = date[:-6] + 'Z'
    return date

def dash_camelcase(value):
    components = value.split('-')
    return "".join(x.title() for x in components)

def camelcase_dash(value):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    return reduce(getattr, attr.split('__'), obj)

def date_to_string(val, local=False, format="%Y-%m-%d %H:%M:%S.%f %Z"):
    ''' Converte uma data (datetime) em uma string de acordo com o formato passado. Caso o parâmetro "local" seja
        True, é utilizado o horário local.'''

    if local:
        from django.utils import timezone
        val = timezone.localtime(val)
    return val.strftime(format)

def string_to_date(val):
    ''' Converte uma string para um objeto datetime. '''

    return parser.parse(val)

def send_email(user,subject,template,template_kwargs={},attachments=[],static_images=[],html=False):
    ''' Envia email para um ou mais recipientes.
        O parâmetro attachments deve ser uma lista de listas contendo: [[nome_arquivo, arquivo],...].
        O "arquivo", no caso, deve ser uma string, portanto, caso trate-se de um arquivo em disco
        (ou StringIO), deve ser passado "fobj.read()".
    '''

    # Montando parâmetros de envio
    from_email = settings.EMAIL_HOST_ADDRESS
    msg = loader.render_to_string(template,template_kwargs)
    if type(user) == type([]) or isinstance(user,QuerySet):
        recipients = [u.email for u in user]
    elif type(user) == type(''):
        recipients = [user]
    else:
        recipients = [user.email]

    if static_images or html:
        mail = EmailMultiAlternatives(subject=subject,body=msg,from_email=from_email,bcc=recipients)
        mail.attach_alternative(msg, "text/html")
        mail.mixed_subtype = 'related'

        for static_img in static_images:
            path = finders.find(static_img.replace('/static/',''))

            fobj = open(path,'rb')
            msg_img = MIMEImage(fobj.read())
            fobj.close()
            msg_img.add_header('Content-ID','<{}>'.format(static_img))
            mail.attach(msg_img)
    else:
        mail = EmailMessage(subject=subject,body=msg,from_email=from_email,bcc=recipients)

    # Adicionando anexos
    for nome_arquivo, arquivo in attachments:
        mail.attach(nome_arquivo, arquivo)

    if getattr(settings, 'TOOLS_REPLY_TO',None):
        mail.extra_headers['Reply-To'] = settings.TOOLS_REPLY_TO

    mail.send(fail_silently=True)

    #print >>sys.stderr, 'Email enviado para %s'%(user.email)


def concatenar_valores(objetos, sep=None):
    ''' Concatena uma lista de strings separando-as por vírgula e incluindo um "e" antes do último item.

        Ex: concatenar_valores(['pera','maçã','uva']) >>  'pera, maçã e uva' '''

    if not objetos:
        return ''

    for idx,obj in enumerate(objetos):
        if obj.isupper():
            objetos[idx] = obj.lower()
    string = objetos[0]

    if len(objetos) > 1:
        string += ', ' if not sep else sep
        for obj in objetos[1:-1]:
            string += obj if not sep else obj
            string += ", " if not sep else sep
        string = string[:len(string) - 2] if not sep else string[:len(string) - len(sep)]
        string += ' e ' if not sep else sep
        string += objetos[-1]

    string = string[0].upper() + string[1::]
    return string


def zip_directory(zobj, path):
    import os
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            zobj.write(file_path,arcname=os.path.relpath(file_path, path))

from functools import wraps