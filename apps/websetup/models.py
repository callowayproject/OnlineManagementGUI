from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import fabfile


SERVER_USE_CHOICES = (
    ('TEST',_('Testing')),
    ('STAGE',_('Staging')),
    ('PROD',_('Production')),
    ('DEMO',_('Demonstration')),
)

URL_CHOICES = (
    ('rsync', 'Rsync Server Path'),
    ('targz', 'tar.gz Path'),
    ('git', 'Git Repository'),
    ('svn', 'Subversion Repository'),
    ('bzr', 'Bazaar Repository'),
    ('hg', 'Mercurial Repository'),
)

PRG_LANGUAGES_CHOICES = (
    ('java', 'Java'),
    ('perl', 'Perl'),
    ('php', 'PHP'),
    ('python', 'Python'),
    ('ruby', 'Ruby'),
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
    install_cmd = models.CharField(_('install package command'), max_length=200)
    list_installed_cmd = models.CharField(_('list installed packages cmd'), max_length=200)
    
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
    package = models.CharField(_('package'), 
        max_length=255, 
        help_text="Which package(s) are required to be installed. " \
                  "Separate multiple packages by a space.")
    
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
    cmd_string = models.CharField(_('command string'), 
        max_length=255, 
        help_text="The command string for this operating system.")
    must_sudo = models.BooleanField(_('must sudo'), 
        default=True)
    
    class Meta:
        unique_together = (('command', 'server_os'),)
    
    def __unicode__(self):
        return self.cmd_string

class LanguageLibrary(models.Model):
    """
    A library for a language, installed typically with a language-specific command
    """
    language = models.CharField(_('programming language'), 
        max_length=50, 
        choices=PRG_LANGUAGES_CHOICES)
    name = models.CharField(_('name'), 
        max_length=50)
    install_cmd = models.CharField(_('install command'), 
        max_length=255)
    check_installed_cmd = models.CharField(_('check installed command'), 
        max_length=255)
    must_sudo = models.BooleanField(_('must sudo'), 
        default=True)
    
    class Meta:
        verbose_name_plural=_('language libraries')
        unique_together = ('language','name')
    
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
    password = models.CharField(_('password'), 
        max_length=128, 
        blank=True,
        null=True,
        help_text="The password is encrypted when saved.")
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
    has_def_svc = models.BooleanField(_('has default services'), default=True)
    has_def_lib = models.BooleanField(_('has default libraries'), default=True)
    
    def __unicode__(self):
        return self.name
    
    
    def check_default_services(self, install_missing=False):
        """
        Check that this server has all default services installed
        """
        
        list_installed_cmd = self.server_os.list_installed_cmd
        install_cmd = self.server_os.install_cmd
        
        for svc in self.default_services.all():
            pkg = ServicePackage.objects.get(service=svc, server_os=self.server_os)
            try:
                has_default_services = fabfile.has_package(list_installed_cmd, pkg.package, \
                                            host_string=self.address, user=self.login, password=self.decrypt_password())
                if has_default_services:
                    continue
                elif install_missing:
                    fabfile.install_package(install_cmd, pkg.package, \
                                            host_string=self.address, user=self.login, password=self.decrypt_password())
                else:
                    return False
            except SystemExit, err:
                return False
        return True
    
    
    def check_default_libraries(self, install_missing=False):
        """
        Check that this server has all default libraries installed
        """
        for lib in self.default_libraries.all():
            try:
                success = fabric.run_or_sudo(lib.check_installed_cmd, sudo=False, \
                                    host_string=self.address, user=self.login, password=self.decrypt_password())
                if success:
                    continue
                elif install_missing:
                    success = fabric.run_or_sudo(lib.install_cmd, lib.must_sudo, \
                                        host_string=self.address, user=self.login, password=self.decrypt_password())
            except SystemExit, err:
                return False
        return True
    
    def save(self, force_insert=False, force_update=False):
        self.has_def_svc = self.check_default_services(install_missing=True)
        self.has_def_lib = self.check_default_libraries(install_missing=True)
        super(Server, self).save(force_insert, force_update)

    def encrypt_password(self):
        """
        Encrypt the password in the object.
        """
        from django.conf import settings
        password = self.password
        from Crypto.Cipher import AES
        input_vector = User.objects.make_random_password(length=16, allowed_chars='0123456789abcdef') # Get a random 32 byte hex string
        key = settings.SECRET_KEY.encode('hex')[:32]
        crypt = AES.new(key, AES.MODE_CFB, input_vector)
        cipher = crypt.encrypt(password).encode('hex')
        password = input_vector+cipher
        self.password = password
    
    
    def decrypt_password(self):
        """
        Decrypt the password and return it
        """
        from django.conf import settings
        password = self.password
        from Crypto.Cipher import AES
        #Get a random input vector
        input_vector = password[:16]
        key = settings.SECRET_KEY.encode('hex')[:32]
        cipher = password[16:].decode('hex')
        crypt = AES.new(key, AES.MODE_CFB, input_vector)
        plaintext = crypt.decrypt(cipher)
        return plaintext
        

class WebSite(models.Model):
    """
    A web site that is on one or more servers
    """
    
    name = models.CharField(_("name"), 
        max_length=255)
    description = models.TextField(_("description"), 
        blank=True)
    master_url = models.CharField(_("master url"), 
        max_length=255, 
        help_text="Where to find the web site code to deploy.")
    url_type = models.CharField(_("url type"), 
        max_length=10, 
        choices=URL_CHOICES,
        help_text="How the web site will be deployed")
    pre_install_script = models.CharField(_("pre-install script"), 
        blank=True, 
        max_length=255, 
        help_text="Path to a file on the remote server to execute before web site files are copied to server.")
    sudo_pre_install = models.BooleanField(_("Sudo the pre-install script"), 
        default=True)
    post_install_script = models.CharField(_("post-install script"), 
        blank=True, 
        max_length=255, 
        help_text="Path to a file on the remote server to execute after web site files are copied to server.")
    sudo_post_install = models.BooleanField(_("Sudo the post-install script"), 
        default=True)
    pre_update_script = models.CharField(_("pre-deploy script"), 
        blank=True, 
        max_length=255, 
        help_text="Path to a file on the remote server to execute before updating.")
    sudo_pre_update = models.BooleanField(_("Sudo the pre-update script"), 
        default=True)
    post_update_script = models.CharField(_("post-update script"), 
        blank=True, 
        max_length=255, 
        help_text="Path to a file on the remote server to execute after updating.")
    sudo_post_update = models.BooleanField(_("Sudo the post-update script"), 
        default=True)
    dependent_libs = models.ManyToManyField(LanguageLibrary)
    dependent_svcs = models.ManyToManyField(Service)
    servers = models.ManyToManyField(Server)
    
    class Meta:
        verbose_name = _("Web Site")
        verbose_name_plural = _("Web Site")
        # abstract = True
        # db_table = 
        # get_latest_by = ""
        # managed = False
        # order_with_respect_to = ""
        # ordering = ["",]
        # permissions = (("permission_name", "Permission Name"),)
        # proxy = True
        # unique_together = ("", "")
    
    def __unicode__(self):
        return self.name

