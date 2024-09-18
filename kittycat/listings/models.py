from django.db import models
from django.contrib.auth.models import User

# Cat model
class Cat(models.Model):
    cat_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    castrated = models.BooleanField(default=False)
    image1 = models.ImageField(upload_to='cat_pics/', blank=False)
    image2 = models.ImageField(upload_to='cat_pics/', blank=False)
    available = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats', default=1)

    def __str__(self):
        return f"Cat ID: {self.cat_id} - {self.name}"

# UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# AdoptionRequest model
class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Request by {self.user.username} for {self.cat.name} - Status: {self.status}"

# ProfileSettings model
class ProfileSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notification_preferences = models.JSONField(default=dict, blank=True)
    privacy_settings = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Settings for {self.user.username}"

# SearchHistory model
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Search History"
        verbose_name_plural = "Search Histories"
        unique_together = ('user', 'cat')

    def __str__(self):
        return f"{self.user.username} searched for {self.cat.name} on {self.date_added}"
