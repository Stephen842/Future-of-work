from django.utils import timezone
from django.db import transaction

from .models import LessonProgress, Badge

@transaction.atomic
def complete_lesson_for_user(user, lesson):
    '''
    Handles the full lesson completion flow:
    - Marks lesson as completed
    - Awards XP
    - Updates streak
    - Updates level
    - Awards badge if eligible
    '''

    profile = user.profile

    progress, created = LessonProgress.objects.get_or_create(
        user=user,
        lesson=lesson
    )

    if progress.completed:
        return False  # Idempotent safety

    # 1. Mark lesson completed
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save(update_fields=["completed", "completed_at"])

    # 2. Award XP (data-driven)
    xp_amount = lesson.xp_amount or 0
    profile.xp += xp_amount
    profile.completed_lessons += 1

    # 3. Update streak
    profile.update_streak()

    # 4. Update level
    new_level = (profile.xp // 100) + 1
    if new_level != profile.level:
        profile.level = new_level

    profile.save(
        update_fields=[
            "xp",
            "level",
            "completed_lessons",
            "streak_current",
            "streak_best",
            "last_active_day",
        ]
    )

    # 5. Badge evaluation (rank-based progression)
    eligible_badge = (
        Badge.objects.filter(
            min_level__lte=profile.level,
            max_level__gte=profile.level
        ).order_by("rank").first()
    )

    if eligible_badge:
        current_rank = (
            profile.badges.order_by("-rank").first().rank
            if profile.badges.exists()
            else 0
        )

        if eligible_badge.rank == current_rank + 1:
            profile.badges.add(eligible_badge)

    return True