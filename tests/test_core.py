import pytest
from src.core.entity_extractor import EntityLinker
from src.core.schema_generator import SchemaGenerator
from src.core.distribution_manager import DistributionManager
import json

# Test data
SAMPLE_TEXT = "Apple Inc. is a technology company based in Cupertino, California."
SAMPLE_QA_PAIRS = [
    {
        "question": "What is GEO?",
        "answer": "GEO (Generative Engine Optimization) is a technique for optimizing content for AI assistants."
    },
    {
        "question": "How does GEO work?",
        "answer": "GEO works by optimizing content for better AI assistant inclusion and understanding."
    }
]
SAMPLE_CONTENT = {
    "title": "Test Content",
    "content": "# Introduction\nThis is a test content.\n## Section 1\nSome text here.",
    "tags": ["test", "example"],
    "url": "https://example.com/test"
}

@pytest.fixture
def entity_linker(mock_wikipedia, mock_wikidata):
    return EntityLinker()

@pytest.fixture
def schema_generator():
    return SchemaGenerator()

@pytest.fixture
def distribution_manager():
    return DistributionManager()

# Entity Extractor Tests
def test_entity_extraction(entity_linker):
    entities = entity_linker.extract_entities(SAMPLE_TEXT)
    assert len(entities) > 0
    assert any(entity['text'] == 'Apple Inc.' for entity in entities)
    assert all(isinstance(entity['start'], int) for entity in entities)
    assert all(isinstance(entity['end'], int) for entity in entities)

def test_entity_extraction_empty_text(entity_linker):
    entities = entity_linker.extract_entities("")
    assert len(entities) == 0

def test_entity_extraction_special_chars(entity_linker):
    text = "Company: Apple Inc. (AAPL) - Founded: 1976"
    entities = entity_linker.extract_entities(text)
    assert len(entities) > 0

def test_wikidata_linking(entity_linker, mock_wikipedia, mock_wikidata):
    entities = ['Apple Inc.']
    results = entity_linker.link_to_wikidata(entities)
    assert len(results) > 0
    assert 'Apple Inc.' in results
    assert 'wikidata_id' in results['Apple Inc.']
    assert 'wikipedia_url' in results['Apple Inc.']

def test_wikidata_linking_empty_list(entity_linker):
    results = entity_linker.link_to_wikidata([])
    assert len(results) == 0

def test_knowledge_graph_creation(entity_linker):
    graph_data = entity_linker.create_knowledge_graph_json(SAMPLE_TEXT)
    assert 'graph' in graph_data
    assert 'entities' in graph_data
    assert len(graph_data['entities']) > 0
    assert isinstance(graph_data['graph'], str)
    assert json.loads(graph_data['graph'])  # Verify valid JSON

# Schema Generator Tests
def test_schema_generation(schema_generator):
    # Test FAQ schema
    faq_schema = schema_generator.generate_faq_schema(SAMPLE_QA_PAIRS)
    assert '@context' in faq_schema
    assert '@type' in faq_schema
    assert 'FAQPage' in faq_schema
    assert len(json.loads(faq_schema)['mainEntity']) == len(SAMPLE_QA_PAIRS)

    # Test schema validation
    validation_result = schema_generator.validate_schema(faq_schema)
    assert validation_result['valid'] is True

def test_schema_generation_empty_qa(schema_generator):
    faq_schema = schema_generator.generate_faq_schema([])
    assert '@context' in faq_schema
    assert len(json.loads(faq_schema)['mainEntity']) == 0

def test_howto_schema(schema_generator):
    steps = ["Step 1", "Step 2", "Step 3"]
    howto_schema = schema_generator.create_howto_schema(steps)
    assert '@context' in howto_schema
    assert '@type' in howto_schema
    assert 'HowTo' in howto_schema
    assert len(json.loads(howto_schema)['step']) == len(steps)

def test_howto_schema_empty_steps(schema_generator):
    howto_schema = schema_generator.create_howto_schema([])
    assert '@context' in howto_schema
    assert len(json.loads(howto_schema)['step']) == 0

def test_product_schema(schema_generator):
    product_info = {
        "name": "Test Product",
        "description": "A test product",
        "brand": "Test Brand",
        "sku": "TEST123"
    }
    product_schema = schema_generator.build_product_schema(product_info)
    assert '@context' in product_schema
    assert '@type' in product_schema
    assert 'Product' in product_schema
    schema_dict = json.loads(product_schema)
    assert schema_dict['name'] == product_info['name']
    assert schema_dict['description'] == product_info['description']

def test_schema_validation_invalid(schema_generator):
    invalid_schema = '{"@type": "InvalidType"}'
    validation_result = schema_generator.validate_schema(invalid_schema)
    assert validation_result['valid'] is False
    assert 'error' in validation_result

# Distribution Manager Tests
def test_github_readme_generation(distribution_manager):
    readme = distribution_manager.create_github_readme(SAMPLE_CONTENT, "test-repo")
    assert SAMPLE_CONTENT['title'] in readme
    assert "Table of Contents" in readme
    assert "Last Updated" in readme
    assert "Introduction" in readme
    assert "Section 1" in readme

def test_github_readme_empty_content(distribution_manager):
    empty_content = {"title": "", "content": ""}
    readme = distribution_manager.create_github_readme(empty_content, "test-repo")
    assert "Table of Contents" in readme
    assert "Last Updated" in readme

def test_youtube_transcript_generation(distribution_manager):
    transcript = distribution_manager.generate_youtube_transcript(SAMPLE_CONTENT)
    assert SAMPLE_CONTENT['title'] in transcript
    assert "Timestamp" in transcript
    assert SAMPLE_CONTENT['content'] in transcript

def test_youtube_transcript_empty_content(distribution_manager):
    empty_content = {"title": "", "content": ""}
    transcript = distribution_manager.generate_youtube_transcript(empty_content)
    assert "Timestamp" in transcript

@pytest.mark.skip(reason="Requires API credentials")
def test_reddit_posting(distribution_manager):
    result = distribution_manager.post_to_reddit(SAMPLE_CONTENT, "test")
    assert isinstance(result, bool)

@pytest.mark.skip(reason="Requires API credentials")
def test_medium_publishing(distribution_manager):
    url = distribution_manager.publish_to_medium(SAMPLE_CONTENT)
    assert isinstance(url, str) 