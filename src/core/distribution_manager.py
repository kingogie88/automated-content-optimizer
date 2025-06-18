from typing import Dict, Optional
import praw
import requests
from medium_api import Medium
import logging
import os
from datetime import datetime

class DistributionManager:
    """
    Automate content distribution to high-index platforms
    that AI systems commonly scrape
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.reddit_client = self._init_reddit()
        self.medium_client = self._init_medium()

    def _init_reddit(self) -> Optional[praw.Reddit]:
        """
        Initialize Reddit client
        """
        try:
            return praw.Reddit(
                client_id=os.getenv('REDDIT_CLIENT_ID'),
                client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                user_agent='GEO AI Optimizer/1.0'
            )
        except Exception as e:
            self.logger.error(f"Error initializing Reddit client: {str(e)}")
            return None

    def _init_medium(self) -> Optional[Medium]:
        """
        Initialize Medium client
        """
        try:
            return Medium(os.getenv('MEDIUM_API_TOKEN'))
        except Exception as e:
            self.logger.error(f"Error initializing Medium client: {str(e)}")
            return None

    def post_to_reddit(self, content: Dict, subreddit: str) -> bool:
        """
        Post content to Reddit
        """
        try:
            if not self.reddit_client:
                raise Exception("Reddit client not initialized")

            subreddit_instance = self.reddit_client.subreddit(subreddit)
            
            # Create post
            post = subreddit_instance.submit(
                title=content['title'],
                selftext=content['content'],
                url=content.get('url', ''),
                flair_id=content.get('flair_id')
            )
            
            return bool(post.id)
        except Exception as e:
            self.logger.error(f"Error posting to Reddit: {str(e)}")
            return False

    def publish_to_medium(self, content: Dict) -> str:
        """
        Publish content to Medium
        """
        try:
            if not self.medium_client:
                raise Exception("Medium client not initialized")

            # Create post
            post = self.medium_client.create_post(
                title=content['title'],
                content=content['content'],
                tags=content.get('tags', []),
                publish_status='public'
            )
            
            return post.url
        except Exception as e:
            self.logger.error(f"Error publishing to Medium: {str(e)}")
            return ""

    def create_github_readme(self, content: Dict, repo_name: str) -> str:
        """
        Create GitHub README content
        """
        try:
            readme_content = f"""# {content['title']}

{content['content']}

## Table of Contents
{self._generate_toc(content['content'])}

## Last Updated
{datetime.now().strftime('%Y-%m-%d')}
"""
            return readme_content
        except Exception as e:
            self.logger.error(f"Error creating GitHub README: {str(e)}")
            return ""

    def generate_youtube_transcript(self, content: Dict) -> str:
        """
        Generate YouTube transcript format
        """
        try:
            transcript = f"""Title: {content['title']}

{content['content']}

Timestamp: {datetime.now().strftime('%H:%M:%S')}
"""
            return transcript
        except Exception as e:
            self.logger.error(f"Error generating YouTube transcript: {str(e)}")
            return ""

    def _generate_toc(self, content: str) -> str:
        """
        Generate table of contents from content
        """
        try:
            # Simple implementation - can be enhanced with proper markdown parsing
            lines = content.split('\n')
            toc = []
            for line in lines:
                if line.startswith('#'):
                    level = len(line.split()[0])
                    title = line.lstrip('#').strip()
                    toc.append(f"{'  ' * (level-1)}- {title}")
            return '\n'.join(toc)
        except Exception as e:
            self.logger.error(f"Error generating table of contents: {str(e)}")
            return "" 