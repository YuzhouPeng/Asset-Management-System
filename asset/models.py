from django.db import models

#common data model
class Asset(models.Model):
    """data sheet of asset's common property"""
    asset_type_choice = (
        ('server', 'serverasset'),
        ('networkdevice', 'networkasset'),
        ('storagedevice', 'storageasset'),
        ('securitydevice','securityasset'),
        ('software','softwareasset'),
    )

    asset_status = (
        (0,'online'),
        (1,'offline'),
        (2,'unknown'),
        (3,'error'),
        (4,'standby'),
    )
    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name="asset_type")
    name = models.CharField(max_length=128, unique=True, verbose_name="asset_serial_number")
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name="belonging_business")
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name="asset_status")

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name="manufacturer")
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="manage_ip")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='tags')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='asset_manager',related_name="admin")

#server model
class Server(models.Model):
    """server asset"""

#device model
class SecurityDevice(models.Model):
    """security asset"""

class StorageDevice(models.Model):
    """storage asset"""

class NetworkDevice(models.Model):
    """network asset"""

class Software(models.Model):
    """paid software"""

# CMDB information models
class IDC(models.Model):
    """computer room"""

class Manufacturer(models.Model):
    """manufacturer"""

class BusinessUnit(models.Model):
    """business line"""

class Contract(models.Model):
    """contract"""

class Tag(models.Model):
    """tag"""

#CPU model

class CPU(models.Model):
    """CPU"""

#RAM model
class RAM(models.Model):
    """RAM"""

#Harddisk model
class Disk(models.Model):
    """Harddisk model"""

class NIC(models.Model):
    """network card"""
# log model
class EventLog(models.Model):
    """event log"""
# new asset approval model
class NewAssetApprovalZone(models.Model):
    """asset approval model"""

# user model
class User(models.Model):
    """user"""