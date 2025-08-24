from app.core.logging_config import get_logger
from app.config import settings


logger = get_logger(__name__)

# topic_handler_map = {
#     settings.api.DIGIO_PAYMENTS_KAFKA_TOPIC: "DigioWebhookHandler",
#     settings.api.RAZORPAY_PAYMENTS_KAFKA_TOPIC: "RazorpayWebhookHandler",
#     settings.api.ORDER_BACKUP_KAFKA_TOPIC: "OrderBackupHandler"
# }
#
# topic_exchange_map = {
#     settings.api.DIGIO_PAYMENTS_KAFKA_TOPIC: settings.api.LMS_KAFKA_TOPIC,
#     settings.api.RAZORPAY_PAYMENTS_KAFKA_TOPIC: settings.api.LMS_KAFKA_TOPIC
# }
topic_handler_map = topic_exchange_map = {}
async def dispatch_event(topic_name: str, payload: dict, kafka_manager=None):
    logger.info(f"Dispatching event for topic: {topic_name} with payload: {payload}")
    handler_class = topic_handler_map.get(topic_name)
    if handler_class:
        handler = handler_class()
        if hasattr(handler, 'handle_webhook_event'):
            # Call the method to handle the webhook event
            status, message = await handler.handle_webhook_event(payload)
            logger.info(f"Event handled successfully: {message}")
            if status and message:    
                await kafka_manager.send_message(
                    topic=topic_exchange_map.get(topic_name),
                    key=message.get("unique_id"),
                    value=message
                )
        else:
            raise ValueError(f"No method handler found for topic: {topic_name}")
    else:
        raise ValueError(f"No handler found for topic: {topic_name}")

