import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum

from fastapi import FastAPI, Body, Path
from fastapi.openapi.utils import get_openapi
# NOTE: For Pydantic v1.x, we don't need the pydantic.json_schema import
from pydantic import BaseModel, Field, AnyHttpUrl

# ==============================================================================
# 1. MOCK DEPENDENCIES (from your seasalt_common_lib)
# ==============================================================================

class ConversationChannelType(str, Enum):
    SEAX_CALL = "seax_call"
    WHATSAPP = "whatsapp"
    VOICE = "voice"
    SMS = "sms"
    EMAIL = "email"

class SenderType(str, Enum):
    CUSTOMER = "customer"
    AGENT = "agent"
    BOT = "bot"
    SYSTEM = "system"

class ConversationMessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

def get_utc_now_without_timezone():
    return datetime.utcnow()

class BaseEventResource(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="The unique ID of the event resource.")
    event_time: datetime = Field(default_factory=get_utc_now_without_timezone, description="The UTC time the event was generated.")

# ==============================================================================
# 2. YOUR PROVIDED EVENT SCHEMAS (Simplified for clarity)
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
    """
    return SubscriptionResponse(subscription_id=f"sub_{uuid.uuid4()}")

# ==============================================================================
# 5. CUSTOM OPENAPI SCHEMA FOR PYDANTIC v1.x
# ==============================================================================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Ensure components and schemas keys exist
    openapi_schema.setdefault("components", {}).setdefault("schemas", {})

    # Manually build the schemas for the Union type for Pydantic v1
    event_models = EventResponse.__args__
    one_of_refs = []

    for model in event_models:
        # Use the standard .schema() method from Pydantic v1
        model_schema = model.schema(ref_template="#/components/schemas/{model}")
        
        # Pydantic v1 puts nested model schemas in a 'definitions' key.
        # We need to hoist them into the main components/schemas.
        if "definitions" in model_schema:
            for def_name, def_schema in model_schema["definitions"].items():
                openapi_schema["components"]["schemas"][def_name] = def_schema
            del model_schema["definitions"]

        # Add the main model schema to the components
        model_name = model.__name__
        openapi_schema["components"]["schemas"][model_name] = model_schema
        
        # Add a reference to this model for the 'oneOf' array
        one_of_refs.append({"$ref": f"#/components/schemas/{model_name}"})
    
    # Create the combined 'oneOf' schema for the Union
    openapi_schema["components"]["schemas"]["EventResponse"] = {"oneOf": one_of_refs}

    # Define and inject the callbacks object
    webhook_callback = {
        "eventWebhook": {
            '{$request.body#/webhook_url}': {
                'post': {
                    'summary': 'Webhook Event Notification',
                    'description': "This is the request your service will send to the client's webhook URL when a subscribed event occurs.",
                    'requestBody': {
                        'description': 'The event payload. The structure depends on the event type.',
                        'required': True,
                        'content': {'application/json': {'schema': {'$ref': '#/components/schemas/EventResponse'}}}
                    },
                    'responses': {'200': {'description': 'The client acknowledges receipt of the event successfully.'}}
                }
            }
        }
    }

    path = "/notify/api/v1/workspaces/{workspace_id}/subscription"
    if path in openapi_schema["paths"] and "post" in openapi_schema["paths"][path]:
        openapi_schema["paths"][path]["post"]["callbacks"] = webhook_callback

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
