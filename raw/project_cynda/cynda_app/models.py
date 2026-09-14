from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='quotes',
        db_column='category_id',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='quotes',
        db_table='quote_tags',
    )

    class Meta:
        db_table = 'quotes'

    def __str__(self):
        return self.text[:50]