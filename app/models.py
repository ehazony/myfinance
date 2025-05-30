# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Represents a chat session for a user."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Conversation {self.pk} for {self.user}"


class Message(models.Model):
    """Single chat message supporting rich types."""

    USER = "user"
    AGENT = "agent"

    TEXT = "text"
    IMAGE = "image"
    BUTTONS = "buttons"
    CHART = "chart"

    SENDER_CHOICES = [
        (USER, "User"),
        (AGENT, "Agent"),
    ]

    CONTENT_TYPE_CHOICES = [
        (TEXT, "Text"),
        (IMAGE, "Image"),
        (BUTTONS, "Buttons"),
        (CHART, "Chart"),
    ]

    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content_type = models.CharField(max_length=20, default="text")
    payload = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="sent")

    class Meta:
        ordering = ["timestamp"]

    def __str__(self) -> str:
        return f"{self.sender} - {self.payload}"


class OrchestratorIntent(models.Model):
    """Mapping from intent key to agent name."""

    key = models.CharField(max_length=64, unique=True)
    agent = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.key


