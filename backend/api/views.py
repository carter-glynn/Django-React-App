from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, ItemSerializer, NotificationPreferenceSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Item, UserPhoneNumber, NotificationPreference
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import export_to_pdf
import logging
from .utils import schedule_notifications, send_sms

# Set up logging for debugging
logger = logging.getLogger(__name__)

class NotificationPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Set notification preferences for an item."""
        # Extract data from the request
        item_id = request.data.get("item")
        notify_when = request.data.get("notify_when")

        # Ensure that both fields are provided
        if not item_id or not notify_when:
            return Response({"error": "Item and notification time are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the item belongs to the logged-in user
            item = Item.objects.get(id=item_id, owner=request.user)

            # Create or update the notification preference
            notification_preference, created = NotificationPreference.objects.get_or_create(
                item=item,
                user=request.user,
                defaults={"notify_when": notify_when}
            )

            if not created:
                # If the preference already exists, update it
                notification_preference.notify_when = notify_when
                notification_preference.save()

            # Log the successful action
            logger.info(f"Notification preference {'created' if created else 'updated'} for item {item_id} by {request.user.username}")
            
            # Return success response
            schedule_notifications()  # Trigger notifications after saving preferences
            return Response({"message": "Notification preference saved successfully."}, status=status.HTTP_200_OK)

        except Item.DoesNotExist:
            # Handle the case where the item is not found or the user is unauthorized
            logger.warning(f"Unauthorized access or item not found for user {request.user.username}")
            return Response({"error": "Item not found or unauthorized access."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle any other unexpected errors
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An error occurred while saving the notification preference."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenerateReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Check if 'type' is provided in the request body
        report_type = request.data.get("type")
        if not report_type:
            logger.error("No report type provided")
            return Response({"error": "Report type is required."}, status=400)

        try:
            # Fetch items based on the logged-in user
            user = request.user
            items = Item.objects.filter(owner=user)

            if not items.exists():
                logger.warning(f"No items found for user {user.username}")
                content = "No items found for this user."
            else:
                # Create content for the PDF
                content = "Report Generated for User\n\n"
                content += f"Report Type: {report_type}\n\n"
                content += "ID | Name | Category | Price | Owner\n"
                content += "-" * 60 + "\n"

                # Add item details to the content
                for item in items:
                    content += f"{item.id} | {item.name} | {item.category} | {item.price} | {item.owner.username}\n"
            
            # Generate PDF using export_to_pdf utility function
            filename = "report.pdf"
            export_to_pdf(content, filename)

            # Set up the response to send the PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            with open(filename, "rb") as pdf_file:
                response.write(pdf_file.read())

            logger.info("PDF Report generated successfully")
            return response

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return Response({"error": "Internal Server Error"}, status=500)

class ItemListCreate(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Item.objects.filter(owner=user)  # Default: filter by user

        # Apply filters based on query parameters
        category = self.request.query_params.get('category', None)
        value = self.request.query_params.get('value', None)
        purchase_date = self.request.query_params.get('purchase_date', None)

        if category:
            queryset = queryset.filter(category__icontains=category)
        if value:
            try:
                value = float(value)
                queryset = queryset.filter(price__gte=value)  # Filter by value greater than or equal
            except ValueError:
                logger.warning(f"Invalid value for price filter: {value}")
        if purchase_date:
            try:
                queryset = queryset.filter(purchase_date=purchase_date)  # Exact match for purchase date
            except ValueError:
                logger.warning(f"Invalid date format for purchase_date filter: {purchase_date}")

        return queryset
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)

class ItemDelete(generics.DestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Item.objects.filter(owner=user)

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
        })

@login_required
def get_user(request):
    return JsonResponse({
        "id": request.user.id,
        "username": request.user.username,
    })