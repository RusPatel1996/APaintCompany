from django.contrib import admin
from api.models import Customer, Employee, Inventory, Role, Permission, Property, PropertyAssignment

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name']
admin.site.register(Customer)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'age']
admin.site.register(Employee, EmployeeAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['color', 'status', 'quantity', 'last_updated']
admin.site.register(Inventory, InventoryAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ['role']
admin.site.register(Role, RoleAdmin)

# class EmployeeRoleAdmin(admin.ModelAdmin):
#     list_display = ['employee', 'role', 'last_updated']
# admin.site.register(EmployeeRole, EmployeeRoleAdmin)

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission']
admin.site.register(Permission, PermissionAdmin)

# class EmployeePermissionAdmin(admin.ModelAdmin):
#     list_display = ['employee', 'permission', 'last_updated']
# admin.site.register(EmployeePermission, EmployeePermissionAdmin)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_type']
admin.site.register(Property, PropertyAdmin)

class PropertyAssignmentAdmin(admin.ModelAdmin):
    list_display = ['property', 'employee', 'status']
admin.site.register(PropertyAssignment, PropertyAssignmentAdmin)
