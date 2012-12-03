from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from socializer.settings import SOCIALIZER_AUTO_TAKEDOWN
from socializer.settings import SOCIALIZER_AUTO_TAKEDOWN_TRIGGER
from socializer.signals import socializer_auto_takedown


class CommentManager(models.Manager):
    def public(self):
        return super(CommentManager, self).get_query_set().filter(visible=True)


class Comment(models.Model):
    """
    A Comment is a simple message that a user can leave on an object.
    """
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    text = models.CharField(max_length=500)
    visible = models.BooleanField(default=True)

    objects = CommentManager()

    def __unicode__(self):
        return u'%s commented on: %s' % (self.user.get_full_name(), self.content_object.__unicode__())

    class Meta:
        ordering = ['timestamp']


class Recommendation(models.Model):
    """
    A Recommendation is a simple notion that a user can leave on a given object
    to indicate how well they liked a particular piece of content.
    """
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __unicode__(self):
        return '%s recommends: \'%s\'' % (self.user.get_full_name(), self.content_object.__unicode__())


class Flag(models.Model):
    """
    A Flag is a simple notion that a user can make to mark a piece of content
    as being inappropriate.
    """
    user = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return u'%s flagged: %s' % (self.user.get_full_name(), self.content_object.__unicode__())

    class Meta:
        ordering = ['timestamp']
        unique_together = ('user', 'content_type', 'object_id')

    def save(self, *args, **kwargs):
        super(Flag, self).save(*args, **kwargs)

        if SOCIALIZER_AUTO_TAKEDOWN:
            if Flag.objects.filter(content_type=self.content_type, object_id=self.object_id).count() >= SOCIALIZER_AUTO_TAKEDOWN_TRIGGER:
                try:
                    self.content_object.socializer_takedown()

                    # Emit a signal to indicate that a piece of content has been taken down
                    socializer_auto_takedown.send(sender=self, data='')
                except AttributeError:
                    pass


class Nudge(models.Model):
    """
    A Nudge represents a simple notion that a user can make on a piece of
    given content, to indicate they want the owner to do something to that content.
    """
    user = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __unicode__(self):
        return u'%s nudged: %s' % (self.user.get_full_name(), self.content_object.__unicode__())
