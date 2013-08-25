

def has_model_permissions(entity, perms, instance):

    if not isinstance(perms, list):
        perms = [perms, ]
    if not isinstance(instance, list):
        instances = [instance, ]
    else:
        instances = instance

    for perm in perms:
        for instance in instances:
            # Check if Model has permissions check
            if hasattr(instance, 'has_%s_permissions' % perm):
                # Check if the User can edit this item
                if getattr(instance, 'has_%s_permissions' % perm)(entity):
                    return True

    return False