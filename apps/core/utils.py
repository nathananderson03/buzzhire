from class_registry import Registry
from collections import OrderedDict


class WeightedRegistry(Registry):
    """A registry that returns registered classes in
    weight order.  The classes that are registered should have
    a 'weight' attribute.
    """
    def __init__(self, *args, **kwargs):
        self._ordered_dict = OrderedDict()
        super(WeightedRegistry, self).__init__(*args, **kwargs)

    def register(self, klass):
        super(WeightedRegistry, self).register(klass)
        key = self._get_key_from_class(klass)
        self._ordered_dict[key] = klass
        self._ordered_dict = OrderedDict(
            sorted(self._ordered_dict.iteritems(),
                   key=lambda item: item[1].weight))

    def __iter__(self):
        return self._ordered_dict.__iter__()

    def values(self):
        return self._ordered_dict.values()


class classproperty(object):
    """Decorator for class-level properties.
    
    Usage:
    
        class MyClass(object):
            @classproperty(cls):
                return cls.something
    """
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def template_names_from_polymorphic_model(model_class, suffix,
                                          subdirectory=''):
    """Returns a list of template names to test for the supplied polymorphic
    model class.
    """
    # Build hierarchy of the model and its parent
    meta_hierarchy = (
        model_class._meta,
        model_class._meta.get_parent_list().pop()._meta,
    )

    template_names = []
    for meta in meta_hierarchy:
        directory = meta.app_label
        if subdirectory:
            directory += '/%s' % subdirectory
        template_names.append(
            "%s/%s%s.html" % (
                directory,
                meta.model_name,
                suffix
            ),
        )
    return template_names
