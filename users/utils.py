from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated and (u.is_superuser or u.groups.filter(name__in=group_names).exists()):
            return True
        return False
    return user_passes_test(in_groups, login_url='sign-in')  
