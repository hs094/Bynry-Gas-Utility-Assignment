from django.db import models
from django.contrib.auth.models import User
from services.models import ServiceRequest

class SupportTicket(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='support_tickets'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    description = models.TextField()
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket #{self.id} - {self.service_request.service_type.name}"

class CustomerInteraction(models.Model):
    INTERACTION_TYPES = [
        ('CALL', 'Phone Call'),
        ('EMAIL', 'Email'),
        ('CHAT', 'Live Chat'),
        ('PORTAL', 'Customer Portal'),
    ]

    support_ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_interactions'
    )
    support_rep = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rep_interactions'
    )
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.interaction_type} interaction for Ticket #{self.support_ticket.id}"
