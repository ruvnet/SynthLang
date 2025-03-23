"""
Compression benchmark scenario.

This module provides a benchmark scenario for measuring compression efficiency,
including token reduction, compression ratio, and cost savings.
"""
from typing import Dict, Any, List, Optional
import time
import random
import logging
import os
import json
from pathlib import Path

from app.benchmark.core.scenario import BenchmarkScenario, BenchmarkResult
from app.benchmark.core.metrics import CompressionMetrics, TokenReductionMetrics
from app.synthlang import compress_prompt, decompress_prompt
from app import llm_provider


logger = logging.getLogger(__name__)


# Sample texts for different types
SAMPLE_TEXTS = {
    "general": [
        "The quick brown fox jumps over the lazy dog. This sentence contains all the letters in the English alphabet and is often used for testing fonts and keyboards.",
        "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.",
        "Climate change is the long-term alteration of temperature and typical weather patterns in a place. Climate change could refer to a particular location or the planet as a whole. Climate change may cause weather patterns to be less predictable. These unexpected weather patterns can make it difficult to maintain and grow crops in regions that rely on farming."
    ],
    "technical": [
        "In computer science, a binary search tree (BST), also called an ordered or sorted binary tree, is a rooted binary tree data structure with the key of each internal node being greater than all the keys in the respective node's left subtree and less than the ones in its right subtree.",
        "The Transmission Control Protocol (TCP) is one of the main protocols of the Internet protocol suite. It originated in the initial network implementation in which it complemented the Internet Protocol (IP). Therefore, the entire suite is commonly referred to as TCP/IP.",
        "A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes. Thus a neural network is either a biological neural network, made up of real biological neurons, or an artificial neural network, for solving artificial intelligence (AI) problems."
    ],
    "creative": [
        "The old oak tree stood sentinel at the edge of the forest, its gnarled branches reaching toward the sky like ancient fingers. Beneath its sprawling canopy, generations had sought shelter from both sun and storm, whispering secrets to its weathered trunk.",
        "As the first light of dawn painted the eastern sky in hues of pink and gold, the small fishing village stirred to life. Nets were cast, boats launched, and the day's work began with the timeless rhythm that had defined this community for centuries.",
        "The abandoned mansion on the hill had been empty for decades, its windows like hollow eyes staring down at the town below. Local children dared each other to approach its rusted gates, but none had the courage to venture beyond the overgrown garden."
    ],
    "code": [
        """
def binary_search(arr, target):
    \"\"\"
    Perform binary search on a sorted array.
    
    Args:
        arr: Sorted array to search
        target: Value to find
        
    Returns:
        Index of target if found, -1 otherwise
    \"\"\"
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
        """,
        """
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        new_node = Node(value)
        
        if self.root is None:
            self.root = new_node
            return
        
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
        """,
        """
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# Load and prepare data
data = np.loadtxt('data.csv', delimiter=',')
X = data[:, :-1]
y = data[:, -1]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Plot results
plt.figure(figsize=(10, 6))
plt.imshow(conf_matrix, cmap='Blues')
plt.title(f'Confusion Matrix (Accuracy: {accuracy:.2f})')
plt.colorbar()
plt.show()
        """
    ]
}


# Token cost per 1K tokens for different models (in USD)
MODEL_TOKEN_COSTS = {
    "gpt-4o": 0.01,  # $10 per 1M tokens
    "gpt-4o-mini": 0.00015,  # $0.15 per 1M tokens
    "o3-mini": 0.00015,  # $0.15 per 1M tokens
    "claude-3-opus": 0.015,  # $15 per 1M tokens
    "claude-3-sonnet": 0.003,  # $3 per 1M tokens
    "claude-3-haiku": 0.00025,  # $0.25 per 1M tokens
}


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """
    Count the number of tokens in a text for a specific model.
    
    Args:
        text: Text to count tokens for
        model: Model to use for token counting
        
    Returns:
        Number of tokens
    """
    try:
        # Use the LLM provider's token counting if available
        return llm_provider.count_tokens(text, model)
    except (AttributeError, NotImplementedError):
        # Fallback to approximate token counting (roughly 4 chars per token)
        return len(text) // 4


