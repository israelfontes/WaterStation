from django.contrib.auth.decorators import user_passes_test

# Decorador para grupo específico
def group_required(nome_grupo):
    return user_passes_test(lambda u: u.is_authenticated and u.groups.filter(name=nome_grupo).exists())

# Decoradores prontos
group_admin = group_required('ADMIN')
group_manager = group_required('MANAGER')
group_operator = group_required('OPERATOR')
group_viewer = group_required('VIEWER')

# Permitir múltiplos grupos
def any_group_required(*grupos):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name__in=grupos).exists()
    )