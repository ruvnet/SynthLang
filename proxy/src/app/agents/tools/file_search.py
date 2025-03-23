"""
File search tool for the agent SDK.

This module provides a tool for performing semantic file searches
using vector embeddings for similarity matching.
"""
import logging
import os
import json
import sys
import traceback
from typing import Dict, Any, List, Optional
import numpy as np
import faiss

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path in file_search.py")

# Print current Python path for debugging
print(f"Python path in file_search.py: {sys.path}")

# Try to import from src.app first
try:
    print("Attempting to import registry from src.app.agents.registry")
    from src.app.agents.registry import register_tool
    print("Successfully imported registry from src.app.agents.registry")
    from src.app import llm_provider
    print("Successfully imported llm_provider from src.app")
except ImportError as e:
    print(f"Error importing from src.app: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    # Try to import from app
    try:
        print("Attempting to import registry from app.agents.registry")
        from app.agents.registry import register_tool
        print("Successfully imported registry from app.agents.registry")
        from app import llm_provider
        print("Successfully imported llm_provider from app")
    except ImportError as e2:
        print(f"Error importing from app: {e2}")
        print(f"Traceback: {traceback.format_exc()}")
        # Define a dummy register_tool function to avoid errors
        def register_tool(name, func):
            print(f"Dummy register_tool called for {name}")
        print("Using dummy register_tool function")
        # Define a dummy llm_provider module
        class DummyLLMProvider:
            async def get_embeddings(self, texts):
                print("Dummy get_embeddings called")
                return [np.zeros(1536) for _ in texts]
        llm_provider = DummyLLMProvider()
        print("Using dummy llm_provider")

# Configure logging
logger = logging.getLogger(__name__)

# In-memory vector stores for file content
# Format: {store_id: {"index": faiss_index, "files": [{"path": path, "content": content, "id": id}]}}
VECTOR_STORES = {}

async def search_files(query: str, directory: Optional[str] = None, user_message: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for files semantically similar to the query.
    
    Args:
        query: The search query
        directory: The directory to search in (optional)
        user_message: The original user message (optional)
        user_id: The ID of the user making the request (optional)
        
    Returns:
        A dictionary containing the search results
    """
    logger.info(f"Searching files for query: {query}")
    print(f"Searching files for query: {query}")
    
    try:
        # Use the user ID as the store ID if available, otherwise use a default
        store_id = user_id or "default"
        
        # Check if we have a vector store for this user/directory
        if store_id not in VECTOR_STORES:
            # Create a new vector store
            await create_vector_store(store_id, directory)
        
        # Get the vector store
        vector_store = VECTOR_STORES.get(store_id)
        if not vector_store:
            raise ValueError(f"Vector store not found for store ID: {store_id}")
        
        # Get embeddings for the query
        query_embedding = await llm_provider.get_embeddings([query])
        if not query_embedding or len(query_embedding) == 0:
            raise ValueError("Failed to get embeddings for query")
        
        # Convert to numpy array
        query_embedding_np = np.array(query_embedding[0]).reshape(1, -1).astype('float32')
        
        # Search the index
        k = min(5, len(vector_store["files"]))  # Number of results to return
        if k == 0:
            raise ValueError("No files in the vector store")
        
        distances, indices = vector_store["index"].search(query_embedding_np, k)
        
        # Get the results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(vector_store["files"]):
                continue
            
            file_info = vector_store["files"][idx]
            results.append({
                "path": file_info["path"],
                "score": float(1.0 - distances[0][i]),  # Convert distance to similarity score
                "excerpt": file_info["content"][:200] + "..." if len(file_info["content"]) > 200 else file_info["content"]
            })
        
        # Create the response
        if results:
            response_text = f"""File Search Results for "{query}":

{json.dumps(results, indent=2)}

This search was performed using the file search tool."""
        else:
            response_text = f"""No files found matching "{query}".

Please try a different query or check that the directory contains files."""
        
        return {
            "content": response_text,
            "tool": "file_search",
            "query": query,
            "directory": directory,
            "results": results
        }
    
    except Exception as e:
        error_message = f"""I couldn't search for files matching "{query}".

Error: {str(e)}

Please try again with a different query or directory."""
        
        logger.error(f"File search error: {str(e)}")
        print(f"File search error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        return {
            "content": error_message,
            "tool": "file_search",
            "query": query,
            "directory": directory,
            "error": str(e)
        }

async def create_vector_store(store_id: str, directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a vector store for a directory.
    
    Args:
        store_id: The ID of the store
        directory: The directory to index (optional)
        
    Returns:
        The created vector store
    """
    logger.info(f"Creating vector store for store ID: {store_id}")
    print(f"Creating vector store for store ID: {store_id}")
    
    try:
        # Use the current directory if none is specified
        directory = directory or os.getcwd()
        
        # Get all text files in the directory
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(('.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv')):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        files.append({
                            "path": file_path,
                            "content": content,
                            "id": len(files)
                        })
                    except Exception as e:
                        logger.error(f"Error reading file {file_path}: {e}")
                        print(f"Error reading file {file_path}: {e}")
        
        # Get embeddings for all files
        if files:
            contents = [file["content"] for file in files]
            embeddings = await llm_provider.get_embeddings(contents)
            
            # Create a FAISS index
            dimension = len(embeddings[0])
            index = faiss.IndexFlatL2(dimension)
            
            # Add embeddings to the index
            embeddings_np = np.array(embeddings).astype('float32')
            index.add(embeddings_np)
            
            # Create the vector store
            VECTOR_STORES[store_id] = {
                "index": index,
                "files": files
            }
            
            logger.info(f"Created vector store with {len(files)} files")
            print(f"Created vector store with {len(files)} files")
            
            return VECTOR_STORES[store_id]
        else:
            logger.warning(f"No files found in directory: {directory}")
            print(f"No files found in directory: {directory}")
            
            # Create an empty vector store
            VECTOR_STORES[store_id] = {
                "index": faiss.IndexFlatL2(1536),  # Default OpenAI embedding dimension
                "files": []
            }
            
            return VECTOR_STORES[store_id]
    
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        print(f"Error creating vector store: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise

# Register the tool
try:
    print("Registering file_search tool")
    register_tool("file_search", search_files)
    print("File search tool registered successfully")
except Exception as e:
    print(f"Error registering file_search tool: {e}")
    print(f"Traceback: {traceback.format_exc()}")