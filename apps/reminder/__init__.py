"""The reminder app is responsible for sending out reminders to users,
for example to tell a freelancer that their job starts in one hour.

It could do with some improvement around its handling of making sure reminders
are not triggered if they become invalid (e.g. if the job request is
rescheduled).  The approach of using ScheduledReminderSet
objects works in most cases but would probably be better rethought to use
Huey's revocation API:
http://huey.readthedocs.org/en/latest/getting-started.html#canceling-a-normal-task-or-one-scheduled-in-the-future 

"""
default_app_config = 'apps.reminder.config.ReminderConfig'