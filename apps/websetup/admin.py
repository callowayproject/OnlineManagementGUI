from django.contrib import admin
from models import Command, Service, ServerOS, ServiceCommand, ServicePackage, \
                    Server, LanguageLibrary

class CommandInline(admin.TabularInline):
    """
    Inline listing for Service commands
    """
    model = Command

class ServiceAdmin(admin.ModelAdmin):
    inlines = [CommandInline,]

admin.site.register(Service, ServiceAdmin)

class ServiceCommandInline(admin.TabularInline):
    """
    Inline mapping of service commands to os
    """
    model = ServiceCommand


class ServicePackageInline(admin.TabularInline):
    """
    Inline mapping of os to packages for services
    """
    model = ServicePackage


class ServerOSAdmin(admin.ModelAdmin):
    inlines = [ServiceCommandInline, ServicePackageInline, ]

admin.site.register(ServerOS, ServerOSAdmin)

class ServerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Server, ServerAdmin)

class LanguageLibraryAdmin(admin.ModelAdmin):
    pass

admin.site.register(LanguageLibrary, LanguageLibraryAdmin)