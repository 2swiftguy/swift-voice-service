from twilio.twiml.messaging_response import MessagingResponse


def build_sms_response(message: str) -> str:
    response = MessagingResponse()
    response.message(message)
    return str(response)

