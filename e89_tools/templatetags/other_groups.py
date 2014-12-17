# -*- coding: utf-8 -*-
import re,sys,json
import accounts.account_utils
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import get_model
from django.contrib.auth.models import Group

register = template.Library()

register.simple_tag(accounts.account_utils.other_groups)