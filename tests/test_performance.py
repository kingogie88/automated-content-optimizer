import pytest
import time
from src.core.entity_extractor import EntityLinker
from src.core.schema_generator import SchemaGenerator
from src.core.distribution_manager import DistributionManager
import json

# Test data
LARGE_TEXT = "Apple Inc. is a technology company based in Cupertino, California. " * 100
LARGE_QA_PAIRS = [
    {
        "question": f"Question {i}",
        "answer": f"Answer {i}"
    } for i in range(100)
]

@pytest.fixture
def entity_linker():
    return EntityLinker()

@pytest.fixture
def schema_generator():
    return SchemaGenerator()

@pytest.fixture
def distribution_manager():
    return DistributionManager()

def test_entity_extraction_performance(entity_linker):
    """Test performance of entity extraction on large text"""
    start_time = time.time()
    entities = entity_linker.extract_entities(LARGE_TEXT)
    end_time = time.time()
    
    processing_time = end_time - start_time
    assert processing_time < 5.0  # Should process within 5 seconds
    assert len(entities) > 0

def test_wikidata_linking_performance(entity_linker):
    """Test performance of Wikidata linking"""
    entities = ['Apple Inc.', 'Microsoft', 'Google', 'Amazon', 'Meta']
    start_time = time.time()
    results = entity_linker.link_to_wikidata(entities)
    end_time = time.time()
    
    processing_time = end_time - start_time
    assert processing_time < 10.0  # Should process within 10 seconds
    assert len(results) > 0

def test_schema_generation_performance(schema_generator):
    """Test performance of schema generation with large dataset"""
    start_time = time.time()
    schema = schema_generator.generate_faq_schema(LARGE_QA_PAIRS)
    end_time = time.time()
    
    processing_time = end_time - start_time
    assert processing_time < 3.0  # Should process within 3 seconds
    assert len(json.loads(schema)['mainEntity']) == len(LARGE_QA_PAIRS)

def test_knowledge_graph_performance(entity_linker):
    """Test performance of knowledge graph creation"""
    start_time = time.time()
    graph_data = entity_linker.create_knowledge_graph_json(LARGE_TEXT)
    end_time = time.time()
    
    processing_time = end_time - start_time
    assert processing_time < 8.0  # Should process within 8 seconds
    assert 'graph' in graph_data
    assert 'entities' in graph_data

def test_memory_usage(entity_linker):
    """Test memory usage during entity extraction"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform entity extraction
    entities = entity_linker.extract_entities(LARGE_TEXT)
    
    final_memory = process.memory_info().rss
    memory_increase = (final_memory - initial_memory) / 1024 / 1024  # Convert to MB
    
    assert memory_increase < 500  # Should not use more than 500MB additional memory
    assert len(entities) > 0

def test_concurrent_processing(entity_linker):
    """Test concurrent processing capabilities"""
    import concurrent.futures
    
    texts = [LARGE_TEXT] * 5
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(entity_linker.extract_entities, texts))
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    assert processing_time < 15.0  # Should process all within 15 seconds
    assert all(len(result) > 0 for result in results)

def test_schema_validation_performance(schema_generator):
    """Test performance of schema validation"""
    schema = schema_generator.generate_faq_schema(LARGE_QA_PAIRS)
    
    start_time = time.time()
    for _ in range(100):  # Test multiple validations
        result = schema_generator.validate_schema(schema)
        assert result['valid'] is True
    end_time = time.time()
    
    processing_time = end_time - start_time
    assert processing_time < 5.0  # Should validate 100 times within 5 seconds 