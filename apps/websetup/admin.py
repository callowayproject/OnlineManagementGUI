from django.contrib import admin
from django import forms
from models import Command, Service, ServerOS, ServiceCommand, ServicePackage, \
                    Server, LanguageLibrary, WebSite

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


class ServerAdminForm(forms.ModelForm):
    orig_password = forms.CharField(widget=forms.HiddenInput, max_length=128, required=False)
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                initial=None, error_class=forms.util.ErrorList, label_suffix=':',
                empty_permitted=False, instance=None):
        if instance is not None:
            pword = instance.password
            initial_data = {'orig_password': pword}
        else:
            initial_data = {'orig_password': ''}
        
        if initial is not None:
            initial_data.update(initial)
        
        super(ServerAdminForm, self).__init__(data, files, auto_id, prefix,
                                    initial_data, error_class, label_suffix, 
                                    empty_permitted, instance)
    
    class Meta:
        model=Server

class ServerAdmin(admin.ModelAdmin):
    form = ServerAdminForm
    exclude = ['orig_password',]
    
    def save_model(self, request, obj, form, change):
        """
        Check if we need to encrypt the password before saving
        """
        print form.cleaned_data
        if change and form.cleaned_data['orig_password'] != form.cleaned_data['password']:
            obj.encrypt_password()
        obj.save()


admin.site.register(Server, ServerAdmin)

class LanguageLibraryAdmin(admin.ModelAdmin):
    pass

admin.site.register(LanguageLibrary, LanguageLibraryAdmin)

class LanguageLibraryInline(admin.TabularInline):
    model=LanguageLibrary


class ServerInline(admin.TabularInline):
    model = Server

class ServiceInline(admin.TabularInline):
    model = Service

class WebSiteAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    # inlines = [LanguageLibraryInline, ServiceInline, ServerInline]

admin.site.register(WebSite, WebSiteAdmin)
