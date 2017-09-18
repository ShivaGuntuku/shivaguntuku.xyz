
from django.conf import settings 
from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.utils.text import slugify

from PIL import Image
# Create your models here.

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager,self).filter(draft = False).filter(publish__lte = timezone.now())

def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)

class Posts(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
	title = models.CharField(max_length = 120)
	slug = models.SlugField(unique = True, max_length = 50)
	image = models.ImageField(upload_to = upload_location, 
			null=True, blank=True,
			width_field = "width_field",
			height_field = "height_field")
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)
	content = models.TextField()
	draft = models.BooleanField(default = False)
	publish = models.DateField(auto_now = False, auto_now_add = False,)
	updated = models.DateTimeField(auto_now = True, auto_now_add = False)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

	objects = PostManager()

	def __str__(self):
		return  self.title

	def get_absolute_url(self):
		return reverse('posts:detail',kwargs = {'slug' : self.slug})

	class Meta:
		ordering = ["-timestamp","-updated"]

	# def save(self):
	# 	if not self.image:
	# 		return

	# 	super(Posts, self).save()
	# 	image = Image.open(self.image)
	# 	(width, height) = image.size
	# 	size = ( 100, 100)
	# 	image = image.resize(size, Image.ANTIALIAS)
	# 	image.save(BytesIO(),format="JPEG")

def create_slug(instance, new_slug = None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Posts.objects.filter(slug = slug).order_by("-id")
	exists = qs.exists()
	if exists :
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug = new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver,sender = Posts)