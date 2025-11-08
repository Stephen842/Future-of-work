from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Badge(models.Model):
    BADGE_TIER_CHOICES = [
        ("Diamond", "Diamond"),
        ("Platinum", "Platinum"),
        ("Gold", "Gold"),
        ("Silver", "Silver"),
        ("Bronze", "Bronze"),
        ("Iron", "Iron"),
    ]
       
    name = models.CharField(max_length=50, choices=BADGE_TIER_CHOICES, unique=True)

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
    last_active_day = models.DateField(auto_now_add=True)

    # Breakdown experience
    xp_learn = models.PositiveIntegerField(default=0)
    xp_do = models.PositiveIntegerField(default=0)
    xp_earn = models.PositiveIntegerField(default=0)

    # Badges (Many-to-Many)
    badges = models.ManyToManyField(Badge, blank=True, related_name="users")

    # Referrals
    referral_code = models.CharField(max_length=32, blank=True, null=True)
    referred_by = models.CharField(max_length=32, blank=True, null=True)


    # Web3
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    wallet_connected = models.BooleanField(default=False)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} profile"
    
    def update_level(self):
        self.level = (self.xp // 100) + 1
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically add default badge if user has no badges yet
        if not self.badges.exists():
            default_badge = Badge.objects.get(name="Iron")
            self.badges.add(default_badge)
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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