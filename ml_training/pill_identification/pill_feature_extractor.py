"""
Pill Feature Extractor - Extract visual features from pill images
Uses pretrained MobileNetV2 for feature extraction
"""
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import json
from pathlib import Path
from datetime import datetime


class PillFeatureExtractor:
    """
    Extract visual features from pill images using pretrained CNN
    """
    
    def __init__(self, model_type='mobilenet_v2', device='cpu'):
        """
        Initialize feature extractor
        
        Args:
            model_type: Type of pretrained model to use
            device: 'cpu' or 'cuda'
        """
        self.device = device
        self.model_type = model_type
        
        # Load pretrained model
        if model_type == 'mobilenet_v2':
            self.model = models.mobilenet_v2(weights='DEFAULT')
            # Remove classification layer, keep feature extractor
            self.model.classifier = nn.Identity()
            self.feature_dim = 1280
        elif model_type == 'resnet50':
            self.model = models.resnet50(weights='DEFAULT')
            # Remove final FC layer
            self.model.fc = nn.Identity()
            self.feature_dim = 2048
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.model.to(self.device)
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
    
    def extract_features(self, image_path):
        """
        Extract features from a single pill image
        
        Args:
            image_path: Path to pill image
            
        Returns:
            Feature vector (numpy array)
        """
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(img).unsqueeze(0).to(self.device)
        
        # Extract features
        with torch.no_grad():
            features = self.model(img_tensor)
        
        # Convert to numpy and flatten
        features_np = features.cpu().numpy().flatten()
        
        # Normalize features (L2 normalization)
        features_np = features_np / (np.linalg.norm(features_np) + 1e-8)
        
        return features_np
    
    def extract_features_from_dataset(self, dataset_dir, output_file=None):
        """
        Extract features from all images in a dataset
        
        Args:
            dataset_dir: Directory containing pill images
            output_file: Path to save feature database (JSON)
            
        Returns:
            Feature database dictionary
        """
        dataset_dir = Path(dataset_dir)
        
        print(f"\n{'='*80}")
        print("EXTRACTING PILL FEATURES")
        print(f"{'='*80}")
        print(f"Dataset: {dataset_dir}")
        print(f"Model: {self.model_type}")
        print(f"Feature dimension: {self.feature_dim}")
        
        # Find all images
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_files = []
        for ext in image_extensions:
            image_files.extend(list(dataset_dir.glob(f'*{ext}')))
            image_files.extend(list(dataset_dir.glob(f'*{ext.upper()}')))
        
        print(f"Found {len(image_files)} images")
        
        # Extract features
        feature_database = {
            'model_type': self.model_type,
            'feature_dim': self.feature_dim,
            'extraction_date': datetime.now().isoformat(),
            'pills': []
        }
        
        for i, image_path in enumerate(image_files, 1):
            try:
                print(f"[{i}/{len(image_files)}] Processing {image_path.name}...", end=' ')
                
                # Extract features
                features = self.extract_features(image_path)
                
                # Parse NDC code from filename (format: NDC_other_info.jpg)
                ndc_code = image_path.stem.split('_')[0]
                
                # Store in database
                pill_entry = {
                    'filename': image_path.name,
                    'ndc_code': ndc_code,
                    'features': features.tolist(),
                    'image_path': str(image_path)
                }
                
                feature_database['pills'].append(pill_entry)
                print("✓")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print(f"\n✓ Extracted features from {len(feature_database['pills'])} pills")
        
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(feature_database, f, indent=2)
            
            print(f"✓ Saved feature database to: {output_path}")
        
        return feature_database
    
    def compute_similarity(self, features1, features2):
        """
        Compute cosine similarity between two feature vectors
        
        Args:
            features1: First feature vector
            features2: Second feature vector
            
        Returns:
            Similarity score (0-1, higher is more similar)
        """
        # Convert to numpy if needed
        if isinstance(features1, list):
            features1 = np.array(features1)
        if isinstance(features2, list):
            features2 = np.array(features2)
        
        # Cosine similarity
        similarity = np.dot(features1, features2)
        
        return float(similarity)
    
    def find_similar_pills(self, query_image_path, feature_database, top_k=3):
        """
        Find similar pills from database
        
        Args:
            query_image_path: Path to query pill image
            feature_database: Feature database (from extract_features_from_dataset)
            top_k: Number of top matches to return
            
        Returns:
            List of (pill_info, similarity_score) tuples
        """
        # Extract features from query image
        query_features = self.extract_features(query_image_path)
        
        # Compute similarities with all pills in database
        similarities = []
        for pill in feature_database['pills']:
            pill_features = np.array(pill['features'])
            similarity = self.compute_similarity(query_features, pill_features)
            similarities.append((pill, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k matches
        return similarities[:top_k]


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract features from pill images")
    parser.add_argument('dataset_dir', type=str, help='Directory containing pill images')
    parser.add_argument('--output', type=str, default='pill_identification/pill_features.json',
                       help='Output file for feature database')
    parser.add_argument('--model', type=str, default='mobilenet_v2',
                       choices=['mobilenet_v2', 'resnet50'],
                       help='Pretrained model to use')
    
    args = parser.parse_args()
    
    # Initialize extractor
    extractor = PillFeatureExtractor(model_type=args.model)
    
    # Extract features
    feature_db = extractor.extract_features_from_dataset(
        dataset_dir=args.dataset_dir,
        output_file=args.output
    )
    
    print(f"\n{'='*80}")
    print("FEATURE EXTRACTION COMPLETE")
    print(f"{'='*80}")
    print(f"Total pills: {len(feature_db['pills'])}")
    print(f"Feature dimension: {feature_db['feature_dim']}")
    print(f"Database saved to: {args.output}")


if __name__ == "__main__":
    main()
