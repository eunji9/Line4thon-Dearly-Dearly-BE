from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_friend_requests',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(from_user=models.F('to_user')),
                name='friendrequest_no_self_request',
            ),
        ]

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.status})"

    @property
    def is_pending(self) -> bool:
        return self.status == self.Status.PENDING
