def add_admin_perms(models, perm_parts=('add', 'change', 'delete')):
    """Designed to be run from a data migration script,
    adds create, edit and delete permissions to the site admin group"""
    from django.contrib.contenttypes.management import update_contenttypes
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.management import create_permissions
    from django.apps import apps
    from django.contrib.auth.models import Group, Permission

    if not isinstance(models, tuple):
        # Allow single model to be passed in
        models = (models,)

    # First, we need to create permissions in case this hasn't run yet
    # http://andrewingram.net/2012/dec/ \
    # common-pitfalls-django-south/#contenttypes-and-permissions
    app_set = set([model._meta.app_label for model in models])
    for app in app_set:
        app_config = apps.get_app_config(app)
        update_contenttypes(app_config)
        create_permissions(app_config)

    # Get group for site admin
    group, created = Group.objects.get_or_create(name='site admin')

    # Add permissions to the site admin
    for model in models:
        for perm_part in perm_parts:
            codename = "%s_%s" % (perm_part, model._meta.model_name)
            content_type = ContentType.objects.get_for_model(model)
            permission = Permission.objects.get(codename=codename,
                                                content_type=content_type)
            group.permissions.add(permission)

    group.save()
