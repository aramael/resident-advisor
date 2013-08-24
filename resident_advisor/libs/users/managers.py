from django.contrib.auth.models import UserManager


class UserManager(UserManager):

    actions = ['delete_items', ]

    @property
    def bulk_actions(self):

        output_actions = []

        for action in self.actions:

            action_func = getattr(self, action)
            description = getattr(action_func, 'short_description', action.replace('_', ' '))

            output_actions.append({
                'action': action,
                'func': action_func,
                'description': description,
            })

        return output_actions

    def process_bulk_actions(self, action, queryset):
        if action in self.actions:
            function = getattr(self, action)
            return function(queryset)

    def delete_items(self, queryset):
        for item in queryset:
            item.delete()
    delete_items.short_description = 'Delete Selected Items'