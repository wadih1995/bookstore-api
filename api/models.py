from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    published_date = models.DateField()

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.quantity > self.book.stock:
            raise ValueError("Not enough stock")

        self.total_price = self.quantity * self.book.price
        self.book.stock -= self.quantity
        self.book.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id}"

