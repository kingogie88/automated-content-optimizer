from typing import List, Dict, Optional
import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class SEOOptimizer:
    def __init__(self):
        """Initialize the SEO optimizer with stop words."""
        try:
            # Try to download NLTK data if not available
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            from nltk.corpus import stopwords
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            logger.warning(f"Could not load NLTK stopwords: {e}")
            # Fallback to basic stop words
            self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    def optimize_content(
        self,
        content: str,
        target_keywords: Optional[List[str]] = None,
        min_word_count: int = 300,
        max_keyword_density: float = 0.05
    ) -> Dict:
        """
        Optimize content for SEO.
        
        Args:
            content: The content to optimize
            target_keywords: List of target keywords
            min_word_count: Minimum word count for good SEO
            max_keyword_density: Maximum keyword density (0.0 to 1.0)
            
        Returns:
            Dictionary containing optimization results
        """
        try:
            # Clean content
            clean_content = self._clean_content(content)
            
            # Analyze content
            word_count = len(clean_content.split())
            keyword_usage = self._analyze_keywords(clean_content, target_keywords or [])
            readability_score = self._analyze_readability(clean_content)
            structure_score = self._analyze_structure(content)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(
                word_count, keyword_usage, readability_score, structure_score, 
                min_word_count, max_keyword_density
            )
            
            # Optimize content
            optimized_content = self._optimize_structure(content, suggestions)
            
            # Calculate overall score
            score = self._calculate_score(word_count, keyword_usage, readability_score, structure_score)
            
            return {
                "original_content": content,
                "optimized_content": optimized_content,
                "metrics": {
                    "word_count": word_count,
                    "keyword_usage": keyword_usage,
                    "readability_score": readability_score,
                    "structure_score": structure_score
                },
                "suggestions": suggestions,
                "score": score
            }
        except Exception as e:
            logger.error(f"Error in SEO optimization: {e}")
            return {
                "original_content": content,
                "optimized_content": content,
                "metrics": {"error": str(e)},
                "suggestions": ["Error occurred during optimization"],
                "score": 0
            }
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize content."""
        # Remove HTML tags
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _analyze_keywords(self, content: str, keywords: List[str]) -> Dict:
        """Analyze keyword usage in content."""
        if not keywords:
            return {"density": 0, "count": 0, "positions": []}
        
        content_lower = content.lower()
        total_words = len(content.split())
        keyword_count = 0
        positions = []
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            keyword_count += count
            
            # Find positions
            start = 0
            while True:
                pos = content_lower.find(keyword_lower, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
        
        density = keyword_count / total_words if total_words > 0 else 0
        
        return {
            "density": density,
            "count": keyword_count,
            "positions": positions
        }
    
    def _analyze_readability(self, content: str) -> float:
        """Analyze content readability using basic metrics."""
        sentences = re.split(r'[.!?]+', content)
        words = content.split()
        
        if not sentences or not words:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple readability score (0-100)
        if avg_sentence_length <= 15:
            return 90.0
        elif avg_sentence_length <= 20:
            return 75.0
        elif avg_sentence_length <= 25:
            return 60.0
        else:
            return 40.0
    
    def _analyze_structure(self, content: str) -> float:
        """Analyze content structure."""
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check for headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        has_h1 = bool(soup.find('h1'))
        
        # Check for paragraphs
        paragraphs = soup.find_all('p')
        
        # Check for lists
        lists = soup.find_all(['ul', 'ol'])
        
        score = 0
        if has_h1:
            score += 30
        if len(headings) >= 2:
            score += 20
        if len(paragraphs) >= 3:
            score += 25
        if lists:
            score += 15
        if len(content) > 1000:
            score += 10
            
        return min(score, 100.0)
    
    def _generate_suggestions(self, word_count: int, keyword_usage: Dict, 
                            readability_score: float, structure_score: float,
                            min_word_count: int, max_keyword_density: float) -> List[str]:
        """Generate optimization suggestions."""
        suggestions = []
        
        if word_count < min_word_count:
            suggestions.append(f"Increase content length to at least {min_word_count} words")
        
        if keyword_usage["density"] > max_keyword_density:
            suggestions.append("Reduce keyword density to avoid keyword stuffing")
        elif keyword_usage["density"] < 0.01:
            suggestions.append("Increase keyword usage for better SEO")
        
        if readability_score < 60:
            suggestions.append("Improve readability by using shorter sentences")
        
        if structure_score < 70:
            suggestions.append("Improve content structure with proper headings and paragraphs")
        
        if not suggestions:
            suggestions.append("Content is well optimized for SEO")
        
        return suggestions
    
    def _optimize_structure(self, content: str, suggestions: List[str]) -> str:
        """Optimize content structure based on suggestions."""
        # For now, return the original content
        # In a full implementation, this would make structural improvements
        return content
    
    def _calculate_score(self, word_count: int, keyword_usage: Dict, 
                        readability_score: float, structure_score: float) -> float:
        """Calculate overall SEO score."""
        # Weighted average of different metrics
        weights = {
            "word_count": 0.2,
            "keyword_usage": 0.3,
            "readability": 0.25,
            "structure": 0.25
        }
        
        # Normalize word count score (0-100)
        word_count_score = min(100, (word_count / 1000) * 100)
        
        # Normalize keyword usage score
        keyword_score = min(100, keyword_usage["density"] * 2000)
        
        total_score = (
            word_count_score * weights["word_count"] +
            keyword_score * weights["keyword_usage"] +
            readability_score * weights["readability"] +
            structure_score * weights["structure"]
        )
        
        return round(total_score, 2) 