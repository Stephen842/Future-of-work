from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from embed_video.fields import EmbedVideoField


# Create your models here.
User = get_user_model()

class Badge(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tier = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="badges/icons/", null=True, blank=True)
    rank = models.PositiveIntegerField(unique=True, default=1)
    min_level = models.PositiveIntegerField(default=1)  # Lowest level of range
    max_level = models.PositiveIntegerField(default=6)  # Highest level of range

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    POD_CHOICES = [
        ("Creator", "Creator"),
        ("Builder", "Builder"),
        ("Educator", "Educator"),
        ("Community", "Community"),
    ]

    GOAL_CHOICES = [
        ("Get Skilled", "Get Skilled"),
        ("Build Projects", "Build Projects"),
        ("Find Work", "Find Work"),
        ("Collaborate", "Collaborate"),
    ]

    ### Personal
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Future of Work Custom Fields
    pod = models.CharField(max_length=64, choices=POD_CHOICES, blank=True)
    goal = models.CharField(max_length=128, choices=GOAL_CHOICES, blank=True)

    # Gamification
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    completed_lessons = models.PositiveIntegerField(default=0)
    streak_current = models.PositiveIntegerField(default=0)
    streak_best = models.PositiveIntegerField(default=0)
    last_active_day = models.DateField(default=timezone.now)

    # Breakdown experience
    xp_learn = models.PositiveIntegerField(default=0)
    xp_do = models.PositiveIntegerField(default=0)
    xp_earn = models.PositiveIntegerField(default=0)

    # Badges (Many-to-Many)
    badges = models.ManyToManyField(Badge, blank=True, related_name="users")

    # Referrals
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.CharField(max_length=10, blank=True, null=True, db_index=True)


    # Web3
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    wallet_connected = models.BooleanField(default=False)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} profile"
    
    def update_level(self):
        self.level = (self.xp // 100) + 1
        self.save(update_fields=["level"])

    def update_streak(self):
        today = timezone.now().date()
        if self.last_active_day == today - timedelta(days=1):
            self.streak_current += 1
        elif self.last_active_day < today - timedelta(days=1):
            self.streak_current = 1
        self.streak_best = max(self.streak_best, self.streak_current)
        self.last_active_day = today
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Lesson(models.Model):
    POD_CHOICES = UserProfile.POD_CHOICES
    pod = models.CharField(max_length=64, choices=POD_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = EmbedVideoField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    locked = models.BooleanField(default=False)
    do_type = models.CharField(max_length=50, blank=True)  # quiz, upload, instruction
    earn_type = models.CharField(max_length=50, blank=True)  # xp, badge, contact
    xp_amount = models.PositiveIntegerField(default=0)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    certificate_enabled = models.BooleanField(default=False)
    prerequisites = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __str__(self):
        return f"{self.pod} - {self.title}"
    
    def is_unlocked_for_user(self, user):
        '''
        Returns True if the user has completed all prerequisite lessons.
        If `locked=True` on the lesson, this will always return False.
        '''
        if self.locked:
            return False

        completed_ids = LessonProgress.objects.filter(
            user=user,
            completed=True
        ).values_list("lesson_id", flat=True)

        return all(prereq.id in completed_ids for prereq in self.prerequisites.all())


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    quiz_score = models.PositiveIntegerField(null=True, blank=True)
    file_submission = models.FileField(upload_to='lesson_uploads/', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')
        indexes = [
            models.Index(fields=['user', 'lesson']),
        ]


class Waitlist(models.Model):
    USER_STATUS = [
        ('', 'Select your status...'),
        ('tutee', 'Student'),
        ('tutor', 'Educator'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField( blank=False, unique=True, 
        error_messages={
            'unique': "Email Address already exists."
        }
    )
    phone = PhoneNumberField(unique=True, 
        error_messages={
            'unique': "Phone number already exists."
        }
    )
    country = CountryField(blank_label='Select your country')
    user_type = models.CharField(max_length=20, choices=USER_STATUS, default="")



class Future_Of_Work(models.Model):
    COURSE_CHOICES = [
        ('', 'Select course type...'),
        ('web3', 'Web3 Fundamentals'),
        ('dao', 'DAO Governance'),
        ('metaverse', 'Metaverse Collaboration'),
        ('blockchain', 'Blockchain Development'),
    ]

    PLAN_CHOICES = [
        ('', 'Select plan...'),
        ('basic', 'Basic Plan'),
        ('pro', 'Pro Plan'),
        ('exclusive', 'Exclusive'),
    ]

    EXPERTISE_CHOICES = [
        ('', 'Select your level...'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("failed", "Failed"),
    ]

    PAYMENT_GATEWAYS = [
        ("helio", "Helio"),
        ("paystack", "Paystack"),
        ("opay", "OPay"),
    ]

    PLAN_FEES = {
        'basic': Decimal("0.00"),
        'pro': Decimal("2.00"),
        'exclusive': Decimal("20.00")
    }
    

    name = models.CharField(max_length=50)
    email = models.EmailField(
        blank=False,
        unique=True, 
        error_messages={
            'unique': "Email Address already exists."
        }
    )
    phone = PhoneNumberField(
        unique=True, 
        error_messages={
            'unique': "Phone number already exists."
        }
    )
    country = CountryField(blank_label='Select your country')
    course_type = models.CharField(max_length=20, choices=COURSE_CHOICES, default="")
    plan_preference = models.CharField(max_length=20, choices=PLAN_CHOICES, default="")
    expertise = models.CharField(max_length=20, choices=EXPERTISE_CHOICES, default="")
    transaction_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_url = models.URLField(null=True, blank=True)

    fee = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    gateway = models.CharField(max_length=20, choices=PAYMENT_GATEWAYS, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Automatically assign fee based on selected plan."""
        self.fee = self.PLAN_FEES.get(self.plan_preference, Decimal("0.00"))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.course_type}"