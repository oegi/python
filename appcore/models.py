# -*- coding: utf-8 -*-
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    role = models.ForeignKey('Role', verbose_name=_('Role'), on_delete=models.CASCADE, null=True, blank=True, )
    date_joined = models.DateTimeField(_('date created'), default=timezone.now)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    class Meta:
        db_table = 'user'
        verbose_name_plural = _('Users')
        verbose_name = _('User')


class Role(models.Model):
    name = models.CharField(_('Role'), max_length=50, unique=False, default="", )
    is_active = models.BooleanField(_('Active'), default=True, help_text=_('is active'), )
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        verbose_name_plural = _('Type of roles')
        verbose_name = _('Role')


class RoleMenu(models.Model):
    name = models.CharField(_('Name'), max_length=50, unique=False, default="", null=True, )
    role = models.ForeignKey('Role', verbose_name=_('Role'), on_delete=models.CASCADE, )
    menu = models.ForeignKey('Menu', verbose_name=_('Menu'), on_delete=models.CASCADE, )
    user = models.CharField(_('User'), max_length=50, unique=False, )
    is_active = models.BooleanField(_('Active'), default=True, help_text=_('is active'), )
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role_menu'
        verbose_name_plural = _('Profiles Menus')
        verbose_name = _('Profile Menu')


class RoleCategory(models.Model):
    name = models.CharField(_('Name'), max_length=50, unique=False, default="", )
    role = models.ForeignKey('Role', verbose_name=_('Role'), on_delete=models.CASCADE, )
    category = models.ForeignKey('Category', verbose_name=_('Category'), on_delete=models.CASCADE, )
    user = models.CharField(_('User'), max_length=50, unique=False, )
    is_active = models.BooleanField(_('Active'), default=True, help_text=_('is active'), )
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role_category'
        verbose_name_plural = _('Profiles Categories')
        verbose_name = _('Profile Category')


class Menu(models.Model):
    title = models.CharField(max_length=200)
    content_rich = models.TextField(blank=True, null=True)
    order_field = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'menu'
        verbose_name_plural = _('Menus')
        verbose_name = _('Menu')


class Category(models.Model):
    title = models.CharField(max_length=200)
    flag = models.BooleanField(null=True)
    is_active = models.BooleanField()
    url = models.CharField(max_length=300, blank=True, null=True)
    path_file = models.CharField(max_length=200, blank=True, null=True)
    content_rich = RichTextField(_('Answer'), null=True, blank=True)
    menu = models.ForeignKey(Menu, models.CASCADE)
    order_field = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        unique_together = ('title', 'menu',)
        verbose_name_plural = _('Categories')
        verbose_name = _('Category')


