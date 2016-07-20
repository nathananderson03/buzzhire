from django.shortcuts import redirect
from django.contrib import messages
from .models import get_job_requests_awaiting_feedback_for_client


class FeedbackMiddleware(object):
     """Feedback-related middleware.
     """
     def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated() and request.user.is_client:
            # If they're booking a freelancer, make sure they have cleared their
            # feedback backlog first.
            if view_func.func_name == 'JobRequestCreate':
                if get_job_requests_awaiting_feedback_for_client(
                                                request.user.client).exists():
                    messages.warning(request,
                        'Before you book another freelancer, please leave '
                        'feedback on these jobs.')
                    return redirect('client_backlog')
