# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AnalysisData(models.Model):
    node = models.CharField(primary_key=True, max_length=100)
    lz_hb = models.CharField(max_length=100, blank=True, null=True)
    trend_3yr = models.FloatField(blank=True, null=True)
    trend_2yr = models.FloatField(blank=True, null=True)
    trend_1yr = models.FloatField(blank=True, null=True)
    typical_production = models.FloatField(blank=True, null=True)
    typical_yield = models.FloatField(blank=True, null=True)
    av_delta = models.FloatField(blank=True, null=True)
    av_revenue = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Analysis_Data'


class HourlyLmp(models.Model):
    deliverydate = models.CharField(max_length=100, blank=True, null=True)
    hourending = models.CharField(max_length=100, blank=True, null=True)
    busname = models.CharField(db_index=True,primary_key=True,max_length=100, blank=True, null=False)
    lmp = models.FloatField(blank=True, null=True)
    dstflag = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Hourly_LMP'

class BowenTest(models.Model):
    deliverydate = models.CharField(max_length=100, blank=True, null=True)
    hourending = models.CharField(max_length=100, blank=True, null=True)
    busname = models.CharField(primary_key=True,max_length=100, blank=True, null=False)
    lmp = models.FloatField(blank=True, null=True)
    dstflag = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bowen_Test'

class NodeLocations(models.Model):
    node = models.CharField(primary_key=True, max_length=50)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    utility = models.CharField(max_length=100, blank=True, null=True)
    voltage_min = models.IntegerField(blank=True, null=True)
    voltage_max = models.IntegerField(blank=True, null=True)
    settlement_lz = models.CharField(db_column='settlement_LZ', max_length=100, blank=True, null=True)  # Field name made lowercase.
    loc_proxy = models.IntegerField(blank=True, null=True)
    lz_proxy = models.IntegerField(db_column='LZ_proxy', blank=True, null=True)  # Field name made lowercase.
    util_proxy = models.IntegerField(blank=True, null=True)
    optional = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Node_Locations'


class SpointData(models.Model):
    node = models.CharField(primary_key=True,max_length=100, blank=True, null=False)
    revenue = models.FloatField(blank=True, null=True)
    production = models.FloatField(blank=True, null=True)
    yield_field = models.FloatField(db_column='yield', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SPoint_Data'


class SpointLmp(models.Model):
    date = models.CharField(max_length=100, blank=True, null=True)
    hourending = models.CharField(max_length=50, blank=True, null=True)
    repeated_hr = models.CharField(max_length=1, blank=True, null=True)
    spoint = models.CharField(db_column='SPoint', max_length=100, blank=True, null=False, primary_key=True)  # Field name made lowercase.
    spoint_lmp = models.FloatField(db_column='SPoint_lmp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPoint_LMP'


class SpointLocations(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SPoint_Locations'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
