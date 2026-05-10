from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('أمومة', 'أمومة'),
        ('البيت', 'البيت'),
        ('تكنولوجيا', 'تكنولوجيا'),
        ('أزياء', 'أزياء'),
        ('مشاعر وعمل', 'مشاعر وعمل'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='أمومة')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)  # فقط الاسم
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"تعليق بواسطة {self.name}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"رسالة من {self.name}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"بروفايل {self.user.username}"
@receiver(post_save, sender=User)

def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, verbose_name="اسم الموقع")
    maintenance_mode = models.BooleanField(default=False, verbose_name="وضع الصيانة")
    contact_email = models.EmailField(verbose_name="بريد التواصل")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="شعار الموقع")

    def __str__(self):
        return "إعدادات الموقع"

    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "الإعدادات"