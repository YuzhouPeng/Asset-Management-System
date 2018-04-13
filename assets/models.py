from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Asset(models.Model):
    """    所有资产的共有数据表    """
    asset_type_choice = (
        ('server', 'server_device'),
        ('networkdevice', 'network_device'),
        ('storagedevice', 'stroage_device'),
        ('securitydevice', 'security_device'),
        ('software', 'software_device'),
    )

    asset_status = (
        (0, 'online'),
        (1, 'offline'),
        (2, 'unknown'),
        (3, 'fault'),
        (4, 'backup'),
        )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name="asset_type")
    name = models.CharField(max_length=64, unique=True, verbose_name="asset_name")     # 不可重复
    sn = models.CharField(max_length=128, unique=True, verbose_name="asset_serial_number")  # 不可重复
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='belonging_business_unit')
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='device_condition')

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='manufacturer')
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='manage_ip')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='tags')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='asset_admin', related_name='admin')
    idc = models.ForeignKey('IDC', null=True, blank=True, verbose_name='idc')
    contract = models.ForeignKey('Contract', null=True, blank=True, verbose_name='contract')

    purchase_day = models.DateField(null=True, blank=True, verbose_name="purchase_day")
    expire_day = models.DateField(null=True, blank=True, verbose_name="expire_day")
    price = models.FloatField(null=True, blank=True, verbose_name="price")

    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='approver', related_name='approved_by')

    memo = models.TextField(null=True, blank=True, verbose_name='comment')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='create_date')
    m_time = models.DateTimeField(auto_now=True, verbose_name='update_time')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = 'asset_table'
        verbose_name_plural = "asset_table"
        ordering = ['-c_time']


