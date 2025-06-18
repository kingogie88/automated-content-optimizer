import pytest
from src.core.analytics_manager import AnalyticsManager
import json
import os
from datetime import datetime

@pytest.fixture
def analytics_manager():
    return AnalyticsManager()

@pytest.fixture
def sample_metrics():
    return {
        'views': 100,
        'interactions': 25,
        'time_on_page': 180,
        'conversions': 5
    }

def test_track_content_performance(analytics_manager, sample_metrics):
    content_id = "test_content_1"
    result = analytics_manager.track_content_performance(content_id, sample_metrics)
    assert result is True
    assert content_id in analytics_manager.analytics_data
    assert 'metrics' in analytics_manager.analytics_data[content_id]
    assert 'last_updated' in analytics_manager.analytics_data[content_id]
    assert analytics_manager.analytics_data[content_id]['metrics'] == sample_metrics

def test_get_content_analytics(analytics_manager, sample_metrics):
    content_id = "test_content_2"
    analytics_manager.track_content_performance(content_id, sample_metrics)
    analytics = analytics_manager.get_content_analytics(content_id)
    assert analytics is not None
    assert analytics['metrics'] == sample_metrics

def test_get_content_analytics_nonexistent(analytics_manager):
    analytics = analytics_manager.get_content_analytics("nonexistent_content")
    assert analytics is None

def test_calculate_engagement_rate(analytics_manager):
    rate = analytics_manager.calculate_engagement_rate(100, 25)
    assert rate == 25.0
    rate = analytics_manager.calculate_engagement_rate(0, 25)
    assert rate == 0.0

def test_export_analytics(analytics_manager, sample_metrics, tmp_path):
    content_id = "test_content_3"
    analytics_manager.track_content_performance(content_id, sample_metrics)
    
    export_path = tmp_path / "analytics.json"
    result = analytics_manager.export_analytics(str(export_path))
    
    assert result is True
    assert export_path.exists()
    
    with open(export_path) as f:
        exported_data = json.load(f)
        assert content_id in exported_data
        assert exported_data[content_id]['metrics'] == sample_metrics

def test_get_aggregate_metrics(analytics_manager):
    # Add multiple content pieces
    analytics_manager.track_content_performance("content_1", {
        'views': 100,
        'interactions': 20,
        'time_on_page': 180
    })
    analytics_manager.track_content_performance("content_2", {
        'views': 200,
        'interactions': 50,
        'time_on_page': 240
    })
    
    metrics = analytics_manager.get_aggregate_metrics()
    assert metrics['total_content'] == 2
    assert metrics['total_views'] == 300
    assert metrics['average_engagement_rate'] == pytest.approx(23.33, 0.01)
    assert metrics['average_time_on_page'] == 210.0

def test_error_handling(analytics_manager):
    # Test with invalid metrics
    result = analytics_manager.track_content_performance("test_content", None)
    assert result is False
    
    # Test export to invalid path
    result = analytics_manager.export_analytics("/invalid/path/analytics.json")
    assert result is False 