class Content(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField()
    description = RichTextField(_('Answer'), null=True)
    order_field = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Category', verbose_name=_('Categories'), on_delete=models.CASCADE, )
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(_('date update'), null=True, blank=True, )

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'content'
        verbose_name_plural = _('Contents')
        verbose_name = _('Content')


class Questions(models.Model):
    question = models.TextField(_('Question'), max_length=2500, )
    is_active = models.BooleanField(_('Active'), default=True, )
    answer = RichTextField(_('Answer'), )
    category = models.ForeignKey('Category', verbose_name=_('Categories'), on_delete=models.CASCADE, )
    order_field = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'questions'
        verbose_name_plural = _('Questions')
        verbose_name = _('Question')


class Binnacle(models.Model):
    id = models.IntegerField(primary_key=True)
    cod_binnacle = models.CharField(_('Binnacle'), max_length=50, )
    date_rescue = models.DateTimeField(_('Date rescue'), )
    period_rescue = models.IntegerField(_('Period rescue'), )
    noins = models.CharField(max_length=50, )
    idsocket = models.CharField(_('Socket'), max_length=50, )
    user_defined01 = models.CharField(_('User defined 01'), max_length=50, )
    user_defined02 = models.CharField(_('User defined 02'), max_length=50, )
    user_defined03 = models.CharField(_('User defined 03'), max_length=50, )
    description = models.CharField(_('Description'), max_length=100, )
    date_start = models.DateTimeField(_('date created'), )
    date_end = models.DateTimeField(_('date created'), )
    user = models.CharField(_('User'), max_length=50, blank=True, null=True, )
    idclient = models.CharField(max_length=50)
    reason = models.ForeignKey('Reason', verbose_name=_('Reason'), db_column='id_reason', on_delete=models.CASCADE,
                               blank=True, null=True, )
    mante_num = models.CharField(_('Mante Num'), max_length=20, )
    comments = models.CharField(_('Comments'), max_length=100, )
    origin = models.CharField(_('Origin'), max_length=50)
    state = models.CharField(_('state'), max_length=20)
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'binnacle'
        verbose_name_plural = _('Binnacles')
        verbose_name = _('Binnacle')


class MeasureDetail(models.Model):
    id_soc = models.IntegerField()
    is_backup = models.IntegerField()
    is_new = models.BooleanField(blank=True, null=True)
    is_novelty = models.BooleanField(blank=True, null=True)
    yearx = models.SmallIntegerField()
    monthx = models.SmallIntegerField()
    dayx = models.SmallIntegerField()
    hourx = models.SmallIntegerField()
    utchourx = models.SmallIntegerField()
    minute = models.SmallIntegerField(blank=True, null=True)
    minute_end = models.IntegerField()
    channel_val1 = models.FloatField(blank=True, null=True)
    channel_val2 = models.FloatField(blank=True, null=True)
    channel_val3 = models.FloatField(blank=True, null=True)
    channel_val4 = models.FloatField(blank=True, null=True)
    channel_val5 = models.FloatField(blank=True, null=True)
    channel_val6 = models.FloatField(blank=True, null=True)
    channel_val7 = models.FloatField(blank=True, null=True)
    channel_val8 = models.FloatField(blank=True, null=True)
    channel_val9 = models.FloatField(blank=True, null=True)
    channel_val10 = models.FloatField(blank=True, null=True)
    channel_val11 = models.FloatField(blank=True, null=True)
    channel_val12 = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    utcdatetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measure_detail'
        verbose_name_plural = _('Measures Details')
        verbose_name = _('Measure Detail')


class MeasureDetailHo(models.Model):
    id_soc = models.IntegerField()
    is_backup = models.IntegerField()
    yearx = models.SmallIntegerField()
    monthx = models.SmallIntegerField()
    dayx = models.SmallIntegerField()
    hourx = models.SmallIntegerField()
    utchourx = models.SmallIntegerField()
    hourx_end = models.IntegerField()
    channel_val1 = models.FloatField(blank=True, null=True)
    channel_val2 = models.FloatField(blank=True, null=True)
    channel_val3 = models.FloatField(blank=True, null=True)
    channel_val4 = models.FloatField(blank=True, null=True)
    channel_val5 = models.FloatField(blank=True, null=True)
    channel_val6 = models.FloatField(blank=True, null=True)
    channel_val7 = models.FloatField(blank=True, null=True)
    channel_val8 = models.FloatField(blank=True, null=True)
    channel_val9 = models.FloatField(blank=True, null=True)
    channel_val10 = models.FloatField(blank=True, null=True)
    channel_val11 = models.FloatField(blank=True, null=True)
    channel_val12 = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'measure_detail_ho'


class MeasureHead(models.Model):
    period_rescue = models.IntegerField()
    id_soc = models.IntegerField(db_column='ID_SOC')
    idclient = models.CharField(db_column='idclient', max_length=50)
    idsocket = models.CharField(db_column='idsocket', max_length=50)
    noins = models.CharField(max_length=50)
    id_cli = models.IntegerField()
    user_defined01 = models.CharField(max_length=50, blank=True, null=True)
    user_defined02 = models.CharField(max_length=50, blank=True, null=True)
    user_defined03 = models.CharField(max_length=50, blank=True, null=True)
    user_defined010 = models.CharField(max_length=50, blank=True, null=True)
    user_defined59 = models.CharField(max_length=50, blank=True, null=True)
    date_last_reading = models.DateTimeField(blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    last_datetime = models.DateTimeField(blank=True, null=True)
    is_backup = models.IntegerField(blank=True, null=True)
    backup_des = models.CharField(max_length=20, blank=True, null=True)
    binnacles = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        db_table = 'measure_head'


class BinnaclePeriod(models.Model):
    id_soc = models.IntegerField()
    is_backup = models.IntegerField(blank=True, null=True)
    binnacle = models.CharField(max_length=500, blank=True, null=True)
    period_rescue = models.IntegerField()
    user = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    date_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'binnacle_period'


class Reason(models.Model):
    user = models.CharField(_('User'), max_length=150, )
    description = models.CharField(_('Description'), max_length=50, unique=True)
    is_active = models.BooleanField(_('is active'), max_length=1, default=True, )
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(_('date update'), null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'reason'
        verbose_name_plural = _('Reasons')
        verbose_name = _('Reason')


class SocketHide(models.Model):
    idsocket = models.CharField(max_length=50)
    id_user = models.IntegerField()
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'socket_hide'


class Parameter(models.Model):
    name = models.CharField(_('Name'), max_length=50, unique=True, )
    value = models.TextField(_('Value'), max_length=500)
    description = models.CharField(_('Description'), max_length=254)
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'parameter'
        verbose_name_plural = _('Parameters')
        verbose_name = _('Parameter')


class Sockets(models.Model):
    idsocket = models.CharField(db_column='IDSOCKET', unique=True, max_length=50)
    description = models.CharField(db_column='DESCRIPTION', max_length=100)
    idclient = models.CharField(db_column='IDCLIENT', max_length=50)
    user_defined01 = models.CharField(db_column='USER_DEFINED01', max_length=100, blank=True, null=True)
    user_defined02 = models.CharField(db_column='USER_DEFINED02', max_length=100, blank=True, null=True)
    user_defined03 = models.CharField(db_column='USER_DEFINED03', max_length=100, blank=True, null=True)
    user_defined04 = models.CharField(db_column='USER_DEFINED04', max_length=100, blank=True, null=True)
    user_defined05 = models.CharField(db_column='USER_DEFINED05', max_length=100, blank=True, null=True)
    user_defined06 = models.CharField(db_column='USER_DEFINED06', max_length=100, blank=True, null=True)
    user_defined07 = models.CharField(db_column='USER_DEFINED07', max_length=100, blank=True, null=True)
    user_defined08 = models.CharField(db_column='USER_DEFINED08', max_length=100, blank=True, null=True)
    user_defined09 = models.CharField(db_column='USER_DEFINED09', max_length=100, blank=True, null=True)
    user_defined10 = models.CharField(db_column='USER_DEFINED10', max_length=100, blank=True, null=True)
    user_defined11 = models.CharField(db_column='USER_DEFINED11', max_length=100, blank=True, null=True)
    user_defined12 = models.CharField(db_column='USER_DEFINED12', max_length=100, blank=True, null=True)
    user_defined13 = models.CharField(db_column='USER_DEFINED13', max_length=100, blank=True, null=True)
    user_defined14 = models.CharField(db_column='USER_DEFINED14', max_length=100, blank=True, null=True)
    user_defined15 = models.CharField(db_column='USER_DEFINED15', max_length=100, blank=True, null=True)
    user_defined16 = models.CharField(db_column='USER_DEFINED16', max_length=100, blank=True, null=True)
    user_defined17 = models.CharField(db_column='USER_DEFINED17', max_length=100, blank=True, null=True)
    user_defined18 = models.CharField(db_column='USER_DEFINED18', max_length=100, blank=True, null=True)
    user_defined19 = models.CharField(db_column='USER_DEFINED19', max_length=100, blank=True, null=True)
    user_defined20 = models.CharField(db_column='USER_DEFINED20', max_length=100, blank=True, null=True)
    user_defined21 = models.CharField(db_column='USER_DEFINED21', max_length=100, blank=True, null=True)
    user_defined22 = models.CharField(db_column='USER_DEFINED22', max_length=100, blank=True, null=True)
    user_defined23 = models.CharField(db_column='USER_DEFINED23', max_length=100, blank=True, null=True)
    user_defined24 = models.CharField(db_column='USER_DEFINED24', max_length=100, blank=True, null=True)
    user_defined25 = models.CharField(db_column='USER_DEFINED25', max_length=100, blank=True, null=True)
    user_defined26 = models.CharField(db_column='USER_DEFINED26', max_length=100, blank=True, null=True)
    user_defined27 = models.CharField(db_column='USER_DEFINED27', max_length=100, blank=True, null=True)
    user_defined28 = models.CharField(db_column='USER_DEFINED28', max_length=100, blank=True, null=True)
    user_defined29 = models.CharField(db_column='USER_DEFINED29', max_length=100, blank=True, null=True)
    user_defined30 = models.CharField(db_column='USER_DEFINED30', max_length=100, blank=True, null=True)
    user_defined31 = models.CharField(db_column='USER_DEFINED31', max_length=100, blank=True, null=True)
    user_defined32 = models.CharField(db_column='USER_DEFINED32', max_length=100, blank=True, null=True)
    user_defined33 = models.CharField(db_column='USER_DEFINED33', max_length=100, blank=True, null=True)
    user_defined34 = models.CharField(db_column='USER_DEFINED34', max_length=100, blank=True, null=True)
    user_defined35 = models.CharField(db_column='USER_DEFINED35', max_length=100, blank=True, null=True)
    user_defined36 = models.CharField(db_column='USER_DEFINED36', max_length=100, blank=True, null=True)
    user_defined37 = models.CharField(db_column='USER_DEFINED37', max_length=100, blank=True, null=True)
    user_defined38 = models.CharField(db_column='USER_DEFINED38', max_length=100, blank=True, null=True)
    user_defined39 = models.CharField(db_column='USER_DEFINED39', max_length=100, blank=True, null=True)
    user_defined40 = models.CharField(db_column='USER_DEFINED40', max_length=100, blank=True, null=True)
    user_defined41 = models.CharField(db_column='USER_DEFINED41', max_length=100, blank=True, null=True)
    user_defined42 = models.CharField(db_column='USER_DEFINED42', max_length=100, blank=True, null=True)
    user_defined43 = models.CharField(db_column='USER_DEFINED43', max_length=100, blank=True, null=True)
    user_defined44 = models.CharField(db_column='USER_DEFINED44', max_length=100, blank=True, null=True)
    user_defined45 = models.CharField(db_column='USER_DEFINED45', max_length=100, blank=True, null=True)
    user_defined46 = models.CharField(db_column='USER_DEFINED46', max_length=100, blank=True, null=True)
    user_defined47 = models.CharField(db_column='USER_DEFINED47', max_length=100, blank=True, null=True)
    user_defined48 = models.CharField(db_column='USER_DEFINED48', max_length=100, blank=True, null=True)
    user_defined49 = models.CharField(db_column='USER_DEFINED49', max_length=100, blank=True, null=True)
    user_defined50 = models.CharField(db_column='USER_DEFINED50', max_length=100, blank=True, null=True)
    user_defined51 = models.CharField(db_column='USER_DEFINED51', max_length=100, blank=True, null=True)
    user_defined52 = models.CharField(db_column='USER_DEFINED52', max_length=100, blank=True, null=True)
    user_defined53 = models.CharField(db_column='USER_DEFINED53', max_length=100, blank=True, null=True)
    user_defined54 = models.CharField(db_column='USER_DEFINED54', max_length=100, blank=True, null=True)
    user_defined55 = models.CharField(db_column='USER_DEFINED55', max_length=100, blank=True, null=True)
    user_defined56 = models.CharField(db_column='USER_DEFINED56', max_length=100, blank=True, null=True)
    user_defined57 = models.CharField(db_column='USER_DEFINED57', max_length=100, blank=True, null=True)
    user_defined58 = models.CharField(db_column='USER_DEFINED58', max_length=100, blank=True, null=True)
    user_defined59 = models.CharField(db_column='USER_DEFINED59', max_length=100, blank=True, null=True)
    user_defined60 = models.CharField(db_column='USER_DEFINED60', max_length=100, blank=True, null=True)
    user_defined61 = models.CharField(db_column='USER_DEFINED61', max_length=100, blank=True, null=True)
    user_defined62 = models.CharField(db_column='USER_DEFINED62', max_length=100, blank=True, null=True)
    user_defined63 = models.CharField(db_column='USER_DEFINED63', max_length=100, blank=True, null=True)
    user_defined64 = models.CharField(db_column='USER_DEFINED64', max_length=100, blank=True, null=True)
    user_defined65 = models.CharField(db_column='USER_DEFINED65', max_length=100, blank=True, null=True)
    user_defined66 = models.CharField(db_column='USER_DEFINED66', max_length=100, blank=True, null=True)
    user_defined67 = models.CharField(db_column='USER_DEFINED67', max_length=100, blank=True, null=True)
    user_defined68 = models.CharField(db_column='USER_DEFINED68', max_length=100, blank=True, null=True)
    user_defined69 = models.CharField(db_column='USER_DEFINED69', max_length=100, blank=True, null=True)
    user_defined70 = models.CharField(db_column='USER_DEFINED70', max_length=100, blank=True, null=True)
    user_defined71 = models.CharField(db_column='USER_DEFINED71', max_length=100, blank=True, null=True)
    user_defined72 = models.CharField(db_column='USER_DEFINED72', max_length=100, blank=True, null=True)
    user_defined73 = models.CharField(db_column='USER_DEFINED73', max_length=100, blank=True, null=True)
    user_defined74 = models.CharField(db_column='USER_DEFINED74', max_length=100, blank=True, null=True)
    user_defined75 = models.CharField(db_column='USER_DEFINED75', max_length=100, blank=True, null=True)
    user_defined76 = models.CharField(db_column='USER_DEFINED76', max_length=100, blank=True, null=True)
    user_defined77 = models.CharField(db_column='USER_DEFINED77', max_length=100, blank=True, null=True)
    user_defined78 = models.CharField(db_column='USER_DEFINED78', max_length=100, blank=True, null=True)
    user_defined79 = models.CharField(db_column='USER_DEFINED79', max_length=100, blank=True, null=True)
    user_defined80 = models.CharField(db_column='USER_DEFINED80', max_length=100, blank=True, null=True)
    user_defined81 = models.CharField(db_column='USER_DEFINED81', max_length=100, blank=True, null=True)
    user_defined82 = models.CharField(db_column='USER_DEFINED82', max_length=100, blank=True, null=True)
    user_defined83 = models.CharField(db_column='USER_DEFINED83', max_length=100, blank=True, null=True)
    user_defined84 = models.CharField(db_column='USER_DEFINED84', max_length=100, blank=True, null=True)
    user_defined85 = models.CharField(db_column='USER_DEFINED85', max_length=100, blank=True, null=True)
    user_defined86 = models.CharField(db_column='USER_DEFINED86', max_length=100, blank=True, null=True)
    user_defined87 = models.CharField(db_column='USER_DEFINED87', max_length=100, blank=True, null=True)
    user_defined88 = models.CharField(db_column='USER_DEFINED88', max_length=100, blank=True, null=True)
    user_defined89 = models.CharField(db_column='USER_DEFINED89', max_length=100, blank=True, null=True)
    user_defined90 = models.CharField(db_column='USER_DEFINED90', max_length=100, blank=True, null=True)
    user_defined91 = models.CharField(db_column='USER_DEFINED91', max_length=100, blank=True, null=True)
    user_defined92 = models.CharField(db_column='USER_DEFINED92', max_length=100, blank=True, null=True)
    user_defined93 = models.CharField(db_column='USER_DEFINED93', max_length=100, blank=True, null=True)
    user_defined94 = models.CharField(db_column='USER_DEFINED94', max_length=100, blank=True, null=True)
    user_defined95 = models.CharField(db_column='USER_DEFINED95', max_length=100, blank=True, null=True)
    user_defined96 = models.CharField(db_column='USER_DEFINED96', max_length=100, blank=True, null=True)
    user_defined97 = models.CharField(db_column='USER_DEFINED97', max_length=100, blank=True, null=True)
    user_defined98 = models.CharField(db_column='USER_DEFINED98', max_length=100, blank=True, null=True)
    user_defined99 = models.CharField(db_column='USER_DEFINED99', max_length=100, blank=True, null=True)
    user_defined100 = models.CharField(db_column='USER_DEFINED100', max_length=100, blank=True, null=True)
    inserted_datetime = models.DateTimeField(db_column='INSERTED_DATETIME')
    location_address1 = models.CharField(db_column='LOCATION_ADDRESS1', max_length=127, blank=True, null=True)
    location_address2 = models.CharField(db_column='LOCATION_ADDRESS2', max_length=127, blank=True, null=True)
    location_address3 = models.CharField(db_column='LOCATION_ADDRESS3', max_length=127, blank=True, null=True)
    city = models.CharField(db_column='CITY', max_length=50, blank=True, null=True)
    state = models.CharField(db_column='STATE', max_length=30, blank=True, null=True)
    email = models.CharField(db_column='EMAIL', max_length=254, blank=True, null=True)
    address_comments = models.CharField(db_column='ADDRESS_COMMENTS', max_length=1440, blank=True, null=True)
    gps_lat = models.CharField(db_column='GPS_LAT', max_length=17, blank=True, null=True)
    gps_long = models.CharField(db_column='GPS_LONG', max_length=17, blank=True, null=True)
    altitude = models.CharField(db_column='ALTITUDE', max_length=17, blank=True, null=True)
    id_dev = models.IntegerField(db_column='ID_DEV', blank=True, null=True)
    id_soc = models.IntegerField(db_column='ID_SOC', primary_key=True)
    export_folder = models.CharField(db_column='EXPORT_FOLDER', max_length=100, blank=True, null=True)
    id_cli = models.IntegerField(db_column='ID_CLI')
    is_virtual = models.IntegerField(db_column='IS_VIRTUAL')
    integration_interval = models.IntegerField(db_column='INTEGRATION_INTERVAL', blank=True, null=True)
    id_nvo = models.IntegerField(db_column='ID_NVO', blank=True, null=True)
    update_datetime = models.DateTimeField(db_column='UPDATE_DATETIME', blank=True, null=True)
    id_sse = models.IntegerField(db_column='ID_SSE')
    cadastral_code = models.CharField(db_column='CADASTRAL_CODE', max_length=100, blank=True, null=True)
    id_sbt = models.IntegerField(db_column='ID_SBT', blank=True, null=True)
    border_type = models.IntegerField(db_column='BORDER_TYPE', blank=True, null=True)
    noins = models.CharField(db_column='NOINS', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sockets'


class ChannelConfig(models.Model):
    idvar = models.CharField(unique=True, max_length=100)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    order_field = models.IntegerField(blank=True, null=True)
    report_field = models.IntegerField(blank=True, null=True)
    report_order_field = models.IntegerField(blank=True, null=True)
    user = models.IntegerField()
    description1 = models.CharField(max_length=100, blank=True, null=True)
    description2 = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'channel_config'


class SocketsMeasure(models.Model):
    idsocket = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    idclient = models.CharField(max_length=50)
    user_defined01 = models.CharField(max_length=100, blank=True, null=True)
    user_defined02 = models.CharField(max_length=100, blank=True, null=True)
    user_defined03 = models.CharField(max_length=100, blank=True, null=True)
    user_defined10 = models.CharField(max_length=100, blank=True, null=True)
    inserted_datetime = models.DateTimeField()
    id_soc = models.IntegerField(primary_key=True)
    id_cli = models.IntegerField()
    is_virtual = models.IntegerField()
    integration_interval = models.IntegerField(blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'sockets_measure'


class MtCollectorHistory(models.Model):
    idclient = models.CharField(db_column='idclient', max_length=50)
    idsocket = models.CharField(db_column='idsocket', max_length=50)
    mail = models.CharField(db_column='mail', max_length=254)
    name_file = models.CharField(db_column='name_file', max_length=100)
    path_file = models.CharField(db_column='path_file', max_length=254)
    observation = models.TextField(db_column='observation', max_length=2500, null=True, blank=True, )
    message = models.TextField(db_column='message', max_length=2500)
    date_start = models.DateTimeField(_('date start'), default=timezone.now, )
    date_end = models.DateTimeField(_('date end'), default=timezone.now, )
    date_created = models.DateTimeField(_('date created'), default=timezone.now, )
    date_update = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'mt_collector_history'


class SocketChannel(models.Model):
    id_soc = models.IntegerField()
    noins = models.CharField(max_length=50)
    idsocket = models.CharField(max_length=50)
    idclient = models.CharField(max_length=50)
    serialno = models.CharField(max_length=30)
    user_defined01 = models.CharField(max_length=50, blank=True, null=True)
    user_defined02 = models.CharField(max_length=50, blank=True, null=True)
    user_defined03 = models.CharField(max_length=50, blank=True, null=True)
    user_defined06 = models.CharField(max_length=50, blank=True, null=True)
    user_defined07 = models.CharField(max_length=50, blank=True, null=True)
    user_defined14 = models.CharField(max_length=50, blank=True, null=True)
    user_defined17 = models.CharField(max_length=50, blank=True, null=True)
    user_defined18 = models.CharField(max_length=50, blank=True, null=True)
    min_datetime = models.DateTimeField()
    max_datetime = models.DateTimeField()
    user_defined59 = models.CharField(max_length=50, blank=True, null=True)
    num_log = models.IntegerField(db_column='NUM_LOG', blank=True, null=True)
    in_energia_act = models.CharField(max_length=50)
    re_energia_act = models.CharField(max_length=50)
    in_energia_rea = models.CharField(max_length=50)
    re_energia_rea = models.CharField(max_length=50)
    kwhd = models.IntegerField(db_column='kWhD', blank=True, null=True)
    kvarhd = models.IntegerField(db_column='kVarhD', blank=True, null=True)
    kwhr = models.IntegerField(db_column='kWhR', blank=True, null=True)
    kvarhr = models.IntegerField(db_column='kVarhR', blank=True, null=True)
    vll_ab_mean = models.IntegerField(db_column='Vll_ab_mean', blank=True, null=True)
    vll_bc_mean = models.IntegerField(db_column='Vll_bc_mean', blank=True, null=True)
    vll_ca_mean = models.IntegerField(db_column='Vll_ca_mean', blank=True, null=True)
    ia_mean = models.IntegerField(db_column='Ia_mean', blank=True, null=True)
    ib_mean = models.IntegerField(db_column='Ib_mean', blank=True, null=True)
    ic_mean = models.IntegerField(db_column='Ic_mean', blank=True, null=True)
    vll_avg_mean = models.IntegerField(db_column='Vll_avg_mean', blank=True, null=True)
    iavg_mean = models.IntegerField(db_column='Iavg_mean', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'socket_channel'


class ChannelOrder(models.Model):
    id_soc = models.IntegerField()
    channel1 = models.CharField(max_length=50, blank=True, null=True)
    channel2 = models.CharField(max_length=50, blank=True, null=True)
    channel3 = models.CharField(max_length=50, blank=True, null=True)
    channel4 = models.CharField(max_length=50, blank=True, null=True)
    channel5 = models.CharField(max_length=50, blank=True, null=True)
    channel6 = models.CharField(max_length=50, blank=True, null=True)
    channel7 = models.CharField(max_length=50, blank=True, null=True)
    channel8 = models.CharField(max_length=50, blank=True, null=True)
    channel9 = models.CharField(max_length=50, blank=True, null=True)
    channel10 = models.CharField(max_length=50, blank=True, null=True)
    channel11 = models.CharField(max_length=50, blank=True, null=True)
    channel12 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'channel_order'
