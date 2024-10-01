from django.db import transaction
from rest_framework import serializers

from clients.models import Customer
from employees.models import Employee
from products.models import Product
from .models import Sale, SaleItem

class SaleItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = SaleItem
        exclude = ["sale"]

class SaleSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    items = SaleItemSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ("__all__")

    @transaction.atomic
    def create(self, validated_data: dict) -> Sale:
        items: dict = validated_data.pop("items")

        sale: Sale = Sale.objects.create(**validated_data)
        for item in items:
            SaleItem.objects.create(sale=sale, **item)
        
        return sale
    
    @transaction.atomic
    def update(self, instance: Sale, validated_data: dict) -> Sale:
        items: dict = validated_data.pop("items", None)
        
        instance.date = validated_data.get("date", instance.date)
        instance.hour = validated_data.get("hour", instance.date)
        instance.status = validated_data.get("status", instance.status)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.total_amount = validated_data.get("total_amount", instance.total_amount)
        instance.payment = validated_data.get("payment", instance.payment)
        instance.customer = validated_data.get("customer", instance.customer)
        instance.employee = validated_data.get("employee", instance.employee)
        instance.save()

        if items:
            SaleItem.objects.filter(sale=instance).delete()

            for item in items:
                SaleItem.objects.create(sale=instance, **item)

        return instance
