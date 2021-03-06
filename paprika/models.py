from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib import admin
from django import forms

class BusinessProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True, related_name='business')
  business_name = models.CharField(max_length=100, blank=False)
  deleted = models.BooleanField(default=False)
  def __unicode__(self):
    return self.business_name

class Flow(models.Model):
  flow_name = models.CharField(max_length=100)
  owner = models.ForeignKey(BusinessProfile, related_name="flows")
  deleted = models.BooleanField(default=False)
  def sorted_stages(self):
    return self.stages.order_by('stage_num')
  def __unicode__(self):
    return "Flow " + self.flow_name

class Stage(models.Model):
  title = models.CharField(max_length=100)
  description = models.CharField(max_length=200)
  stage_num = models.IntegerField(default=1)
  flow = models.ForeignKey(Flow, related_name="stages")
  notes = models.CharField(max_length=300, blank=True)
  deleted = models.BooleanField(default=False)
  def __unicode__(self):
    return self.title 

class Order(models.Model):
  flow = models.ForeignKey(Flow, related_name="flows")
  merchant = models.ForeignKey(BusinessProfile, related_name="orders")
  current_stage = models.ForeignKey(Stage, blank=True, null=True)
  cust_name = models.CharField(max_length=50)
  cust_phone = PhoneNumberField()
  cust_email = models.EmailField(max_length=254)
  time_entered = models.DateTimeField(auto_now_add=True)
  STATE_CHOICES = (
    ('current', 'current'),
    ('done', 'done'),
    ('canceled', 'canceled'),
  )
  state = models.CharField(max_length = 10, choices = STATE_CHOICES, default='current')
  def __unicode__(self):
    return "Order " + self.cust_name

  def jsonify(self):
    import json
    ret = {}
    ret['cust_name'] = self.cust_name
    ret['cust_phone'] = self.cust_phone
    ret['cust_email'] = self.cust_email
    ret['flow'] = self.flow.id
    return json.dumps(ret)

  def save(self, *args, **kwargs):
    if not self.pk: 
      #we allow current_stage not to be set, because we set it on save
      self.current_stage = self.flow.stages.get(stage_num=1)
    super(Order, self).save(*args, **kwargs)

class FeedEntry(models.Model):
  body = models.CharField(max_length=300)
  time_entered = models.DateTimeField(auto_now_add=True)
  order = models.ForeignKey(Order, related_name="feeds")
  def __unicode__(self):
    return self.body

admin.site.register(FeedEntry)
admin.site.register(Flow)
admin.site.register(Stage)
admin.site.register(BusinessProfile)

