import os
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import models
from dotenv import load_dotenv

load_dotenv(os.path.join('.env'))

# Create your models here.
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    try:
        # Create default groups if they don't exist
        group_names = ['manager', 'user', 'public']
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"Group {group_name} created.")

        # Create users for each role if they don't already exist
        # Manager User
        if not User.objects.filter(username='manager').exists():
            manager_user = User.objects.create_user(
                username=os.getenv('MANAGER_USER'),
                first_name=os.getenv('MANAGER_FRIST'),
                last_name=os.getenv('MANAGER_LAST'),
                email=os.getenv('MANAGER_EMAIL'),
                password=os.getenv('MANAGER_PASS')
            )
            manager_group = Group.objects.get(name='manager')
            manager_user.groups.add(manager_group)
            manager_user.save()
            print("Manager user created successfully.")

        # Regular User
        if not User.objects.filter(username='user').exists():
            regular_user = User.objects.create_user(
                username=os.getenv('USER_USER'),
                first_name=os.getenv('USER_FRIST'),
                last_name=os.getenv('USER_LAST'),
                email=os.getenv('USER_EMAIL'),
                password=os.getenv('USER_PASS')
            )
            user_group = Group.objects.get(name='user')
            regular_user.groups.add(user_group)
            regular_user.save()
            print("Regular user created successfully.")

        # Public User
        if not User.objects.filter(username='public').exists():
            public_user = User.objects.create_user(
                username=os.getenv('PUBLIC_USER'),
                first_name=os.getenv('PUBLIC_FRIST'),
                last_name=os.getenv('PUBLIC_LAST'),
                email=os.getenv('PUBLIC_EMAIL'),
                password=os.getenv('PUBLIC_PASS')
            )
            public_group = Group.objects.get(name='public')
            public_user.groups.add(public_group)
            public_user.save()
            print("Public user created successfully.")

    except Exception as e:
        print(f"Error during group and user creation: {e}")

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    try:
        if not User.objects.filter(is_superuser=True).exists():
            # Create a superuser if one doesn't exist
            User.objects.create_superuser(
                username=os.getenv('SUPER_USER'),
                email=os.getenv('SUPER_EMAIL'),
                password=os.getenv('SUPER_PASS'),
                is_staff=True
            )
            print("Superuser created successfully.")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")

    # Assign permissions to groups after creating them
    manager_group = Group.objects.get(name='manager')
    user_group = Group.objects.get(name='user')
    public_group = Group.objects.get(name='public')

    # Module
    module_content_type = ContentType.objects.get_for_model(Module)
    module_permissions = Permission.objects.filter(content_type=module_content_type)

    for perm in module_permissions:
        if perm.codename == 'delete_module':
            # Manager gets delete permission
            manager_group.permissions.add(perm)
        elif perm.codename in ['change_module', 'add_module']:
            # User and Manager get add/change permissions
            user_group.permissions.add(perm)
            manager_group.permissions.add(perm)
        elif perm.codename == 'view_module':
            # Public, User, and Manager get view permission
            public_group.permissions.add(perm)
            user_group.permissions.add(perm)
            manager_group.permissions.add(perm)

    # Product
    product_content_type = ContentType.objects.get_for_model(Product)
    product_permissions = Permission.objects.filter(content_type=product_content_type)

    for perm in product_permissions:
        if perm.codename == 'delete_product':
            # Manager gets delete permission
            manager_group.permissions.add(perm)
        elif perm.codename in ['change_product', 'add_product']:
            # User and Manager get add/change permissions
            user_group.permissions.add(perm)
            manager_group.permissions.add(perm)
        elif perm.codename == 'view_product':
            # Public, User, and Manager get view permission
            public_group.permissions.add(perm)
            user_group.permissions.add(perm)
            manager_group.permissions.add(perm)

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    id = models.BigAutoField(primary_key=True)
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


class Module(models.Model):
    id_module = models.AutoField(primary_key=True)
    auth_user_id = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='auth_user_id', blank=True, null=True)
    name = models.CharField(unique=True, max_length=255)
    installed = models.BooleanField(default=False)
    version = models.CharField(max_length=50)
    extra_fields = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'module'

class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    module_id = models.ForeignKey(Module, models.DO_NOTHING, db_column='module_id', blank=True, null=True)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    extra_fields = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'product'
        unique_together = (('name', 'barcode', 'module_id'),)
