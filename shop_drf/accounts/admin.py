from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import User,OtpCode


class UserAdmin(UserBaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number','email','is_active','is_admin')
    list_filter = ('is_admin','is_active')

    fieldsets = (
        ('Specification',{'fields':('phone_number','email','full_name','password')}),
        ('Permissions',{'fields':('is_superuser','is_admin','is_active','last_login','groups','user_permissions')})
    )

    add_fieldsets = (
        ('Specification',{'fields':('phone_number','email','full_name','password','password2')}),
    )

    filter_horizontal = ['groups','user_permissions']
    ordering = ('is_admin','is_active')
    readonly_fields = ('last_login',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request,obj,**kwargs)
        is_superuser = request.user.is_superuser
        is_admin = request.user.is_admin
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True

        if is_admin:
            form.base_fields['is_admin'].disabled = True

        return form


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created')


admin.site.register(User,UserAdmin)



