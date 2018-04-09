from django.db import models
from django.contrib.auth.models import User
#common data model
class Asset(models.Model):
    """data sheet of asset's common property"""
    asset_type_choice = (
        ('server', 'server_asset'),
        ('networkdevice', 'network_asset'),
        ('storagedevice', 'storage_asset'),
        ('securitydevice','security_asset'),
        ('software','software_asset'),
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
    sn = models.CharField(max_length=128, unique=True, verbose_name='asset_serial_number')
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name="belonging_business")
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name="asset_status")

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name="manufacturer")
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="manage_ip")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='tags')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='asset_manager',related_name="admin")
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='locating_computer_room')
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='contract')

    purchase_day = models.DateField(null=True, blank=True, verbose_name='purchase_day')
    expire_day = models.DateField(null=True, blank=True, verbose_name='expired_date')
    price = models.FloatField(null=True, blank=True, verbose_name='price')

    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='approver', related_name='approved_by')

    memo = models.TextField(null=True, blank=True, verbose_name='comment')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='approve_date')
    m_time = models.DateTimeField(auto_now=True, verbose_name='update_date')

    def __str__(self):
        return '<%s> %s' % (self.get_asset_type_display(),self.name)

    class Meta:
        verbose_name = 'asset_general_table'
        verbose_name_plural = 'asset_general_table'
        ordering = ['-c_time']

