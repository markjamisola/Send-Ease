from django.shortcuts import render
from twilio.rest import Client
from decouple import config

def welcome_page(request):
    return render(request, 'dashboard/welcome.html') 

def send_sms(request):
    if request.method == "POST":
        salutation = request.POST.get("salutation")  # Get salutation (greeting) from form
        recipient_name = request.POST.get("recipient_name")  # Get recipient name from form
        phone_number = request.POST.get("phone_number")  # Get phone number
        message_body = request.POST.get("message_body")  # Get message body

        # Construct the full message with salutation and name
        full_message = f"{salutation}, {recipient_name}. {message_body}"

        # Twilio credentials
        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token = config('TWILIO_AUTH_TOKEN')
        twilio_phone_number = config('TWILIO_PHONE_NUMBER')
        client = Client(account_sid, auth_token)

        try:
            # Send SMS using Twilio
            message = client.messages.create(
                body=full_message,
                from_=twilio_phone_number,
                to=phone_number
            )
            # Redirect to success page with context
            return render(request, 'dashboard/success.html', {
                'phone_number': phone_number,
                'message_sid': message.sid,
                'recipient_name': recipient_name,
                'salutation': salutation,
                'message_body': message_body,
            })
        except Exception as e:
            # Handle errors and display them on the SMS form page
            return render(request, 'dashboard/sms.html', {
                'error': str(e),
                'salutation': salutation,
                'recipient_name': recipient_name,
                'phone_number': phone_number,
                'message_body': message_body,
            })

    return render(request, 'dashboard/sms.html')
