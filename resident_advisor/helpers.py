

def has_model_permissions(entity, model, perms, app, instance=None):

    if not isinstance(perms, list):
        perms = [perms, ]

    for perm in perms:

        # Check if the User has the ability to edit all
        if not entity.has_perm("%s.%s_%s" % (app, perm, model.__name__)):
            return False

        if instance:
            # Check if Model has permissions check
            if hasattr(instance, 'has_%s_permissions' % perm):
                # Check if the User can edit this item
                if not getattr(instance, 'has_%s_permissions' % perm)(entity):
                    return False

    return True