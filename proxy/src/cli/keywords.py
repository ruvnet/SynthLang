#!/usr/bin/env python
"""
CLI tool for managing keyword detection configurations.

This tool allows users to view, add, edit, and delete keyword patterns,
as well as import and export configurations.
"""
import os
import sys
import argparse
import logging
from typing import Dict, List, Any, Optional
import tomli
import tomli_w
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config.keywords import (
    load_keyword_config,
    save_keyword_config,
    pattern_to_toml,
    toml_to_pattern,
    export_patterns_to_toml,
    import_patterns_from_toml,
    create_default_config,
    get_config_file_path
)
from app.keywords.registry import KeywordPattern, KEYWORD_REGISTRY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("keywords-cli")

def list_patterns(args):
    """List all patterns in the configuration."""
    config = load_keyword_config(args.config)
    
    if not config or "patterns" not in config:
        print("No patterns found in configuration.")
        return
    
    patterns = config.get("patterns", {})
    
    if not patterns:
        print("No patterns found in configuration.")
        return
    
    print(f"Found {len(patterns)} patterns:")
    print("-" * 80)
    
    for name, data in patterns.items():
        enabled = data.get("enabled", True)
        status = "ENABLED" if enabled else "DISABLED"
        required_role = data.get("required_role", "any")
        priority = data.get("priority", 0)
        
        print(f"Name: {name} ({status})")
        print(f"Tool: {data.get('tool', 'unknown')}")
        print(f"Priority: {priority}")
        print(f"Required Role: {required_role}")
        print(f"Description: {data.get('description', '')}")
        print(f"Pattern: {data.get('pattern', '')}")
        print("-" * 80)

def show_pattern(args):
    """Show details for a specific pattern."""
    config = load_keyword_config(args.config)
    
    if not config or "patterns" not in config:
        print("No patterns found in configuration.")
        return
    
    patterns = config.get("patterns", {})
    
    if args.name not in patterns:
        print(f"Pattern '{args.name}' not found.")
        return
    
    data = patterns[args.name]
    enabled = data.get("enabled", True)
    status = "ENABLED" if enabled else "DISABLED"
    required_role = data.get("required_role", "any")
    priority = data.get("priority", 0)
    
    print(f"Name: {args.name} ({status})")
    print(f"Tool: {data.get('tool', 'unknown')}")
    print(f"Priority: {priority}")
    print(f"Required Role: {required_role}")
    print(f"Description: {data.get('description', '')}")
    print(f"Pattern: {data.get('pattern', '')}")

def add_pattern(args):
    """Add a new pattern to the configuration."""
    config = load_keyword_config(args.config)
    
    if not config:
        config = {"settings": {}, "patterns": {}}
    
    if "patterns" not in config:
        config["patterns"] = {}
    
    if args.name in config["patterns"]:
        print(f"Pattern '{args.name}' already exists. Use 'edit' to modify it.")
        return
    
    # Create pattern data
    pattern_data = {
        "name": args.name,
        "pattern": args.pattern,
        "tool": args.tool,
        "description": args.description,
        "priority": args.priority,
        "enabled": not args.disabled
    }
    
    if args.required_role:
        pattern_data["required_role"] = args.required_role
    
    # Add to configuration
    config["patterns"][args.name] = pattern_data
    
    # Save configuration
    if save_keyword_config(config, args.config):
        print(f"Pattern '{args.name}' added successfully.")
    else:
        print(f"Failed to add pattern '{args.name}'.")

def edit_pattern(args):
    """Edit an existing pattern in the configuration."""
    config = load_keyword_config(args.config)
    
    if not config or "patterns" not in config:
        print("No patterns found in configuration.")
        return
    
    if args.name not in config["patterns"]:
        print(f"Pattern '{args.name}' not found.")
        return
    
    # Get existing pattern
    pattern_data = config["patterns"][args.name]
    
    # Update pattern data
    if args.pattern is not None:
        pattern_data["pattern"] = args.pattern
    
    if args.tool is not None:
        pattern_data["tool"] = args.tool
    
    if args.description is not None:
        pattern_data["description"] = args.description
    
    if args.priority is not None:
        pattern_data["priority"] = args.priority
    
    if args.required_role is not None:
        if args.required_role == "":
            # Remove required_role if empty
            pattern_data.pop("required_role", None)
        else:
            pattern_data["required_role"] = args.required_role
    
    if args.enable:
        pattern_data["enabled"] = True
    
    if args.disable:
        pattern_data["enabled"] = False
    
    # Save configuration
    if save_keyword_config(config, args.config):
        print(f"Pattern '{args.name}' updated successfully.")
    else:
        print(f"Failed to update pattern '{args.name}'.")

def delete_pattern(args):
    """Delete a pattern from the configuration."""
    config = load_keyword_config(args.config)
    
    if not config or "patterns" not in config:
        print("No patterns found in configuration.")
        return
    
    if args.name not in config["patterns"]:
        print(f"Pattern '{args.name}' not found.")
        return
    
    # Remove pattern
    del config["patterns"][args.name]
    
    # Save configuration
    if save_keyword_config(config, args.config):
        print(f"Pattern '{args.name}' deleted successfully.")
    else:
        print(f"Failed to delete pattern '{args.name}'.")

