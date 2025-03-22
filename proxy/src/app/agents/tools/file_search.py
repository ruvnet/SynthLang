"""
File search tool for the agent SDK.

This module provides a tool for performing semantic file searches
using vector embeddings for similarity matching.
"""
import logging
import os
import json
from typing import Dict, Any, List, Optional
import numpy as np
import faiss
from app.agents.registry import register_tool
from app import llm_provider

# Configure logging
logger = logging.getLogger(__name__)

# In-memory vector stores for file content
# Format: {store_id: {"index": faiss_index, "files": [{"path": path, "content": content, "id": id}]}}
VECTOR_STORES = {}


def create_vector_store(store_id: str, files: List[Dict[str, str]]) -> bool:
    """
    Create a new vector store with the given files.
    
    Args:
        store_id: The ID for the new vector store
        files: List of file dictionaries with 'path' and 'content' keys
        
    Returns:
        True if successful, False otherwise
    """
    global VECTOR_STORES
    
    if store_id in VECTOR_STORES:
        logger.warning(f"Vector store {store_id} already exists, overwriting")
    
    try:
        # Create a new FAISS index
        embed_dim = 1536  # OpenAI embedding dimension
        index = faiss.IndexFlatIP(embed_dim)
        
        # Process each file
        processed_files = []
        embeddings = []
        
        for i, file_info in enumerate(files):
            path = file_info.get("path", "")
            content = file_info.get("content", "")
            
            if not content:
                logger.warning(f"Skipping empty file: {path}")
                continue
            
            # Get embedding for file content
            try:
                embedding = llm_provider.get_embedding(content)
                embedding_array = np.array([embedding], dtype='float32')
                faiss.normalize_L2(embedding_array)
                embeddings.append(embedding_array)
                
                # Store file info with ID
                processed_files.append({
                    "id": i,
                    "path": path,
                    "content": content
                })
            except Exception as e:
                logger.error(f"Error embedding file {path}: {e}")
        
        # Add all embeddings to the index
        if embeddings:
            embeddings_matrix = np.vstack(embeddings)
            index.add(embeddings_matrix)
            
            # Store the index and files
            VECTOR_STORES[store_id] = {
                "index": index,
                "files": processed_files
            }
            logger.info(f"Created vector store {store_id} with {len(processed_files)} files")
            return True
        else:
            logger.warning(f"No valid files to index for store {store_id}")
            return False
    
    except Exception as e:
        logger.error(f"Error creating vector store {store_id}: {e}")
        return False


def perform_file_search(query: str, vector_store_id: str, max_results: int = 3) -> Dict[str, Any]:
    """
    Search for files in a vector store based on semantic similarity.
    
    Args:
        query: The search query
        vector_store_id: The ID of the vector store to search in
        max_results: Maximum number of results to return
        
    Returns:
        A dictionary containing the response message with search results
    """
    logger.info(f"File search requested: {query[:50]}...")
    
    # Check if vector store exists
    if vector_store_id not in VECTOR_STORES:
        logger.warning(f"Vector store {vector_store_id} not found")
        return {"content": f"Vector store '{vector_store_id}' not found. Please create it first."}
    
    try:
        # Get the vector store
        store = VECTOR_STORES[vector_store_id]
        index = store["index"]
        files = store["files"]
        
        # Get embedding for query
        query_embedding = llm_provider.get_embedding(query)
        query_embedding = np.array([query_embedding], dtype='float32')
        faiss.normalize_L2(query_embedding)
        
        # Search the index
        k = min(max_results, len(files))
        if k == 0:
            return {"content": "No files in the vector store to search."}
        
        distances, indices = index.search(query_embedding, k)
        
        # Format results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid index
                file_info = files[idx]
                similarity = float(distances[0][i])
                
                # Add result with similarity score and truncated content
                content = file_info["content"]
                if len(content) > 200:
                    content = content[:200] + "..."
                
                results.append({
                    "path": file_info["path"],
                    "similarity": similarity,
                    "content_preview": content
                })
        
        # Format response
        if results:
            response_content = f"Found {len(results)} relevant files for query: '{query}'\n\n"
            for i, result in enumerate(results):
                response_content += f"{i+1}. {result['path']} (similarity: {result['similarity']:.2f})\n"
                response_content += f"   Preview: {result['content_preview']}\n\n"
        else:
            response_content = f"No relevant files found for query: '{query}'"
        
        return {"content": response_content}
    
    except Exception as e:
        logger.error(f"Error searching vector store {vector_store_id}: {e}")
        return {"content": f"Error searching files: {str(e)}"}


# Register the file search tool in the registry
register_tool("file_search", perform_file_search)