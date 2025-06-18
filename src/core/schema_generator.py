from typing import Dict, List, Optional
import json
from jsonschema import validate, ValidationError
import logging

class SchemaGenerator:
    """
    Generate and validate structured data for better AI understanding
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.schema_templates = {
            'FAQ': {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": []
            },
            'HowTo': {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "step": []
            },
            'Product': {
                "@context": "https://schema.org",
                "@type": "Product"
            }
        }

    def generate_faq_schema(self, qa_pairs: List[Dict]) -> str:
        """
        Generate FAQ schema from Q&A pairs
        """
        try:
            schema = self.schema_templates['FAQ'].copy()
            for qa in qa_pairs:
                schema['mainEntity'].append({
                    "@type": "Question",
                    "name": qa['question'],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": qa['answer']
                    }
                })
            return json.dumps(schema, indent=2)
        except Exception as e:
            self.logger.error(f"Error generating FAQ schema: {str(e)}")
            return "{}"

    def create_howto_schema(self, steps: List[str]) -> str:
        """
        Create HowTo schema from steps
        """
        try:
            schema = self.schema_templates['HowTo'].copy()
            for i, step in enumerate(steps, 1):
                schema['step'].append({
                    "@type": "HowToStep",
                    "position": i,
                    "text": step
                })
            return json.dumps(schema, indent=2)
        except Exception as e:
            self.logger.error(f"Error creating HowTo schema: {str(e)}")
            return "{}"

    def build_product_schema(self, product_info: Dict) -> str:
        """
        Build product schema from product information
        """
        try:
            schema = self.schema_templates['Product'].copy()
            schema.update(product_info)
            return json.dumps(schema, indent=2)
        except Exception as e:
            self.logger.error(f"Error building product schema: {str(e)}")
            return "{}"

    def validate_schema(self, schema_json: str) -> Dict:
        """
        Validate schema against JSON Schema
        """
        try:
            schema = json.loads(schema_json)
            # Define validation schema based on type
            if schema.get('@type') == 'FAQPage':
                validation_schema = {
                    "type": "object",
                    "required": ["@context", "@type", "mainEntity"],
                    "properties": {
                        "@context": {"type": "string"},
                        "@type": {"type": "string"},
                        "mainEntity": {"type": "array"}
                    }
                }
            elif schema.get('@type') == 'HowTo':
                validation_schema = {
                    "type": "object",
                    "required": ["@context", "@type", "step"],
                    "properties": {
                        "@context": {"type": "string"},
                        "@type": {"type": "string"},
                        "step": {"type": "array"}
                    }
                }
            elif schema.get('@type') == 'Product':
                validation_schema = {
                    "type": "object",
                    "required": ["@context", "@type"],
                    "properties": {
                        "@context": {"type": "string"},
                        "@type": {"type": "string"}
                    }
                }
            else:
                return {
                    'valid': False,
                    'error': 'Unknown schema type'
                }

            validate(instance=schema, schema=validation_schema)
            return {
                'valid': True,
                'message': 'Schema is valid'
            }
        except ValidationError as e:
            return {
                'valid': False,
                'error': str(e)
            }
        except Exception as e:
            self.logger.error(f"Error validating schema: {str(e)}")
            return {
                'valid': False,
                'error': str(e)
            } 