from django.db import models
from django.utils import timezone

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Place(BaseModel):
    '''地点表'''
    room_name = models.CharField(
        max_length=30, unique=True, verbose_name='位置名称')

    def __str__(self) -> str:
        return self.room_name

    class Meta:
        verbose_name = '地点信息'
        verbose_name_plural = verbose_name


class Manufacturer(BaseModel):
    '''供应商表'''
    name = models.CharField(max_length=50, verbose_name='供应商')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = '供应商信息'
        verbose_name_plural = verbose_name


class Category(BaseModel):
    '''型号表'''
    class_choices = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
        (5, 'E'),
    )
    model = models.CharField(max_length=50, verbose_name='型号')
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name="供应商", on_delete=models.CASCADE)
    name_zh = models.CharField(max_length=50, verbose_name='中文名称')
    name_en = models.CharField(max_length=50, verbose_name='英文名称')
    classification = models.SmallIntegerField(
        choices=class_choices, verbose_name='设备分类')
    Range = models.CharField(max_length=50, blank=True, verbose_name='范围')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = '型号信息'
        verbose_name_plural = verbose_name


class User(BaseModel):
    '''人员表'''
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = '人员信息'
        verbose_name_plural = verbose_name


class Instrument(BaseModel):
    '''设备表'''
    status_choices = (
        (1, '安装中'),
        (2, '使用中'),
        (3, '退休'),
        (4, '备用'),
        (5, '宁波设备'),
    )
    eql = models.CharField(max_length=30, unique=True, verbose_name='设备编号')
    sn = models.CharField(max_length=50, unique=True, verbose_name='序列号')
    calibration_date = models.DateField(
        blank=True, null=True, verbose_name='校准日期')
    calibration_due = models.DateField(
        blank=True, null=True, verbose_name='校准到期日期')
    pm_date = models.DateField(blank=True, null=True, verbose_name='PM日期')
    pm_due = models.DateField(blank=True, null=True, verbose_name='PM到期日期')
    release_date = models.DateField(blank=True, null=True, verbose_name='释放日期')
    status = models.SmallIntegerField(
        choices=status_choices, verbose_name='设备状态')
    retire_date = models.DateField(blank=True, null=True, verbose_name='退休日期')
    note = models.TextField(blank=True, verbose_name='备注')
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, verbose_name='位置')
    model = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='型号')
    primary_assignee = models.ForeignKey(
        User, related_name='primary_assigned_instruments', on_delete=models.CASCADE, verbose_name='首责任人')
    secondary_assignee = models.ForeignKey(
        User, related_name='secondary_assigned_instruments', on_delete=models.CASCADE, verbose_name='次责任人')

    def __str__(self) -> str:
        return self.eql

    class Meta:
        verbose_name = '设备信息'
        verbose_name_plural = verbose_name
