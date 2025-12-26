from rest_framework import serializers
from .models import Author, Book, Order

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total_price']

    def validate_quantity(self, value):
        book = self.initial_data.get('book')
        book_obj = Book.objects.get(id=book)
        if value > book_obj.stock:
            raise serializers.ValidationError("Quantity exceeds available stock")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
