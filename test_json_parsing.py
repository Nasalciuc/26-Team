#!/usr/bin/env python3
"""
Test script to debug JSON parsing issues
"""

import json
import re

def repair_json(json_str):
    """Attempt to repair common JSON issues"""
    # Fix missing commas between elements
    json_str = re.sub(r'(\]|\})\s*(\[|\{)', r'\1,\2', json_str)
    json_str = re.sub(r'(")\s*(\[|\{)', r'\1,\2', json_str)
    json_str = re.sub(r'(\]|\})\s*(")', r'\1,\2', json_str)
    json_str = re.sub(r'(\d+)\s*(\[|\{)', r'\1,\2', json_str)
    json_str = re.sub(r'(\]|\})\s*(\d+)', r'\1,\2', json_str)
    json_str = re.sub(r'(true|false|null)\s*(\[|\{)', r'\1,\2', json_str)
    json_str = re.sub(r'(\]|\})\s*(true|false|null)', r'\1,\2', json_str)
    
    # Fix missing commas in object properties
    json_str = re.sub(r'(")\s*(")', r'\1,\2', json_str)
    json_str = re.sub(r'(\d+)\s*(")', r'\1,\2', json_str)
    json_str = re.sub(r'(")\s*(\d+)', r'\1,\2', json_str)
    
    # Fix trailing commas (which are invalid in JSON)
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    
    # Fix missing quotes around property names
    json_str = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_str)
    
    return json_str

def test_json_parsing():
    """Test various JSON parsing scenarios"""
    
    # Example of what might be causing the "Expecting ',' delimiter: line 8 column 6" error
    problematic_json = '''{
  "personas": [
    {
      "name": "John Doe"
      "age": "25-35"
      "location": "New York"
      "description": "Marketing Manager"
      "interests": ["technology" "marketing" "innovation"]
      "needs": ["efficiency" "automation"]
      "frustrations": ["time management" "complex tools"]
    }
  ]
}'''
    
    print("Original problematic JSON:")
    print(problematic_json)
    print("\n" + "="*50 + "\n")
    
    # Try to repair it
    repaired = repair_json(problematic_json)
    print("Repaired JSON:")
    print(repaired)
    print("\n" + "="*50 + "\n")
    
    # Try to parse
    try:
        parsed = json.loads(repaired)
        print("✅ Successfully parsed!")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"❌ Still failed: {e}")
        print(f"Error at line {e.lineno}, column {e.colno}")
        
        # Show the problematic line
        lines = repaired.split('\n')
        if e.lineno <= len(lines):
            print(f"Problematic line {e.lineno}: {lines[e.lineno-1]}")
            print(f"Column {e.colno}: {lines[e.lineno-1][:e.colno]}|{lines[e.lineno-1][e.colno:]}")

if __name__ == "__main__":
    test_json_parsing() 