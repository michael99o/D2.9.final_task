from datetime import timedelta
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives

from news.models import *

logger = logging.getLogger(__name__)


def my_job():
    posts = Post.objects.filter(date__gte = timezone.now()-timedelta(days=60))
    categories = set(posts.values_list('category', flat=True))
    subscribers = set(User.objects.filter(subscriptions__category__in=categories))

    for subscriber in subscribers:
        post_list = set(posts.filter(category__in = subscriber.categories.all()))
        html_content = render_to_string(
            'daily_post.html',
            {
                'link': settings.SITE_URL,
                'post_list': post_list,
            }
        )
        msg = EmailMultiAlternatives(
            subject = 'Статьи за неделю',
            body = '',
            from_email= settings.DEFAULT_FROM_EMAIL,
            to = [subscriber.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()




@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri',hour="18", minute="00", timezone="UTC"),
            # trigger=CronTrigger(second="*/5"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")