import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum

from fastapi import FastAPI, Body, Path
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, AnyHttpUrl, TypeAdapter

# ==============================================================================
# 1. MOCK DEPENDENCIES (from your seasalt_common_lib)
# This section creates mock enums and base classes to make the code runnable.
# ==============================================================================

class ConversationChannelType(str, Enum):
    SEAX_CALL = "seax_call"
    WHATSAPP = "whatsapp"
    VOICE = "voice"
    SMS = "sms"
    EMAIL = "email"

class SeaNotifyCallFinishReason(str, Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class SenderType(str, Enum):
    CUSTOMER = "customer"
    AGENT = "agent"
    BOT = "bot"
    SYSTEM = "system"

class ConversationStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CLOSED = "closed"

class MessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class MessageType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"

class ConversationMessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class LabelType(str, Enum):
    CONTACT = "contact"
    CONVERSATION = "conversation"

def get_utc_now_without_timezone():
    return datetime.utcnow()

class BaseEventResource(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="The unique ID of the event resource.")
    event_time: datetime = Field(default_factory=get_utc_now_without_timezone, description="The UTC time the event was generated.")

class BaseLabel(BaseModel):
    name: str = Field(..., example="High Priority")
    color: str = Field(..., example="#FF0000")
    description: Optional[str] = Field(None, example="For critical customer issues.")

class Label(BaseLabel):
    id: str = Field(..., example="label-123")
    type: LabelType = Field(..., example=LabelType.CONVERSATION)

# ==============================================================================
# 2. YOUR PROVIDED EVENT SCHEMAS
# All the event schemas that could be sent to the webhook.
# ==============================================================================

class SeaNotifyWorkspaceSchema(BaseModel):
    id: str
    name: str

class SeaNotifySourceSchema(BaseModel):
    id: str
    type: ConversationChannelType
    identifier: str

class SeaNotifyCustomerSchema(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    channel: ConversationChannelType
    address: Optional[str]

class DataBase(BaseModel):
    conversation_id: str
    conversation_title: str

class SeaNotifyConversationNewEventDataSchemaBase(DataBase):
    channel: ConversationChannelType
    customer: SeaNotifyCustomerSchema

class EventSchemaBase(BaseEventResource):
    id: str
    version: str
    workspace: SeaNotifyWorkspaceSchema
    source: SeaNotifySourceSchema

class SeaNotifyConversationNewEvent(EventSchemaBase):
    """Event schema for a new conversation."""
    data: SeaNotifyConversationNewEventDataSchemaBase

class SeaNotifyMessageNewEventSenderSchema(BaseModel):
    type: SenderType
    id: str
    name: Optional[str]

class SeaNotifyMessageNewEventContentSchema(BaseModel):
    type: str
    text: str
    data: Optional[Dict[str, Any]]

class SeaNotifyMessageNewEventDataSchema(DataBase):
    message_id: str
    direction: ConversationMessageDirection
    created_at: datetime
    sender: SeaNotifyMessageNewEventSenderSchema
    content: SeaNotifyMessageNewEventContentSchema

class SeaNotifyMessageNewEvent(EventSchemaBase):
    """Event schema for a new message."""
    data: SeaNotifyMessageNewEventDataSchema

# ==============================================================================
# 3. DEFINE A UNION OF ALL POSSIBLE WEBHOOK PAYLOADS
# ==============================================================================
EventResponse = Union[
    SeaNotifyConversationNewEvent,
    SeaNotifyMessageNewEvent,
]

# ==============================================================================
# 4. FASTAPI APP AND ENDPOINT DEFINITION
# ==============================================================================

# -- Request and Response Models for the Subscription Endpoint --
class SubscriptionRequest(BaseModel):
    webhook_url: AnyHttpUrl = Field(..., description="The URL to which event notifications will be sent.", example="https://api.example.com/my-webhook-handler")
    event_types: List[str] = Field(..., description="A list of event types to subscribe to.", example=["conversation.new", "message.new"])
    created_by: str = Field(..., description="Identifier for the user or system creating the subscription.", example="user_12345")
    is_enabled: bool = Field(True, description="Set to false to pause sending events.")
    type: str = Field("SEASALT", description="Type of the subscription.", example="SEASALT")

class SubscriptionResponse(BaseModel):
    subscription_id: str = Field(..., description="The unique ID for the created subscription.")
    status: str = Field("active", description="The status of the subscription.")
    message: str = Field("Webhook subscription registered successfully.", description="A confirmation message.")


# -- Main FastAPI Application --
app = FastAPI(
    title="SeaNotify Webhook API",
    description="This API allows clients to subscribe to real-time event notifications via webhooks.",
    version="1.0.0",
)


@app.post(
    "/notify/api/v1/workspaces/{workspace_id}/subscription",
    response_model=SubscriptionResponse,
    summary="Create a Webhook Subscription",
    tags=["Subscriptions"],
)
async def create_subscription(
    workspace_id: str = Path(..., description="The ID of the workspace.", example="ws-a9b8c7d6"),
    subscription_request: SubscriptionRequest = Body(...)
):
    """
    Register a new webhook URL to receive notifications for specific event types.

    When a subscribed event (e.g., `conversation.new`) occurs, our system will
    send a `POST` request to the provided `webhook_url`.

    **Callbacks:** Check the "Callbacks" section in the documentation below to see the structure of the
    request that will be sent to your webhook.
    """
    # In a real application, you would save the subscription details to a database.
    print(f"Creating subscription for workspace: {workspace_id}")
    return SubscriptionResponse(subscription_id=f"sub_{uuid.uuid4()}")

# ==============================================================================
# 5. CUSTOM OPENAPI SCHEMA GENERATION (THE FIX)
# ==============================================================================
def custom_openapi():
    # If the schema is already cached, return it
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the default OpenAPI schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Manually define the callback object
    webhook_callback = {
        "eventWebhook": {
            '{$request.body#/webhook_url}': {
                'post': {
                    'summary': 'Webhook Event Notification',
                    'description': "This is the request your service will send to the client's webhook URL when a subscribed event occurs.",
                    'requestBody': {
                        'description': 'The event payload. The structure depends on the event type.',
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    # This uses a reference to the Union model defined below
                                    '$ref': '#/components/schemas/EventResponse'
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {'description': 'The client acknowledges receipt of the event successfully.'},
                        '4xx': {'description': 'The client reports a client-side error in processing the event.'},
                        '5xx': {'description': 'The client server encountered an error.'}
                    }
                }
            }
        }
    }

    # Find the subscription path and inject the callback
    path = "/notify/api/v1/workspaces/{workspace_id}/subscription"
    if path in openapi_schema["paths"] and "post" in openapi_schema["paths"][path]:
        openapi_schema["paths"][path]["post"]["callbacks"] = webhook_callback

    # Ensure our Union model `EventResponse` is in the components schema
    # Pydantic v2's `model_json_schema` helps create the 'oneOf' structure
    if "EventResponse" not in openapi_schema.get("components", {}).get("schemas", {}):
        openapi_schema.setdefault("components", {}).setdefault("schemas", {})
        # The original line `EventResponse.model_json_schema(...)` is incorrect because
        # `model_json_schema` is a method on Pydantic models, not Union types.
        # The correct way to generate a schema for a Union is with a TypeAdapter.
        adapter = TypeAdapter(EventResponse)
        event_response_schema = adapter.json_schema(ref_template="#/components/schemas/{model}")

        # Move the generated sub-model schemas from '$defs' to the main components section
        openapi_schema["components"]["schemas"].update(event_response_schema.pop("$defs", {}))
        openapi_schema["components"]["schemas"]["EventResponse"] = event_response_schema

    # Cache the schema and return it
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign the custom function to the app. This overrides the default schema generation.
app.openapi = custom_openapi
