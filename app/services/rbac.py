def is_admin(user):
    return user.role == 'admin'

def is_manager(user):
    return user.role == 'manager'

def is_warehouse_manager(user, warehouse):
    return warehouse.manager_id == user.id
