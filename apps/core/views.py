from django.views.generic.edit import FormView, FormMixin
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
import logging
from .forms import ConfirmForm
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.apps.registry import apps
from .utils import template_names_from_polymorphic_model
from django.http import JsonResponse


# A GBP sign
POUND_SIGN = u'\u00A3'


logger = logging.getLogger('project')


class ContextMixin(object):
    """Views mixin - adds the extra_context attribute
    to the context.
    """
    extra_context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(ContextMixin, self).get_context_data(*args, **kwargs)
        context.update(self.extra_context)
        return context


class ContextTemplateView(ContextMixin, TemplateView):
    """TemplateView that makes it easy to add extra context
    within the url conf.

    Usage:

        url(r'^$', ContextTemplateView.as_view(
                                template_name='template.html',
                                extra_context={'title': 'Title'}),
                                    name='home'),
    """
    pass


class TabsMixin(object):
    """Mixin for adding the tabs to a page context.

    Adds 'tabs' and 'page_title' to the context.

    For child pages of tab pages, you can specify which tab is
    active by setting the active_tab_name attribute to the url name
    of the relevant tab.
    
    Usage:

        class MySectionTabsMixin(TabsMixin):
            tabs = [
                ('Tab one', 'url/for/tab/1/'),
                ('Tab two', 'url/for/tab/2/'),
            ]
    """

    tabs = []
    active_tab_name = ''

    def get_tabs(self):
        "Returns a list of two-tuples for the tabs."
        return self.tabs

    def get_active_tab_name(self):
        "Returns the url of the active tab, to be used for child tabs."
        return self.active_tab_name

    def get_context_data(self, **kwargs):
        context = super(TabsMixin, self).get_context_data(**kwargs)

        context['tabs'] = []

        # Build the tabs from the tabs tuple
        tabs = self.get_tabs()
        active_detected = False
        for title, url in tabs:
            tab = {'title': title,
                    'url': url}
            if tab['url'] == self.request.get_full_path():
                active_detected = True
                # Set this tab as being active
                tab['active'] = True
                context['page_title'] = tab['title']
            elif url == self.get_active_tab_name():
                # Make the tab active for child pages
                tab['active'] = True
            else:
                tab['active'] = False
            context['tabs'].append(tab)
        if not active_detected:
            # Make the first tab active
            context['tabs'][0]['active'] = True

        # Add page title
        for tab in context['tabs']:

                break

        return context


class MultiFormViewMixin(object):
    """View mixin designed to work with multiple forms on the same page.
    Only one form should be submitted.
    
    Usage:
        
        class MyFormView(MultiFormViewMixin, FormView):
            form_classes = {
                FirstFormClass: 'first',
                SecondFormClass: 'second',
            }
     
    """

    def get(self, request, *args, **kwargs):
        # Build all forms passed by get
        forms = {}
        for form_class, prefix in self.form_classes.items():
            forms[prefix] = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(forms=forms))

    def form_invalid(self, form):
        forms = {form.prefix: form}
        for form_class, prefix in self.form_classes.items():
            if prefix != form.prefix:
                forms[prefix] = self.get_form(form_class, suppress_bind=True)
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_form(self, form_class, suppress_bind=False):
        # Pass the form_class to get_form_kwargs
        return form_class(**self.get_form_kwargs(form_class, suppress_bind))

    def get_form_kwargs(self, form_class, suppress_bind=False):
        # Set the prefix on the form
        if suppress_bind:
            # If another form was posted, we don't want to bind the data
            # to the form
            form_kwargs = {}
        else:
            form_kwargs = super(MultiFormViewMixin, self).get_form_kwargs(
                                                                    form_class)
        form_kwargs['prefix'] = self.form_classes[form_class]
        return form_kwargs

    def get_form_class(self, request):
        if request.method == 'POST':
            # Determine which form was posted.
            for form_class, prefix in self.form_classes.items():
                # If the submit button matches the prefix, it was that form
                if '%s_submit' % prefix in request.POST:
                    return form_class
        else:
            # We only use this from the post() method
            raise Exception('MultiFormViewMixin.get_form_class() should ' \
                            'only be called from post().')

    def get_context_data(self, *args, **kwargs):
        context = super(MultiFormViewMixin, self).get_context_data(*args,
                                                                 **kwargs)
        for form_class, prefix in self.form_classes.items():
            context['%s_form' % prefix] = context['forms'][prefix]
        return context


class CanEditObject(object):
    """Views mixin - only allow users who can edit
    the object.
    
    Designed for use with views that extend SingleObjectMixin.
    """

    def get_object(self, *args, **kwargs):
        object = super(CanEditObject, self).get_object(*args, **kwargs)
        if not object.can_edit(self.request.user):
            raise PermissionDenied
        return object


class ConfirmationMixin(FormMixin):
    "Generic confirmation view mixin."

    template_name = 'form_page.html'
    form_class = ConfirmForm
    question = None
    cancel_url = ''
    action_icon = 'confirm'
    cancel_icon = 'undo'

    def get_form_kwargs(self):
        form_kwargs = super(ConfirmationMixin, self).get_form_kwargs()
        form_kwargs.update({
            'cancel_url': self.get_cancel_url(),
            'question': self.get_question(),
            'action_icon': self.action_icon,
            'cancel_icon': self.cancel_icon,
        })
        return form_kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(ConfirmationMixin, self).get_context_data(*args,
                                                                 **kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context

    def get_cancel_url(self):
        "Returns url to link to if they cancel."
        return self.cancel_url

    def get_question(self):
        "Returns question to ask."
        return self.question


class OwnerOnlyMixin(object):
    """Mixin for a DetailView - restricts the view to the user who owns
    the model in question, or a site admin.
    
    By default, 'ownership' is determined by a 'user' field on the model.
    This can be changed by overriding the is_owner() method.
    """
    def is_owner(self):
        "Whether or not the current user should be treated as the 'owner'."
        return self.get_object().user == self.request.user

    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)
        elif not self.request.user.is_admin:
            if not self.is_owner():
                # The user doesn't 'own' the object
                raise PermissionDenied
        return super(OwnerOnlyMixin, self).dispatch(request, *args, **kwargs)


