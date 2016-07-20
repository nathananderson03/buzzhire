from apps.core.views import JSONResponseView


class GetMinPayJson(JSONResponseView):
    """Returns the minimum pay so the front end can 
    update the client pay widget.
    """
    def get_data(self):
        return {'foo': 'bar'}
