"""
Convert medicinal plants metadata to frontend format
Converts the comprehensive JSON metadata to the format expected by the React frontend
"""
import json
from pathlib import Path

# Paths
METADATA_PATH = Path(__file__).parent.parent / "data" / "medicinal_plants_metadata.json"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "frontend_plants_data.js"

def convert_to_frontend_format(metadata):
    """
    Convert metadata JSON to frontend JavaScript format
    
    Args:
        metadata: Dictionary with plant metadata
        
    Returns:
        JavaScript-formatted string
    """
    plants = []
    
    for plant_name, data in metadata.items():
        plant_obj = {
            'id': data['id'],
            'name': data['name'],
            'scientificName': data['scientificName'],
            'family': data['family'],
            'nativeRegion': data['nativeRegion'],
            'imageUrl': data['imageUrl'],
            'uses': data['uses'],
            'activeCompounds': data['activeCompounds'],
            'partsUsed': data['partsUsed'],
            'precautions': data['precautions'],
            'sideEffects': data['sideEffects'],
            'storage': data['storage'],
            'description': data['description'],
            'remedies': data['remedies']
        }
        plants.append(plant_obj)
    
    # Convert to JavaScript format
    js_content = "// Medicinal Plants Data for Frontend\n"
    js_content += "// Auto-generated from metadata\n\n"
    js_content += "const medicinalPlants = " + json.dumps(plants, indent=2) + "\n\n"
    js_content += "export { medicinalPlants }\n"
    js_content += "export default medicinalPlants\n"
    
    return js_content

def main():
    print("Converting metadata to frontend format...")
    
    # Load metadata
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print(f"Loaded metadata for {len(metadata)} plants")
    
    # Convert to frontend format
    js_content = convert_to_frontend_format(metadata)
    
    # Save to file
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✓ Frontend data saved to: {OUTPUT_PATH}")
    print("\nTo update frontend:")
    print("1. Copy the content from frontend_plants_data.js")
    print("2. Replace the medicinalPlants array in Medicine/src/data/mockData.js")
    print("3. Keep the class IDs consistent with model predictions")

if __name__ == "__main__":
    main()
