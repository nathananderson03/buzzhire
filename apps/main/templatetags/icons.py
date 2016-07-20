from django import template
from django.utils.safestring import mark_safe

register = template.Library()


ICON_MAP = {
    'login': 'fa fa-sign-in',
    'logout': 'fa fa-sign-out',
    'register': 'fa fa-user',
    'driver_register': 'fa fa-motorcycle',
    'driver': 'fa fa-motorcycle',
    'undo': 'fa fa-reply',
    'confirm': 'fa fa-check-circle',
    'user': 'fa fa-user',
    'account': 'fa fa-user',
    'forgot': 'fa fa-question-circle',
    'admin': 'fa fa-cogs',
    'edit': 'fa fa-edit',
    'delete': 'fa fa-trash',
    'clear': 'fa fa-times',
    'password': 'fa fa-lock',
    'book': 'fa fa-calendar',
    'date': 'fa fa-calendar',
    'time': 'fa fa-clock-o',
    'reset_password': 'fa fa-undo',
    'dashboard': 'fa fa-dashboard',
    'freelancer_profile_view': 'fa fa-eye',
    'freelancer_profile_change': 'fa fa-edit',
    'client_profile_change': 'fa fa-edit',
    'client': 'fa fa-briefcase',
    'job_request_create': 'fa fa-plus-circle',
    'requested_jobs': 'fa fa-list',
    'freelancer_bookings': 'fa fa-list',
    'availability': 'fa fa-calendar',
    'save': 'fa fa-check-circle',
    'job_matching': 'fa fa-search',
    'create': 'fa fa-plus-circle',
    'vehicletypes': 'sidebar-icon-14',
    'yes': 'fa fa-check',
    'no': 'fa fa-times',
    'location': 'fa fa-map-marker',
    'search': 'fa fa-search',
    'right_arrow': 'fa fa-arrow-circle-right',
    'phone': 'fa fa-phone',
    'pay': 'fa fa-check-circle',
    'photo': 'fa fa-camera-retro',
    'upload': 'fa fa-upload',
    'feedback': 'fa fa-comment-o',
    'score_full': 'fa fa-star',
    'score_empty': 'fa fa-star-o',
    'score_half': 'fa fa-star-half-o',
    'invitation': 'fa fa-paper-plane-o',
    'kitchen': 'fa fa-cutlery',
    'bar': 'fa fa-beer',
    'cleaner': 'fa fa-tint',
    'waiting': 'fa fa-glass',
    'notification': 'fa fa-bell',
    'faq': 'fa fa-question-circle',
    'user-alt': 'user-icon',
    'icon-my-bookings': 'sidebar-icon-1',
    'icon-notification': 'sidebar-icon-2',
    'icon-feedback': 'sidebar-icon-3',
    'icon-cleaner': 'sidebar-icon-4',
    'icon-bar': 'sidebar-icon-5',
    'icon-waiting': 'sidebar-icon-6',
    'icon-driver': 'sidebar-icon-7',
    'icon-kitchen': 'sidebar-icon-8',
    'icon-client_profile_change': 'sidebar-icon-9',
    'icon-password': 'sidebar-icon-10',
    'icon-logout': 'sidebar-icon-11',
    'icon-edit': 'sidebar-icon-9',
    'icon-freelancer_profile_change': 'sidebar-icon-9',
    'icon-photo': 'sidebar-icon-7',
    'icon-confirm': 'sidebar-icon-3',
    'icon-availability': 'sidebar-icon-13',
    'icon-invitations': 'sidebar-icon-12',
    'icon-notification-panel': 'notification-icon-panel',
    'vehicle-yes': 'fa fa-check-circle fa-lg',
    'vehicle-no': 'fa fa-times-circle fa-lg',
    'edit-lg': 'fa fa-edit fa-lg',
    'delete-lg': 'fa fa-trash fa-lg',

}

@register.filter
def icon(name):
    """Outputs icon markup based on the supplied name.
    
    Usage:
    
        {{ 'foo'|icon }}
    """
    if name.startswith( 'icon-'):
        return mark_safe("<span class='%s'></span>" % ICON_MAP[name]);
    else:
        return mark_safe("<i class='%s'></i>" % ICON_MAP[name])
