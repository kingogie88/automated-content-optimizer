import os
import pytest
from unittest.mock import patch, MagicMock
import json

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'REDDIT_CLIENT_ID': 'test_client_id',
        'REDDIT_CLIENT_SECRET': 'test_client_secret',
        'MEDIUM_API_TOKEN': 'test_medium_token',
        'OPENAI_API_KEY': 'test_openai_key',
        'ANTHROPIC_API_KEY': 'test_anthropic_key',
        'HUGGINGFACE_TOKEN': 'test_hf_token'
    }):
        yield

@pytest.fixture
def mock_wikipedia():
    """Mock Wikipedia API responses"""
    with patch('wikipedia.search') as mock_search, \
         patch('wikipedia.page') as mock_page:
        mock_search.return_value = ['Test Page']
        mock_page.return_value.url = 'https://en.wikipedia.org/wiki/Test'
        yield mock_search, mock_page

@pytest.fixture
def mock_wikidata():
    """Mock Wikidata API responses"""
    with patch('wikidata.client.Client') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = {'id': 'Q123'}
        yield mock_instance

@pytest.fixture
def mock_reddit():
    """Mock Reddit API responses"""
    with patch('praw.Reddit') as mock_reddit:
        mock_instance = mock_reddit.return_value
        mock_subreddit = MagicMock()
        mock_post = MagicMock()
        mock_post.id = '12345'
        mock_subreddit.submit.return_value = mock_post
        mock_instance.subreddit.return_value = mock_subreddit
        yield mock_instance

@pytest.fixture
def mock_medium():
    """Mock Medium API responses"""
    with patch('medium_api.Medium') as mock_medium:
        mock_instance = mock_medium.return_value
        mock_post = MagicMock()
        mock_post.url = 'https://medium.com/test-post'
        mock_instance.create_post.return_value = mock_post
        yield mock_instance

@pytest.fixture
def mock_spacy():
    """Mock spaCy NLP pipeline"""
    with patch('spacy.load') as mock_load:
        mock_nlp = MagicMock()
        mock_doc = MagicMock()
        mock_ent = MagicMock()
        mock_ent.text = 'Apple Inc.'
        mock_ent.label_ = 'ORG'
        mock_ent.start_char = 0
        mock_ent.end_char = 9
        mock_doc.ents = [mock_ent]
        mock_nlp.return_value = mock_doc
        mock_load.return_value = mock_nlp
        yield mock_nlp

@pytest.fixture
def sample_knowledge_graph():
    """Sample knowledge graph data"""
    return {
        'graph': json.dumps({
            '@context': 'https://schema.org',
            '@graph': [
                {
                    '@id': 'http://example.org/entity/Apple_Inc',
                    '@type': 'Organization',
                    'name': 'Apple Inc.'
                }
            ]
        }),
        'entities': [
            {
                'text': 'Apple Inc.',
                'label': 'ORG',
                'start': 0,
                'end': 9
            }
        ]
    }

@pytest.fixture
def sample_schema():
    """Sample schema data"""
    return {
        'FAQ': {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [
                {
                    '@type': 'Question',
                    'name': 'What is GEO?',
                    'acceptedAnswer': {
                        '@type': 'Answer',
                        'text': 'GEO is a technique for optimizing content.'
                    }
                }
            ]
        },
        'HowTo': {
            '@context': 'https://schema.org',
            '@type': 'HowTo',
            'step': [
                {
                    '@type': 'HowToStep',
                    'position': 1,
                    'text': 'Step 1'
                }
            ]
        }
    } 