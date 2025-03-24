"""
Pydantic models for request and response validation.

This module contains the Pydantic models used for validating
API requests and responses.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional, Dict, Any, Union


class Message(BaseModel):
    """
    A chat message in a conversation.
    
    Attributes:
        role: The role of the message sender (system, user, or assistant)
        content: The content of the message
    """
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """
    Request model for chat completions API.
    
    Attributes:
        model: The model to use for generating completions
        messages: The conversation messages
        stream: Whether to stream the response
        temperature: Controls randomness (higher = more random)
        top_p: Controls diversity via nucleus sampling
        n: How many completions to generate
        max_tokens: Maximum number of tokens to generate
        presence_penalty: Penalizes repeated tokens
        frequency_penalty: Penalizes frequent tokens
        logit_bias: Modifies likelihood of specific tokens
        user: A unique identifier for the end-user
    """
    model: str = Field(..., description="Model name (e.g., gpt-3.5-turbo)")
    messages: List[Message] = Field(..., description="Conversation messages")
    stream: Optional[bool] = Field(False, description="Whether to stream the response")
    temperature: Optional[float] = Field(None, description="Controls randomness (higher = more random)")
    top_p: Optional[float] = Field(None, description="Controls diversity via nucleus sampling")
    n: Optional[int] = Field(None, description="How many completions to generate")
    max_tokens: Optional[int] = Field(None, description="Maximum number of tokens to generate")
    presence_penalty: Optional[float] = Field(None, description="Penalizes repeated tokens")
    frequency_penalty: Optional[float] = Field(None, description="Penalizes frequent tokens")
    logit_bias: Optional[Dict[str, float]] = Field(None, description="Modifies likelihood of specific tokens")
    user: Optional[str] = Field(None, description="A unique identifier for the end-user")
    
    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v):
        if v is not None and (v < 0 or v > 2):
            raise ValueError('Temperature must be between 0 and 2')
        return v
    
    @field_validator('top_p')
    @classmethod
    def validate_top_p(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Top_p must be between 0 and 1')
        return v
    
    @field_validator('presence_penalty', 'frequency_penalty')
    @classmethod
    def validate_penalties(cls, v):
        if v is not None and (v < -2 or v > 2):
            raise ValueError('Penalty values must be between -2 and 2')
        return v


class ChatResponseChoice(BaseModel):
    """
    A single completion choice in a chat response.
    
    Attributes:
        index: The index of this completion choice
        message: The message containing the completion
        finish_reason: The reason why the completion finished
    """
    index: int
    message: Message
    finish_reason: Optional[str] = None


class ChatResponseUsage(BaseModel):
    """
    Token usage information for a chat response.
    
    Attributes:
        prompt_tokens: Number of tokens in the prompt
        completion_tokens: Number of tokens in the completion
        total_tokens: Total number of tokens used
    """
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class DebugInfo(BaseModel):
    """
    Debug information for a chat response.
    
    Attributes:
        compressed_messages: The compressed messages
        decompressed_messages: The decompressed messages
    """
    compressed_messages: Optional[List[Dict[str, str]]] = None
    decompressed_messages: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    """
    Response model for chat completions API.
    
    Attributes:
        id: A unique identifier for the completion
        object: The object type (always "chat.completion")
        created: The Unix timestamp of when the completion was created
        model: The model used for the completion
        choices: The completion choices
        usage: Token usage information
        debug: Debug information (optional)
    """
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatResponseChoice]
    usage: Optional[ChatResponseUsage] = None
    debug: Optional[DebugInfo] = None


class ErrorResponse(BaseModel):
    """
    Error response model.
    
    Attributes:
        error: The error details
    """
    error: Dict[str, Any]


class StreamResponseChoice(BaseModel):
    """
    A streaming response choice.
    
    Attributes:
        index: The index of this completion choice
        delta: The delta content for this chunk
        finish_reason: The reason why the completion finished
    """
    index: int
    delta: Dict[str, str]
    finish_reason: Optional[str] = None


class StreamResponse(BaseModel):
    """
    A streaming response chunk.
    
    Attributes:
        id: A unique identifier for the completion
        object: The object type (always "chat.completion.chunk")
        created: The Unix timestamp of when the chunk was created
        model: The model used for the completion
        choices: The completion choices for this chunk
    """
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[StreamResponseChoice]


class APIInfo(BaseModel):
    """
    Basic API information.
    
    Attributes:
        name: The name of the API
        version: The version of the API
        status: The status of the API
        documentation: The URL to the API documentation
    """
    name: str
    version: str
    status: str
    documentation: Optional[str] = None


class HealthCheck(BaseModel):
    """
    Health check response.
    
    Attributes:
        status: The status of the API (healthy or unhealthy)
        timestamp: The Unix timestamp of when the health check was performed
        synthlang_available: Whether SynthLang is available
        version: The version of the API
    """
    status: str
    timestamp: int
    synthlang_available: bool
    version: str