class Server(models.Model):
    """服务器设备"""
    sub_asset_type_choice = (
        (0, 'pc_server'),
        (1, 'blade_computer'),
        (2, 'mini+computer'),
    )

    created_by_choice = (
        ('auto', 'auto_record'),
        ('manual', 'manual_record'),
    )

    asset = models.OneToOneField('Asset')  # 非常关键的一对一关联！
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="server_type")
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="create_type")
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server',
                                  blank=True, null=True, verbose_name="host_machine")  # 虚拟机专用字段
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='server_model')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='raid_type')

    os_type = models.CharField('os_type', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('os_distribution_version', max_length=64, blank=True, null=True)
    os_release = models.CharField('os_release_version', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = 'server'
        verbose_name_plural = "server"


class SecurityDevice(models.Model):
    """安全设备"""
    sub_asset_type_choice = (
        (0, 'firewall'),
        (1, 'intrusion_detect_system'),
        (2, 'internet_gateway'),
        (4, 'maintance_system'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="security_device_type")

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + " id:%s" % self.id

    class Meta:
        verbose_name = 'security_device'
        verbose_name_plural = "security_device"


class StorageDevice(models.Model):
    """存储设备"""
    sub_asset_type_choice = (
        (0, 'disk_array'),
        (1, 'network_storage'),
        (2, 'tape_library'),
        (4, 'tape_machine'),
    )

    asset = models.OneToOneField('Asset')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="storage_device_type")

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + " id:%s" % self.id

    class Meta:
        verbose_name = 'storage_device'
        verbose_name_plural = "storage_device"


class NetworkDevice(models.Model):
    """网络设备"""
    sub_asset_type_choice = (
        (0, 'router'),
        (1, 'interchanger'),
        (2, 'load_balancing'),
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
    """
    只保存付费购买的软件
    """
    sub_asset_type_choice = (
        (0, 'operation_system'),
        (1, 'office\development_software'),
        (2, 'business_software'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="software_type")
    license_num = models.IntegerField(default=1, verbose_name="license_number")
    version = models.CharField(max_length=64, unique=True, help_text='example: CentOS release 6.7 (Final)',
                               verbose_name='software/system_version')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = 'software/system'
        verbose_name_plural = "software/system"


class IDC(models.Model):
    """data center"""
    name = models.CharField(max_length=64, unique=True, verbose_name="idc_name")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='comment')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'idc'
        verbose_name_plural = "idc"


class Manufacturer(models.Model):
    """厂商"""

    name = models.CharField('manufacturer_name', max_length=64, unique=True)
    telephone = models.CharField('support_telephone', max_length=30, blank=True, null=True)
    memo = models.CharField('comment', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'manufacturer'
        verbose_name_plural = "manufacturer"


class BusinessUnit(models.Model):
    """业务线"""

    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level')
    name = models.CharField('business_name', max_length=64, unique=True)
    memo = models.CharField('comment', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'business_unit'
        verbose_name_plural = "business_unit"


class Contract(models.Model):
    """合同"""

    sn = models.CharField('contract_serial_number', max_length=128, unique=True)
    name = models.CharField('contract_name', max_length=64)
    memo = models.TextField('comment', blank=True, null=True)
    price = models.IntegerField('contract_price')
    detail = models.TextField('contract_detail', blank=True, null=True)
    start_day = models.DateField('contract_start_day', blank=True, null=True)
    end_day = models.DateField('contract_end_day', blank=True, null=True)
    license_num = models.IntegerField('license_number', blank=True, null=True)
    c_day = models.DateField('create_time', auto_now_add=True)
    m_day = models.DateField('update_time', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'contract'
        verbose_name_plural = "contract"


class Tag(models.Model):
    """标签"""
    name = models.CharField('tag_name', max_length=32, unique=True)
    c_day = models.DateField('create_day', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = "tag"


class CPU(models.Model):
    """CPU组件"""

    asset = models.OneToOneField('Asset')  # 设备上的cpu肯定都是一样的，所以不需要建立多个cpu数据，一条就可以，因此使用一对一。
    cpu_model = models.CharField('cpu_model', max_length=128, blank=True, null=True)
    cpu_count = models.PositiveSmallIntegerField('cpu_count', default=1)
    cpu_core_count = models.PositiveSmallIntegerField('cpu_core_count', default=1)

    def __str__(self):
        return self.asset.name + ":   " + self.cpu_model

    class Meta:
        verbose_name = 'cpu'
        verbose_name_plural = "cpu"

class RAM(models.Model):
    """内存组件"""

    asset = models.ForeignKey('Asset')  # 只能通过外键关联Asset。否则不能同时关联服务器、网络设备等等。
    sn = models.CharField('ram_serial_number', max_length=128, blank=True, null=True)
    model = models.CharField('ram_model', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('ram_manufacturer', max_length=128, blank=True, null=True)
    slot = models.CharField('slot', max_length=64)
    capacity = models.IntegerField('ram_capacity', blank=True, null=True)

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = 'ram'
        verbose_name_plural = "ram"
        unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一


class Disk(models.Model):
    """存储设备"""

    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey('Asset')
    sn = models.CharField('disk_serial_number', max_length=128)
    slot = models.CharField('slot_position', max_length=64, blank=True, null=True)
    model = models.CharField('disk_model', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('disk_manufacturer', max_length=128, blank=True, null=True)
    capacity = models.FloatField('disk_capacity', blank=True, null=True)
    interface_type = models.CharField('interface_type', max_length=16, choices=disk_interface_type_choice, default='unknown')

    def __str__(self):
        return '%s:  %s:  %s:  %sGB' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = 'disk'
        verbose_name_plural = "disk"
        unique_together = ('asset', 'sn')

class NIC(models.Model):
    """network card"""

    asset = models.ForeignKey('Asset')  # 注意要用外键
    name = models.CharField('nic_name', max_length=64, blank=True, null=True)
    model = models.CharField('nic_model', max_length=128)
    mac = models.CharField('mac_address', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField('ip_address', blank=True, null=True)
    net_mask = models.CharField('mask', max_length=64, blank=True, null=True)
    bonding = models.CharField('bonding_address', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s:  %s:  %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = 'nic'
        verbose_name_plural = "nic"
        unique_together = ('asset', 'model', 'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。

class EventLog(models.Model):
    """
    日志.
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """

    name = models.CharField('event_name', max_length=128)
    event_type_choice = (
        (0, 'other'),
        (1, 'hardware_alternation'),
        (2, 'increased_asset'),
        (3, 'asset_offline'),
        (4, 'asset_online'),
        (5, 'maintance_routine'),
        (6, 'business_online_update_alternation'),
    )
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.SmallIntegerField('event_type', choices=event_type_choice, default=4)
    component = models.CharField('event_component', max_length=256, blank=True, null=True)
    detail = models.TextField('event_detail')
    date = models.DateTimeField('event_time', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='event_executor', on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    memo = models.TextField('comment', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'eventlog'
        verbose_name_plural = "eventlog"

class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    sn = models.CharField('asset_serial_number', max_length=128, unique=True)  # 此字段必填
    asset_type_choice = (
        ('server', 'server'),
        ('networkdevice', 'networkdevice'),
        ('storagedevice', 'storagedevice'),
        ('securitydevice', 'securitydevice'),
        ('IDC', 'IDC'),
        ('software', 'software'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='asset_type')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='manufacturer')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='model')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='ram_size')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='cpu_model')
    cpu_count = models.PositiveSmallIntegerField(blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)

    data = models.TextField('asset_data')  # 此字段必填

    c_time = models.DateTimeField('create_time', auto_now_add=True)
    m_time = models.DateTimeField('update_time', auto_now=True)
    approved = models.BooleanField('approve', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = 'new_asset_approval'
        verbose_name_plural = "new_asset_approval"
        ordering = ['-c_time']