#server model
class Server(models.Model):
    """server asset"""
    sub_asset_type_choice = {
        (0, 'pc server'),
        (1, 'blade computer'),
        (2, 'mini computer'),
    }

    created_by_choice = {
        ('auto', 'auto_add'),
        ('manual', 'manual_record'),
    }

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="server_types")
    created_by_choice = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="adding_type")
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',blank=True, null=True, verbose_name="host_machine")
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='server_type')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='raid_type')

    os_type = models.CharField('operating_system_type', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('released_version',max_length=64, blank=True, null=True)
    os_release = models.CharField('operating_system_version',max_length=64,blank=True,null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

#device model
class SecurityDevice(models.Model):
    """security asset"""
    sub_asset_type_choice = (
        (0, 'firewall'),
        (1, 'intrusion_detecting_device'),
        (2, 'internet_gateway'),
        (4, 'operation_and_maintenance_system'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="security_system_type")

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + " id:%s" % self.id

    class Meta:
        verbose_name = 'security_system'
        verbose_name_plural = "security_system"

class StorageDevice(models.Model):
    """storage asset"""
    sub_asset_type_choice = (
        (0, 'disk_array'),
        (1, 'network_attached_storage'),
        (2, 'tape_library'),
        (4, 'tape_station'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="storage_device_type")

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + " id:%s" % self.id

    class Meta:
        verbose_name = 'storage_device'
        verbose_name_plural = "storage_device"

class NetworkDevice(models.Model):
    """network asset"""
    sub_asset_type_choice = (
        (0, 'router'),
        (1, 'interchanger'),
        (2, 'load_banlancing'),
        (4, 'vpn_device'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="network_device_type")

    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="vlan_ip")
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="intranet_ip")

    model = models.CharField(max_length=128, null=True, blank=True, verbose_name="network_device_model")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="device_firmware_version")
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="port_num")
    device_detail = models.TextField(null=True, blank=True, verbose_name="device_detail")

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = 'network_device'
        verbose_name_plural = "network_device"

class Software(models.Model):
    """paid software"""
    sub_asset_type_choice = (
        (0, 'operation_system'),
        (1, 'office/development software'),
        (2, 'business_software'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="software_type")
    license_num = models.IntegerField(default=1, verbose_name="authorized_number")
    version = models.CharField(max_length=64, unique=True, help_text='example: CentOS release 6.7 (Final)',
                               verbose_name='software/system_version')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = 'software/system'
        verbose_name_plural = "software/system"

# CMDB information models
class IDC(models.Model):
    """computer room"""
    name = models.CharField(max_length=64, unique=True, verbose_name="computer_room_name")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='comment')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'computer_room'
        verbose_name_plural = "computer_room"

class Manufacturer(models.Model):
    """manufacturer"""
    name = models.CharField('manufacture_name', max_length=64, unique=True)
    telephone = models.CharField('support_telephone', max_length=30, blank=True, null=True)
    memo = models.CharField('comment', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'manufacture'
        verbose_name_plural = "manufacture"

class BusinessUnit(models.Model):
    """business line"""
    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level')
    name = models.CharField('business_line', max_length=64, unique=True)
    memo = models.CharField('comment', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'business_line'
        verbose_name_plural = "business_line"

class Contract(models.Model):
    """contract"""
    sn = models.CharField('contract_number', max_length=128, unique=True)
    name = models.CharField('contract_name', max_length=64)
    memo = models.TextField('comment', blank=True, null=True)
    price = models.IntegerField('contract_price')
    detail = models.TextField('contract_detail', blank=True, null=True)
    start_day = models.DateField('start_day', blank=True, null=True)
    end_day = models.DateField('end_day', blank=True, null=True)
    license_num = models.IntegerField('license_number', blank=True, null=True)
    c_day = models.DateField('create_date', auto_now_add=True)
    m_day = models.DateField('modified_date', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'contract'
        verbose_name_plural = "contract"

class Tag(models.Model):
    """tag"""
    name = models.CharField('tag_name', max_length=32, unique=True)
    c_day = models.DateField('create_date', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = "tag"
#CPU model

class CPU(models.Model):
    """CPU"""
    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField('cpu_type', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('cpu_number', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('cpu_core_number', default=1)

    def __str__(self):
        return self.asset.name + ":   " + self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"

#RAM model
class RAM(models.Model):
    """RAM"""
    asset = models.ForeignKey('Asset')  # 只能通过外键关联Asset。否则不能同时关联服务器、网络设备等等。
    sn = models.CharField('sn_number', max_length=128, blank=True, null=True)
    model = models.CharField('memory_type', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('memory_manufacturer', max_length=128, blank=True, null=True)
    slot = models.CharField('slot', max_length=64)
    capacity = models.IntegerField('memory_size(GB)', blank=True, null=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一

#Harddisk model
class Disk(models.Model):
    """Harddisk model"""
    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey('Asset')
    sn = models.CharField('disk_sn_number', max_length=128)
    slot = models.CharField('slot_number', max_length=64, blank=True, null=True)
    model = models.CharField('disk_model', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('disk_manufacturer', max_length=128, blank=True, null=True)
    capacity = models.FloatField('disk_capacity(GB)', blank=True, null=True)
    interface_type = models.CharField('slot_type', max_length=16, choices=disk_interface_type_choice, default='unknown')

    def __str__(self):
        return '%s:  %s:  %s:  %sGB' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = 'disk'
        verbose_name_plural = "disk"
        unique_together = ('asset', 'sn')

class NIC(models.Model):
    """network card"""
    asset = models.ForeignKey('Asset')  # 注意要用外键
    name = models.CharField('network_card_number', max_length=64, blank=True, null=True)
    model = models.CharField('network_card_model', max_length=128)
    mac = models.CharField('mac_address', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField('ip_address', blank=True, null=True)
    net_mask = models.CharField('mask', max_length=64, blank=True, null=True)
    bonding = models.CharField('bonding_address', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s:  %s:  %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = 'network_card'
        verbose_name_plural = "network_card"
        unique_together = ('asset', 'model', 'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。

# log model
class EventLog(models.Model):
    """event log"""
    name = models.CharField('event_name', max_length=128)
    event_type_choice = (
        (0, 'other'),
        (1, 'hardware_alteration'),
        (2, 'new_accessories'),
        (3, 'device_offline'),
        (4, 'device_online'),
        (5, 'scheduled_maintance'),
        (6, 'business_online/offline/alteration'),
    )
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True,
                                  on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.SmallIntegerField('event_type', choices=event_type_choice, default=4)
    component = models.CharField('event_subitem', max_length=256, blank=True, null=True)
    detail = models.TextField('event_detail')
    date = models.DateTimeField('event_date', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='event_executor',
                             on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    memo = models.TextField('comment', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'eventlog'
        verbose_name_plural = "eventlog"


# new asset approval model
class NewAssetApprovalZone(models.Model):
    """asset approval model"""
    sn = models.CharField('asset_sn_number', max_length=128, unique=True)  # 此字段必填
    asset_type_choice = (
        ('server', 'server'),
        ('networkdevice', 'network_device'),
        ('storagedevice', 'storage_device'),
        ('securitydevice', 'security_device'),
        ('IDC', 'computer_room'),
        ('software', 'software_asset'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='asset_type')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='manufacturer')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='model')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='ream_size')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='cpu_model')
    cpu_count = models.PositiveSmallIntegerField(blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)

    data = models.TextField('asser_data')  # 此字段必填

    c_time = models.DateTimeField('create_time', auto_now_add=True)
    m_time = models.DateTimeField('update_time', auto_now=True)
    approved = models.BooleanField('whether_approve', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = 'new_pending_approval_asset'
        verbose_name_plural = "new_pending_approval_asset"
        ordering = ['-c_time']
