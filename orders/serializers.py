from rest_framework import serializers

from users.models import User

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)
    initiator = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field='email'
    )
    class Meta:
        model = Order
        fields = "__all__"