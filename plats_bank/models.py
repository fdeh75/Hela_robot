from django.db import models

# Create your models here.
from slugify import slugify, Slugify, UniqueSlugify


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Namn")
    slug = models.CharField(max_length=50, blank=True)
    lau_2_code_2015 = models.CharField(max_length=6, verbose_name='Municipality codes',blank=False, unique=True)

    class Meta:
        verbose_name = 'post ort'
        verbose_name_plural = 'post orts'

    def __str__(self):
        return self.name

    def my_unique_check(self, text, uids):
        if text in uids:
            return False
        return not City.objects.filter(slug=text).exists()

    def save(self, *args, **kwargs):
        if not self.slug:
            custom_slugify = Slugify(to_lower=True)
            custom_slugify.separator = '_'
            self.slug = custom_slugify(str(self.name))
        super().save(*args, **kwargs)


class Job_type(models.Model):
    name = models.CharField(max_length=50, verbose_name="Arbets yrken")
    af_id = models.CharField(max_length=30, verbose_name="AF code", unique=True)
    definition = models.TextField(verbose_name='Beskrivning', blank=True)
    ssyk_code_2012 = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'Arbets yrken'
        verbose_name_plural = 'Arbets yrken'

    def __str__(self):
        return self.name


class Job_ad(models.Model):
    af_id = models.IntegerField(unique=True)
    application_deadline = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ad_url = models.URLField(blank=True)
    city =models.ForeignKey('City', on_delete=models.CASCADE,verbose_name='Arbets ort')
    job_type = models.ForeignKey('Job_type', on_delete=models.CASCADE, verbose_name='Yrke')

    class Meta:
        verbose_name = 'Jobb annons'
        verbose_name_plural = 'Jobb annonser'

    def __str__(self):
        return self.title
