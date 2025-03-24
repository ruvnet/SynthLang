"""
Generate sample data for benchmarks.

This script generates sample data for benchmarks by extracting code examples
from the code_examples.md file and saving them as JSON files.
"""
import json
import os
import re
from pathlib import Path

def extract_code_blocks(markdown_file):
    """
    Extract code blocks from a markdown file.
    
    Args:
        markdown_file: Path to the markdown file
        
    Returns:
        List of dictionaries with code blocks and their metadata
    """
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Regular expression to match code blocks with their language
    pattern = r'```(\w+)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    code_blocks = []
    for i, (language, code) in enumerate(matches):
        # Find the heading above this code block
        heading_pattern = r'#+\s+(.*?)\n(?:.*?)```' + language
        heading_match = re.search(heading_pattern, content, re.DOTALL)
        heading = heading_match.group(1) if heading_match else f"Example {i+1}"
        
        code_blocks.append({
            "text": code.strip(),
            "metadata": {
                "language": language,
                "heading": heading,
                "length": len(code.strip()),
                "id": f"{language}_{i+1}",
                "description": f"{language} code example: {heading}"
            }
        })
    
    return code_blocks

def save_samples(code_blocks, output_dir):
    """
    Save code blocks as JSON sample files.
    
    Args:
        code_blocks: List of code block dictionaries
        output_dir: Directory to save the samples in
        
    Returns:
        List of paths to the generated sample files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    filepaths = []
    for i, block in enumerate(code_blocks):
        language = block["metadata"]["language"]
        filename = f"{language}_sample_{i+1}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(block, f, indent=2)
        
        filepaths.append(filepath)
        print(f"Generated sample: {filepath}")
    
    return filepaths

def main():
    """Main entry point for the sample generator."""
    # Get the path to the code examples markdown file
    script_dir = Path(__file__).parent
    markdown_file = script_dir / "code_examples.md"
    output_dir = script_dir / "samples"
    
    # Extract code blocks
    code_blocks = extract_code_blocks(markdown_file)
    print(f"Extracted {len(code_blocks)} code blocks from {markdown_file}")
    
    # Save samples
    filepaths = save_samples(code_blocks, output_dir)
    print(f"Generated {len(filepaths)} samples in {output_dir}")

if __name__ == "__main__":
    main()