def import_config(args):
    """Import patterns from another configuration file."""
    source_config = load_keyword_config(args.source)
    
    if not source_config:
        print(f"Source configuration file '{args.source}' not found or is empty.")
        return
    
    # Load target configuration
    target_config = load_keyword_config(args.config)
    
    if not target_config:
        target_config = {"settings": {}, "patterns": {}}
    
    if "patterns" not in target_config:
        target_config["patterns"] = {}
    
    # Import patterns
    imported = 0
    for name, data in source_config.get("patterns", {}).items():
        if args.overwrite or name not in target_config["patterns"]:
            target_config["patterns"][name] = data
            imported += 1
    
    # Save configuration
    if save_keyword_config(target_config, args.config):
        print(f"Imported {imported} patterns successfully.")
    else:
        print("Failed to import patterns.")

def export_config(args):
    """Export patterns to another configuration file."""
    config = load_keyword_config(args.config)
    
    if not config or "patterns" not in config:
        print("No patterns found in configuration.")
        return
    
    # Save to target file
    if save_keyword_config(config, args.target):
        print(f"Exported {len(config.get('patterns', {}))} patterns to '{args.target}'.")
    else:
        print(f"Failed to export patterns to '{args.target}'.")

def create_default(args):
    """Create a default configuration."""
    config = create_default_config()
    
    # Save configuration
    if save_keyword_config(config, args.config):
        print(f"Created default configuration with {len(config.get('patterns', {}))} patterns.")
    else:
        print("Failed to create default configuration.")

def show_settings(args):
    """Show current settings."""
    config = load_keyword_config(args.config)
    
    if not config or "settings" not in config:
        print("No settings found in configuration.")
        return
    
    settings = config.get("settings", {})
    
    print("Current settings:")
    print("-" * 80)
    
    for key, value in settings.items():
        print(f"{key}: {value}")

def update_settings(args):
    """Update settings in the configuration."""
    config = load_keyword_config(args.config)
    
    if not config:
        config = {"settings": {}, "patterns": {}}
    
    if "settings" not in config:
        config["settings"] = {}
    
    # Update settings
    if args.enable_detection is not None:
        config["settings"]["enable_keyword_detection"] = args.enable_detection
    
    if args.detection_threshold is not None:
        config["settings"]["detection_threshold"] = args.detection_threshold
    
    if args.default_role is not None:
        config["settings"]["default_role"] = args.default_role
    
    # Save configuration
    if save_keyword_config(config, args.config):
        print("Settings updated successfully.")
    else:
        print("Failed to update settings.")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Manage keyword detection configurations")
    parser.add_argument("--config", "-c", help="Path to configuration file", default=get_config_file_path())
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List patterns
    list_parser = subparsers.add_parser("list", help="List all patterns")
    list_parser.set_defaults(func=list_patterns)
    
    # Show pattern
    show_parser = subparsers.add_parser("show", help="Show details for a specific pattern")
    show_parser.add_argument("name", help="Name of the pattern")
    show_parser.set_defaults(func=show_pattern)
    
    # Add pattern
    add_parser = subparsers.add_parser("add", help="Add a new pattern")
    add_parser.add_argument("name", help="Name of the pattern")
    add_parser.add_argument("--pattern", "-p", required=True, help="Regex pattern")
    add_parser.add_argument("--tool", "-t", required=True, help="Tool to invoke")
    add_parser.add_argument("--description", "-d", required=True, help="Description")
    add_parser.add_argument("--priority", "-r", type=int, default=0, help="Priority (default: 0)")
    add_parser.add_argument("--required-role", "-o", help="Required role")
    add_parser.add_argument("--disabled", action="store_true", help="Disable the pattern")
    add_parser.set_defaults(func=add_pattern)
    
    # Edit pattern
    edit_parser = subparsers.add_parser("edit", help="Edit an existing pattern")
    edit_parser.add_argument("name", help="Name of the pattern")
    edit_parser.add_argument("--pattern", "-p", help="Regex pattern")
    edit_parser.add_argument("--tool", "-t", help="Tool to invoke")
    edit_parser.add_argument("--description", "-d", help="Description")
    edit_parser.add_argument("--priority", "-r", type=int, help="Priority")
    edit_parser.add_argument("--required-role", "-o", help="Required role")
    edit_parser.add_argument("--enable", action="store_true", help="Enable the pattern")
    edit_parser.add_argument("--disable", action="store_true", help="Disable the pattern")
    edit_parser.set_defaults(func=edit_pattern)
    
    # Delete pattern
    delete_parser = subparsers.add_parser("delete", help="Delete a pattern")
    delete_parser.add_argument("name", help="Name of the pattern")
    delete_parser.set_defaults(func=delete_pattern)
    
    # Import configuration
    import_parser = subparsers.add_parser("import", help="Import patterns from another configuration file")
    import_parser.add_argument("source", help="Source configuration file")
    import_parser.add_argument("--overwrite", "-o", action="store_true", help="Overwrite existing patterns")
    import_parser.set_defaults(func=import_config)
    
    # Export configuration
    export_parser = subparsers.add_parser("export", help="Export patterns to another configuration file")
    export_parser.add_argument("target", help="Target configuration file")
    export_parser.set_defaults(func=export_config)
    
    # Create default configuration
    default_parser = subparsers.add_parser("create-default", help="Create a default configuration")
    default_parser.set_defaults(func=create_default)
    
    # Show settings
    settings_parser = subparsers.add_parser("settings", help="Show current settings")
    settings_parser.set_defaults(func=show_settings)
    
    # Update settings
    update_parser = subparsers.add_parser("update-settings", help="Update settings")
    update_parser.add_argument("--enable-detection", "-e", type=bool, help="Enable or disable keyword detection")
    update_parser.add_argument("--detection-threshold", "-t", type=float, help="Detection threshold (0.0 to 1.0)")
    update_parser.add_argument("--default-role", "-r", help="Default role")
    update_parser.set_defaults(func=update_settings)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)

if __name__ == "__main__":
    main()