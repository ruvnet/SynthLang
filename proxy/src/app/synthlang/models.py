"""
SynthLang API models.

This module defines the Pydantic models for SynthLang API endpoints.
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    """Request model for translation endpoint."""
    text: str = Field(..., description="Text to translate to SynthLang format")
    instructions: Optional[str] = Field(None, description="Optional custom translation instructions")


class TranslateResponse(BaseModel):
    """Response model for translation endpoint."""
    source: str = Field(..., description="Original text")
    target: str = Field(..., description="Translated text in SynthLang format")
    explanation: str = Field(..., description="Explanation of the translation")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class GenerateRequest(BaseModel):
    """Request model for generation endpoint."""
    task_description: str = Field(..., description="Description of the task")


class GenerateResponse(BaseModel):
    """Response model for generation endpoint."""
    prompt: str = Field(..., description="Generated system prompt")
    rationale: str = Field(..., description="Design rationale")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class OptimizeRequest(BaseModel):
    """Request model for optimization endpoint."""
    prompt: str = Field(..., description="Prompt to optimize")
    max_iterations: Optional[int] = Field(5, description="Maximum optimization iterations")


class OptimizeResponse(BaseModel):
    """Response model for optimization endpoint."""
    optimized: str = Field(..., description="Optimized prompt")
    improvements: List[str] = Field(..., description="List of improvements made")
    metrics: Dict[str, float] = Field(..., description="Performance metrics")
    original: str = Field(..., description="Original prompt")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class EvolveRequest(BaseModel):
    """Request model for evolution endpoint."""
    seed_prompt: str = Field(..., description="Initial prompt to evolve from")
    n_generations: Optional[int] = Field(10, description="Number of generations to evolve")


class EvolveResponse(BaseModel):
    """Response model for evolution endpoint."""
    best_prompt: str = Field(..., description="Best evolved prompt")
    fitness: Dict[str, Any] = Field(..., description="Fitness scores")
    generations: int = Field(..., description="Number of generations completed")
    total_variants: int = Field(..., description="Total variants created")
    successful_mutations: int = Field(..., description="Count of successful mutations")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class ClassifyRequest(BaseModel):
    """Request model for classification endpoint."""
    text: str = Field(..., description="Text to classify")
    labels: List[str] = Field(..., description="List of possible classification labels")


class ClassifyResponse(BaseModel):
    """Response model for classification endpoint."""
    input: str = Field(..., description="Input text")
    label: str = Field(..., description="Classification label")
    explanation: str = Field(..., description="Explanation for the classification")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class SavePromptRequest(BaseModel):
    """Request model for save prompt endpoint."""
    name: str = Field(..., description="Name to save prompt under")
    prompt: str = Field(..., description="The prompt content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata about the prompt")


class SavePromptResponse(BaseModel):
    """Response model for save prompt endpoint."""
    success: bool = Field(..., description="Whether the prompt was saved successfully")
    name: str = Field(..., description="Name of the saved prompt")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class LoadPromptRequest(BaseModel):
    """Request model for load prompt endpoint."""
    name: str = Field(..., description="Name of prompt to load")


class LoadPromptResponse(BaseModel):
    """Response model for load prompt endpoint."""
    name: str = Field(..., description="Name of the prompt")
    prompt: str = Field(..., description="The prompt content")
    metadata: Dict[str, Any] = Field(..., description="Metadata about the prompt")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class ListPromptsResponse(BaseModel):
    """Response model for list prompts endpoint."""
    prompts: List[Dict[str, Any]] = Field(..., description="List of prompt data dictionaries")
    count: int = Field(..., description="Number of prompts")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class DeletePromptRequest(BaseModel):
    """Request model for delete prompt endpoint."""
    name: str = Field(..., description="Name of prompt to delete")


class DeletePromptResponse(BaseModel):
    """Response model for delete prompt endpoint."""
    success: bool = Field(..., description="Whether the prompt was deleted successfully")
    name: str = Field(..., description="Name of the deleted prompt")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class ComparePromptsRequest(BaseModel):
    """Request model for compare prompts endpoint."""
    name1: str = Field(..., description="First prompt name")
    name2: str = Field(..., description="Second prompt name")


class ComparePromptsResponse(BaseModel):
    """Response model for compare prompts endpoint."""
    prompts: Dict[str, str] = Field(..., description="Prompts being compared")
    metrics: Dict[str, Dict[str, Any]] = Field(..., description="Metrics for each prompt")
    differences: Dict[str, Any] = Field(..., description="Differences between prompts")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")


class SynthLangError(BaseModel):
    """Error model for SynthLang API endpoints."""
    error: Dict[str, Any] = Field(..., description="Error details")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the error")