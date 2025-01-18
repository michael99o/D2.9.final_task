from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post, Category, PostCategory, Subscriber


@receiver(m2m_changed, sender=Post.category.through)
def post_created(action, instance, pk_set, **kwargs):
    if action == 'post_add':
        categories = Category.objects.filter(pk__in=pk_set)

        subscribers = User.objects.filter(
            subscriptions__category__in = categories
        ).distinct()

        subject = f'Новый пост в категориях: {", ".join(cat.get_topic_display() for cat in categories)}'

        text_content = (
            f'{instance.text[:30]}\n'
            f'Полный текст по: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'{instance.text[:30]}<br>'
            f'Полный текст <a href = "http://127.0.0.1:8000{instance.get_absolute_url()}"> здесь </a>'
        )

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(subject, text_content, None, [subscriber.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
