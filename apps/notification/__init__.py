"""The notification app is responsible for handling sending notifications
by various means to users.

Specifically, it defines a Notification model, and sends push requests when
Notifications are created.

It also provides the ability to send sms to users.

This app could do with some more thought.  At the moment, the Notification model
is tightly coupled with push notifications (a push notification is sent
whenever a Notification is created), but not with sms and email.

There is also no ability for users to control how they get notified.

"""