"""
JSON-based data persistence layer.
Provides generic CRUD operations on JSON files stored in the data/ directory.
Designed to be swapped for a database adapter in Phase 2.
"""

import json
import os

# Data directory sits at project root / data /
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def _ensure_data_dir():
    """Create the data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _get_filepath(filename):
    """Return the full path for a given JSON filename."""
    _ensure_data_dir()
    return os.path.join(DATA_DIR, filename)


def load_all(filename):
    """Load all records from a JSON file. Returns an empty list if the file doesn't exist."""
    filepath = _get_filepath(filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_all(filename, data):
    """Overwrite a JSON file with the given data list."""
    filepath = _get_filepath(filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add(filename, item):
    """Append a single record to the JSON file."""
    data = load_all(filename)
    data.append(item)
    save_all(filename, data)
    return item


def find_by_id(filename, item_id):
    """Find a single record by its 'id' field."""
    data = load_all(filename)
    for item in data:
        if item.get('id') == item_id:
            return item
    return None


def update(filename, item_id, updates):
    """Update a record by id with the given dict of updates. Returns the updated record."""
    data = load_all(filename)
    for item in data:
        if item.get('id') == item_id:
            item.update(updates)
            save_all(filename, data)
            return item
    return None


def delete(filename, item_id):
    """Remove a record by id."""
    data = load_all(filename)
    new_data = [item for item in data if item.get('id') != item_id]
    save_all(filename, new_data)
    return len(data) != len(new_data)


def find_by_field(filename, field, value):
    """Return all records where record[field] == value."""
    data = load_all(filename)
    return [item for item in data if item.get(field) == value]
