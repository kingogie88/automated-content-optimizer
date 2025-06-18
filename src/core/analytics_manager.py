import json
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

class AnalyticsManager:
    def __init__(self):
        self.analytics_data = {}
        self.metrics = {
            'content_views': 0,
            'engagement_rate': 0.0,
            'conversion_rate': 0.0,
            'average_time_on_page': 0.0
        }

    def track_content_performance(self, content_id: str, metrics: Dict[str, Union[int, float]]) -> bool:
        """
        Track performance metrics for a specific content piece.
        
        Args:
            content_id: Unique identifier for the content
            metrics: Dictionary of metrics to track
            
        Returns:
            bool: Success status of the tracking operation
        """
        try:
            if content_id not in self.analytics_data:
                self.analytics_data[content_id] = {
                    'metrics': {},
                    'last_updated': datetime.now().isoformat()
                }
            
            self.analytics_data[content_id]['metrics'].update(metrics)
            self.analytics_data[content_id]['last_updated'] = datetime.now().isoformat()
            return True
        except Exception as e:
            logger.error(f"Error tracking content performance: {str(e)}")
            return False

    def get_content_analytics(self, content_id: str) -> Optional[Dict]:
        """
        Retrieve analytics data for a specific content piece.
        
        Args:
            content_id: Unique identifier for the content
            
        Returns:
            Optional[Dict]: Analytics data for the content or None if not found
        """
        return self.analytics_data.get(content_id)

    def calculate_engagement_rate(self, views: int, interactions: int) -> float:
        """
        Calculate engagement rate based on views and interactions.
        
        Args:
            views: Number of content views
            interactions: Number of user interactions
            
        Returns:
            float: Calculated engagement rate
        """
        if views == 0:
            return 0.0
        return (interactions / views) * 100

    def export_analytics(self, file_path: str) -> bool:
        """
        Export analytics data to a JSON file.
        
        Args:
            file_path: Path to save the analytics data
            
        Returns:
            bool: Success status of the export operation
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(self.analytics_data, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error exporting analytics: {str(e)}")
            return False

    def get_aggregate_metrics(self) -> Dict[str, Union[int, float]]:
        """
        Get aggregate metrics across all content.
        
        Returns:
            Dict[str, Union[int, float]]: Aggregated metrics
        """
        total_views = 0
        total_interactions = 0
        total_time = 0
        content_count = len(self.analytics_data)

        for content_data in self.analytics_data.values():
            metrics = content_data['metrics']
            total_views += metrics.get('views', 0)
            total_interactions += metrics.get('interactions', 0)
            total_time += metrics.get('time_on_page', 0)

        return {
            'total_content': content_count,
            'total_views': total_views,
            'average_engagement_rate': self.calculate_engagement_rate(total_views, total_interactions),
            'average_time_on_page': total_time / content_count if content_count > 0 else 0
        }

    def get_summary(self) -> Dict[str, Union[int, float, str]]:
        """
        Get analytics summary for the router endpoint.
        
        Returns:
            Dict[str, Union[int, float, str]]: Analytics summary
        """
        aggregate_metrics = self.get_aggregate_metrics()
        return {
            'total_content': aggregate_metrics['total_content'],
            'total_views': aggregate_metrics['total_views'],
            'average_engagement_rate': aggregate_metrics['average_engagement_rate'],
            'average_time_on_page': aggregate_metrics['average_time_on_page'],
            'last_updated': datetime.now().isoformat(),
            'status': 'active'
        }

    def get_metrics(self) -> Dict[str, Union[int, float]]:
        """
        Get current metrics.
        
        Returns:
            Dict[str, Union[int, float]]: Current metrics
        """
        return self.metrics.copy()

    def update_metrics(self, new_metrics: Dict[str, Union[int, float]]) -> bool:
        """
        Update metrics with new values.
        
        Args:
            new_metrics: New metrics to update
            
        Returns:
            bool: Success status of the update operation
        """
        try:
            self.metrics.update(new_metrics)
            return True
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
            return False 