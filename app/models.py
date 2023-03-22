from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import random


class MyAccountManager(BaseUserManager):
    '''
    Extending the BaseUserManager.
    '''
    # def create_user(self, email, username, password=None):
    def create_user(self, email, password=None):
        '''
        OverWriting the create_user function.
        '''
        if not email:
            raise ValueError('Users must have an email address')
        # if not username:
        #     raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            # username=username,
        )

        user.set_password(password)
        user.is_active=False
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, username, password):
    def create_superuser(self, email, password):
        '''
        OverWriting the create_superuser function.
        '''

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            # username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    Creating thr custom user module schema.
    '''
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    # username                = models.CharField(max_length=30, unique=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    first_name              = models.CharField(max_length=15, blank=True, null=True)
    last_name               = models.CharField(max_length=15, blank=True, null=True)
    aid                     = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        '''
        Return the username as string
        '''
        return self.email

    def has_perm(self, perm, obj=None):
        '''
        For checking permissions. to keep it simple all admin have ALL permissons.
        '''
        return self.is_admin

    def has_module_perms(self, app_label):
        '''
        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
        '''
        return True

    def create_aid(self):
        '''
        Generating a unique aid for every applicant
        '''
        not_a_unique_hash = True
        while not_a_unique_hash: # while True
            aid = int(''.join(str(random.randint(10, 99)))+''.join(str(random.randint(100, 999))))
            not_a_unique_hash = self.__class__.objects.filter(aid=aid).exists()
            print(not_a_unique_hash)
        print(not_a_unique_hash, "not_a_unique_hash")
        return aid

    def save(self, *args, **kwargs):
        if not self.pk:
            self.aid=self.create_aid()
        super().save()