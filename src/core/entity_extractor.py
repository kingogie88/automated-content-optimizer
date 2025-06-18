from typing import Dict, List, Optional
import spacy
from rdflib import Graph, URIRef, Literal
import wikipedia
from wikidata.client import Client
import logging

class EntityLinker:
    """
    Extract and link entities to major knowledge graphs
    """
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.wikidata_client = Client()
        self.logger = logging.getLogger(__name__)

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract named entities using spaCy
        """
        try:
            doc = self.nlp(text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            return entities
        except Exception as e:
            self.logger.error(f"Error extracting entities: {str(e)}")
            return []

    def link_to_wikidata(self, entities: List[str]) -> Dict:
        """
        Link entities to Wikidata
        """
        try:
            results = {}
            for entity in entities:
                # Search Wikidata
                search_results = wikipedia.search(entity, results=1)
                if search_results:
                    page = wikipedia.page(search_results[0])
                    # Get Wikidata ID from Wikipedia page
                    wikidata_id = self._get_wikidata_id(page.url)
                    if wikidata_id:
                        results[entity] = {
                            'wikidata_id': wikidata_id,
                            'wikipedia_url': page.url
                        }
            return results
        except Exception as e:
            self.logger.error(f"Error linking to Wikidata: {str(e)}")
            return {}

    def _get_wikidata_id(self, wikipedia_url: str) -> Optional[str]:
        """
        Extract Wikidata ID from Wikipedia URL
        """
        try:
            # Implementation depends on Wikipedia API
            # This is a placeholder for the actual implementation
            return None
        except Exception as e:
            self.logger.error(f"Error getting Wikidata ID: {str(e)}")
            return None

    def generate_wikidata_template(self, entity: Dict) -> str:
        """
        Generate Wikidata template for an entity
        """
        try:
            template = f"""{{{{Wikidata|{entity.get('wikidata_id', '')}}}}}"""
            return template
        except Exception as e:
            self.logger.error(f"Error generating Wikidata template: {str(e)}")
            return ""

    def create_knowledge_graph_json(self, content: str) -> Dict:
        """
        Create a knowledge graph representation of the content
        """
        try:
            g = Graph()
            entities = self.extract_entities(content)
            
            for entity in entities:
                # Create subject
                subject = URIRef(f"http://example.org/entity/{entity['text']}")
                # Add entity type
                g.add((subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), 
                      Literal(entity['label'])))
                
                # Link to Wikidata if available
                wikidata_info = self.link_to_wikidata([entity['text']])
                if entity['text'] in wikidata_info:
                    g.add((subject, URIRef("http://www.wikidata.org/entity/"), 
                          Literal(wikidata_info[entity['text']]['wikidata_id'])))

            return {
                'graph': g.serialize(format='json-ld'),
                'entities': entities
            }
        except Exception as e:
            self.logger.error(f"Error creating knowledge graph: {str(e)}")
            return {'graph': '{}', 'entities': []} 