class GrantCheckingMixin(object):
    """Views mixin for checking multiple grants, and allowing other apps
    to register grants too.
    
    A grant is a function that receives the view, and returns True if the
    user can proceed.
    
    # TODO - improve the API for this (decorators?)
    
    Usage:
    
        class MyView(GrantCheckingMixin, DetailView):
            model = MyModel
            grant_methods = ['is_foo']
            
            def is_foo(self):
                # If the user can access the object, return True
            
        # In another app
        
        from apps.myapp.views import MyView
        
        def _is_bar(self):
            # Return True or False
        MyView.is_bar = _is_bar
        MyView.grant_methods.append('is_bar')
    """
    require_login = True  # Whether to require the user is logged in
    allow_admin = True  # Whether to allow admins access
    # List of grant methods on the view class - can also be strings
    grant_methods = []
    # Whether to run self.object = self.get_object() before the grants
    populate_object = True


    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, give them the chance to
        if self.require_login and self.request.user.is_anonymous():
            return redirect_to_login(self.request.path)

        if self.populate_object:
            self.object = self.get_object()

        granted = False
        for method in self.get_grant_methods():
            if method():
                granted = True

        if not granted:
            # None of the grants returned True;
            # Do a final check to see if the user is admin
            if not (self.allow_admin and self.request.user.is_admin):
                raise PermissionDenied

        return super(GrantCheckingMixin, self).dispatch(request, *args,
                                                        **kwargs)

    def get_grant_methods(self):
        """Returns list of grant methods, converting string based methods
        to callable methods.
        """
        methods = []
        for method in self.grant_methods:
            # Convert it to callable
            method = getattr(self, method)
            methods.append(method)
        return methods


class PolymorphicTemplateMixin(object):
    """Views mixin to allow specifying template names for job requests
    to override the template.  For example, if the template_suffix is '_detail'
    and the model is DriverJobRequest, the view will look first for a template
    driver/driverjobrequest_detail.html and then fall back to
    job/jobrequest_detail.html.
    
    It will try to get the model class from the self.object, failing that it
    will use self.model.
    
    Usage:
    
        class MyView(PolymorphicTemplateMixin, FormView):
            model = MyModel
            template_suffix = '_register'
            
    """
    template_suffix = ''

    def get_template_names(self):
        """Give subclassing job requests the chance to override the template,
        falling back to a default.
        """
        # Prefer self.object to the model_class.  This is because for detail
        # views, the model may be the parent class.
        if getattr(self, 'object', None):
            model_class = self.object.__class__
        else:
            model_class = self.model

        return template_names_from_polymorphic_model(model_class,
                                                     self.template_suffix)


class ExtraFormsView(FormView):
    """FormView for handling a main form and a number of extra forms.
    
    Usually you will want to specify the form_class, and override
    get_extra_forms() and form_valid().
    """
    form_class = None
    prefix = 'main'  # The form prefix for the main form

    def get_context_data(self, *args, **kwargs):
        context = super(ExtraFormsView,
                        self).get_context_data(*args, **kwargs)
        context['extra_forms'] = []
        for prefix, form_class in self.extra_forms.items():
            context['extra_forms'].append(self.get_form(form_class, prefix))
        return context

    def get_form(self, form_class, prefix=None):
        # Now is a good time to set the extra_forms too
        self.extra_forms = self.get_extra_forms()
        # Pass the prefix through to get_form_kwargs
        return form_class(**self.get_form_kwargs(prefix))

    def get_extra_forms(self):
        """
            Returns a dictionary of the extra form classes, keyed with their
            form prefixes.
            
            Usage:
            
                def get_extra_forms(self):
                    return {
                        'client': ClientInnerForm,
                    }
        """
        return {}

    def get_form_kwargs(self, prefix=None):
        """Standard get_form_kwargs() method adapted to return
        the extra forms too."""

        if prefix is None:
            # This is for the main form
            prefix = self.get_prefix()

        kwargs = {
            'initial': self.get_initial(),
            'prefix': prefix,
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        "Standard post method adapted to validate all forms."
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.bound_forms = {self.get_prefix(): form}
        for prefix, form_class in self.extra_forms.items():
            self.bound_forms[prefix] = self.get_form(form_class, prefix)

        if all([f.is_valid() for f in self.bound_forms.values()]):
            # If all the forms validate
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Action to perform once the forms validate.
        
        Usage:
        
            def form_valid(self, form):
                instance = form.save()

                # Save extra forms too
                for extra_form in self.bound_forms.items():
                    extra_form.save()

                return self.get_success_url()
        """
        pass


class JSONResponseView(View):
    """
    A views mixin that can be used to render a JSON response.
    """
    def get(self, request, *args, **kwargs):
        context = self.get_data()
        return JsonResponse(context)

    def get_data(self):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        return None
