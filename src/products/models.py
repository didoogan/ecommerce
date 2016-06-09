from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()	

	def get_related(self, instance):
		products_one = self.get_queryset().filter(categories__in=instance.categories.all())	
		products_two = self.get_queryset().filter(default=instance.default)	
		qs = (products_one | products_two).exclude(id=instance.id).distinct()
		#qs = self.get_queryset()
		return qs


class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	active = models.BooleanField(default=True)
	categories = models.ManyToManyField('Category', blank=True)
	default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)


	objects = ProductManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("product_detail", kwargs={"pk": self.pk})

	def get_image_url(self):
		img = self.productimage_set.first()
		if img:
			return img.image.url
		return img #None			

class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.title

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_html_price(self):
		if self.sale_price is not None:
			html_text = "<span class='sale-price'>%s</span> <span class='orig_price'>%s</span>"%(self.sale_price, self.price)
		else:
			html_text = "<span class='orig_price'>%s</span>"%(self.price)
		return mark_safe(html_text)	


	def get_absolute_url(self):
		return self.product.get_absolute_url()	

def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	product = instance
	variations = product.variation_set.all()
	if variations.count() ==0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var.price = product.price
		new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)

def image_upload_to(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	basename, file_extansion = filename.split(".")
	new_filename = "%s-%s.%s" % (basename, instance.id, file_extansion)
	return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to=image_upload_to, default='products/')		

	def __str__(self):
		return self.product.title					


class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug":self.slug})		



def image_upload_to_feateured(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	basename, file_extansion = filename.split(".")
	new_filename = "%s-%s.%s" % (basename, instance.id, file_extansion)
	return "products/%s/featured/%s" %(slug, new_filename)

class ProductFeatued(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to=image_upload_to_feateured)
	title = models.CharField(max_length=120, null=True, blank=True)
	text = models.CharField(max_length=200, null=True, blank=True)
	make_backround_image = models.BooleanField(default=False)
	text_css_color = models.CharField(max_length=6, null=True, blank=True)
	text_right = models.BooleanField(default=False)
	show_price = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.product.title	


