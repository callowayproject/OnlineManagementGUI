from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _


SERVER_USE_CHOICES = (
    ('TEST',_('Testing')),
    ('STAGE',_('Staging')),
    ('PROD',_('Production')),
    ('DEMO',_('Demonstration')),
)


class Service(models.Model):
    """
    A service that runs on a server. It has multiple commands
    """
    name = models.CharField(_('name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    
    def __unicode__(self):
        return self.name


class Command(models.Model):
    """
    Commands for a service
    """
    name = models.CharField(_('name'), max_length=25)
    description = models.CharField(_('description'), blank=True, null=True, max_length=255)
    service = models.ForeignKey(Service)
    
    class Meta:
        unique_together=(('name', 'service'),)
    
    def __unicode__(self):
        return u"%s %s" % (self.service, self.name)


class ServerOS(models.Model):
    """
    Operating system
    """
    name = models.CharField(_('name'), max_length=50, primary_key=True)
    install_cmd = models.CharField(_('install command'), max_length=200)
    
    class Meta:
        verbose_name = u'Server OS'
        verbose_name_plural = u'Server OSes'
    
    def __unicode__(self):
        return self.name


class ServicePackage(models.Model):
    """
    A package that is installed on an OS that contains a service
    """
    service = models.ForeignKey(Service)
    server_os = models.ForeignKey(ServerOS)
    package = models.CharField(_('package'), max_length=255, help_text="Which package(s) are required to be installed. Separate multiple packages by a space.")
    
    class Meta:
        unique_together = (('service', 'server_os'),)
    
    def __unicode__(self):
        return self.package


class ServiceCommand(models.Model):
    """
    Commands for services based on the operating system
    """
    command = models.ForeignKey(Command)
    server_os = models.ForeignKey(ServerOS)
    cmd_string = models.CharField(_('command string'), max_length=255, help_text="The command string for this operating system.")
    must_sudo = models.BooleanField(_('must sudo'), default=True)
    
    class Meta:
        unique_together = (('command', 'server_os'),)
    
    def __unicode__(self):
        return self.cmd_string

class LanguageLibrary(models.Model):
    """
    A library for a language, installed typically with a language-specific command
    """
    
    name = models.CharField(_('name'), max_length=255)
    install_cmd = models.CharField(_('install command'), max_length=255)
    must_sudo = models.BooleanField(_('must sudo'), default=True)
    
    class Meta:
        verbose_name_plural=_('language libraries')
    def __unicode__(self):
        return self.name


class Server(models.Model):
    """
    A machine with services and web sites
    """
    address = models.CharField(_('address'), 
        primary_key=True, 
        help_text="Can be in the form of IP address, DNS name, or user@address.",
        max_length=100,
    )
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    login = models.CharField(_('login'), 
        max_length=50,
        blank=True,
        null=True,
        help_text="This isn't required if you specified it in the address, or you are using shared ssh keys.",
    )
    server_use = models.CharField(_('server use'), 
        max_length=5,
        blank=True,
        null=True,
        choices=SERVER_USE_CHOICES,
        help_text='Is this a production server?',
    )
    server_os = models.ForeignKey(ServerOS,
        help_text="What type of operating system is installed on this server?",
    )
    default_services = models.ManyToManyField(Service, blank=True, verbose_name=_('Default Services'))
    default_libraries = models.ManyToManyField(LanguageLibrary, blank=True, verbose_name=_('Default Language Libraries'))
    
    
    def __unicode__(self):
        return self.name

    