def get_sample_text(text_type: str = "general", min_length: int = 100, max_length: int = 1000) -> str:
    """
    Get a sample text of the specified type and length.
    
    Args:
        text_type: Type of text to get (general, technical, creative, code)
        min_length: Minimum length of the text
        max_length: Maximum length of the text
        
    Returns:
        Sample text
    """
    if text_type not in SAMPLE_TEXTS:
        text_type = "general"
    
    # Get a random sample from the specified type
    samples = SAMPLE_TEXTS[text_type]
    text = random.choice(samples)
    
    # Ensure the text is within the specified length range
    if len(text) < min_length:
        # Repeat the text to reach minimum length
        text = text * (min_length // len(text) + 1)
    
    if len(text) > max_length:
        # Truncate to maximum length
        text = text[:max_length]
    
    return text


def load_real_world_samples(sample_count: int = 5) -> List[Dict[str, Any]]:
    """
    Load real-world samples from the samples directory.
    
    Args:
        sample_count: Number of samples to load
        
    Returns:
        List of sample dictionaries with text and metadata
    """
    samples_dir = Path(__file__).parent.parent / "data" / "samples"
    
    if not samples_dir.exists():
        logger.warning(f"Samples directory not found: {samples_dir}")
        return []
    
    samples = []
    sample_files = list(samples_dir.glob("*.json"))
    
    # If there are fewer files than requested, use all available
    sample_count = min(sample_count, len(sample_files))
    
    # Randomly select files
    selected_files = random.sample(sample_files, sample_count) if sample_files else []
    
    for file_path in selected_files:
        try:
            with open(file_path, 'r') as f:
                sample = json.load(f)
            samples.append(sample)
        except Exception as e:
            logger.error(f"Error loading sample file {file_path}: {e}")
    
    return samples


class CompressionBenchmark(BenchmarkScenario):
    """
    Benchmark for measuring compression efficiency.
    
    This benchmark measures the efficiency of different compression methods,
    including token reduction, compression ratio, and cost savings.
    """
    
    def __init__(self, name: str):
        """
        Initialize the compression benchmark.
        
        Args:
            name: Name of the benchmark
        """
        super().__init__(name)
        self.texts = []
        self.compression_method = "synthlang"
        self.model = "gpt-4o"
        self.use_gzip = False
    
    def setup(self, parameters: Dict[str, Any]) -> None:
        """
        Set up the benchmark with parameters.
        
        Args:
            parameters: Parameters for the benchmark
        """
        self.parameters = parameters
        
        # Get compression method
        self.compression_method = parameters.get("compression_method", "synthlang")
        
        # Get model for token counting
        self.model = parameters.get("model", "gpt-4o")
        
        # Get text type
        text_type = parameters.get("text_type", "general")
        
        # Get sample size
        sample_size = parameters.get("sample_size", 3)
        
        # Get use_gzip flag
        self.use_gzip = parameters.get("use_gzip", False)
        
        # Determine if we should use real-world samples
        use_real_samples = parameters.get("use_real_samples", False)
        
        # Load texts
        if use_real_samples:
            samples = load_real_world_samples(sample_size)
            self.texts = [sample.get("text", "") for sample in samples]
        else:
            # Generate synthetic texts
            self.texts = [
                get_sample_text(text_type, 
                               min_length=parameters.get("min_length", 200),
                               max_length=parameters.get("max_length", 2000))
                for _ in range(sample_size)
            ]
    
    def execute(self) -> BenchmarkResult:
        """
        Execute the benchmark and return results.
        
        Returns:
            BenchmarkResult containing metrics and metadata
        """
        # Create result object
        result = BenchmarkResult(
            scenario_name=self.name,
            start_time=time.time(),
            parameters=self.parameters
        )
        
        # Initialize metrics
        compression_metrics_list = []
        token_metrics_list = []
        total_original_size = 0
        total_compressed_size = 0
        total_original_tokens = 0
        total_compressed_tokens = 0
        total_compression_time = 0
        
        # Process each text
        for i, text in enumerate(self.texts):
            logger.info(f"Processing text {i+1}/{len(self.texts)}")
            
            # Measure original size and tokens
            original_size = len(text.encode('utf-8'))
            original_tokens = count_tokens(text, self.model)
            
            # Compress the text
            start_time = time.time()
            
            if self.compression_method == "synthlang":
                compressed_text = compress_prompt(text, use_gzip=False)
            elif self.compression_method == "synthlang+gzip":
                compressed_text = compress_prompt(text, use_gzip=True)
            elif self.compression_method == "gzip":
                import gzip
                import base64
                compressed_bytes = gzip.compress(text.encode('utf-8'))
                compressed_text = f"gz:{base64.b64encode(compressed_bytes).decode('utf-8')}"
            elif self.compression_method == "none":
                compressed_text = text
            else:
                compressed_text = text
                logger.warning(f"Unknown compression method: {self.compression_method}")
            
            compression_time = (time.time() - start_time) * 1000  # in milliseconds
            
            # Measure compressed size and tokens
            compressed_size = len(compressed_text.encode('utf-8'))
            compressed_tokens = count_tokens(compressed_text, self.model)
            
            # Calculate metrics
            compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
            token_reduction = (original_tokens - compressed_tokens) / original_tokens if original_tokens > 0 else 0.0
            
            # Calculate cost metrics
            token_cost_per_1k = MODEL_TOKEN_COSTS.get(self.model, 0.01)  # Default to gpt-4o cost
            token_cost_original = (original_tokens / 1000) * token_cost_per_1k
            token_cost_compressed = (compressed_tokens / 1000) * token_cost_per_1k
            cost_savings = (token_cost_original - token_cost_compressed) / token_cost_original if token_cost_original > 0 else 0.0
            
            # Create metrics objects
            compression_metrics = CompressionMetrics(
                original_size=original_size,
                compressed_size=compressed_size,
                compression_ratio=compression_ratio,
                original_tokens=original_tokens,
                compressed_tokens=compressed_tokens,
                token_reduction=token_reduction * 100,  # as percentage
                compression_time_ms=compression_time
            )
            
            token_metrics = TokenReductionMetrics(
                model=self.model,
                original_tokens=original_tokens,
                compressed_tokens=compressed_tokens,
                token_reduction=token_reduction * 100,  # as percentage
                token_cost_original=token_cost_original,
                token_cost_compressed=token_cost_compressed,
                cost_savings=cost_savings * 100  # as percentage
            )
            
            # Add to lists
            compression_metrics_list.append(compression_metrics)
            token_metrics_list.append(token_metrics)
            
            # Update totals
            total_original_size += original_size
            total_compressed_size += compressed_size
            total_original_tokens += original_tokens
            total_compressed_tokens += compressed_tokens
            total_compression_time += compression_time
            
            # Verify decompression works
            if self.compression_method == "synthlang" or self.compression_method == "synthlang+gzip":
                decompressed_text = decompress_prompt(compressed_text)
                if decompressed_text != text:
                    logger.warning("Decompression did not restore original text")
        
        # Calculate overall metrics
        overall_compression_ratio = total_compressed_size / total_original_size if total_original_size > 0 else 1.0
        overall_token_reduction = (total_original_tokens - total_compressed_tokens) / total_original_tokens if total_original_tokens > 0 else 0.0
        
        # Calculate overall cost metrics
        token_cost_per_1k = MODEL_TOKEN_COSTS.get(self.model, 0.01)  # Default to gpt-4o cost
        overall_token_cost_original = (total_original_tokens / 1000) * token_cost_per_1k
        overall_token_cost_compressed = (total_compressed_tokens / 1000) * token_cost_per_1k
        overall_cost_savings = (overall_token_cost_original - overall_token_cost_compressed) / overall_token_cost_original if overall_token_cost_original > 0 else 0.0
        
        # Prepare result metrics
        metrics = {
            "compression_ratio": overall_compression_ratio,
            "token_reduction_percentage": overall_token_reduction * 100,  # as percentage
            "cost_savings_percentage": overall_cost_savings * 100,  # as percentage
            "average_compression_time_ms": total_compression_time / len(self.texts) if self.texts else 0,
            "total_original_size_bytes": total_original_size,
            "total_compressed_size_bytes": total_compressed_size,
            "total_original_tokens": total_original_tokens,
            "total_compressed_tokens": total_compressed_tokens,
            "size_reduction_bytes": total_original_size - total_compressed_size,
            "token_reduction_count": total_original_tokens - total_compressed_tokens,
            "token_cost_original_usd": overall_token_cost_original,
            "token_cost_compressed_usd": overall_token_cost_compressed,
            "cost_savings_usd": overall_token_cost_original - overall_token_cost_compressed,
            "samples_count": len(self.texts)
        }
        
        # Complete the result
        result.complete(metrics)
        
        return result