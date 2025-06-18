from typing import List, Dict, Optional
import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class SEOOptimizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def optimize_content(
        self,
        content: str,
        target_keywords: Optional[List[str]] = None,
        min_word_count: int = 300,
        max_keyword_density: float = 0.03
    ) -> Dict:
        """
        Optimize content for search engines
        
        Args:
            content: The content to optimize
            target_keywords: List of target keywords
            min_word_count: Minimum word count for content
            max_keyword_density: Maximum keyword density (0-1)
            
        Returns:
            Dict containing optimization results and suggestions
        """
        # Initialize results
        results = {
            "original_content": content,
            "optimized_content": content,
            "metrics": {},
            "suggestions": [],
            "score": 0
        }
        
        # Basic content analysis
        word_count = len(word_tokenize(content))
        results["metrics"]["word_count"] = word_count
        
        if word_count < min_word_count:
            results["suggestions"].append(
                f"Content length ({word_count} words) is below recommended minimum of {min_word_count} words"
            )
        
        # Keyword analysis
        if target_keywords:
            keyword_metrics = self._analyze_keywords(content, target_keywords, max_keyword_density)
            results["metrics"].update(keyword_metrics)
        
        # Readability analysis
        readability_metrics = self._analyze_readability(content)
        results["metrics"].update(readability_metrics)
        
        # Meta tag suggestions
        meta_suggestions = self._generate_meta_suggestions(content, target_keywords)
        results["meta_tags"] = meta_suggestions
        
        # Structure analysis
        structure_analysis = self._analyze_structure(content)
        results["metrics"].update(structure_analysis)
        
        # Calculate overall score
        results["score"] = self._calculate_score(results["metrics"])
        
        # Generate optimization suggestions
        results["suggestions"].extend(self._generate_suggestions(results["metrics"]))
        
        # Optimize content
        results["optimized_content"] = self._optimize_content_structure(
            content,
            results["suggestions"]
        )
        
        return results
    
    def _analyze_keywords(
        self,
        content: str,
        target_keywords: List[str],
        max_density: float
    ) -> Dict:
        """Analyze keyword usage and density"""
        words = word_tokenize(content.lower())
        total_words = len(words)
        
        keyword_metrics = {
            "keyword_density": {},
            "keyword_count": {},
            "keyword_positions": {}
        }
        
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            count = content.lower().count(keyword_lower)
            density = count / total_words if total_words > 0 else 0
            
            keyword_metrics["keyword_count"][keyword] = count
            keyword_metrics["keyword_density"][keyword] = density
            
            # Find keyword positions
            positions = [
                m.start() for m in re.finditer(
                    re.escape(keyword_lower),
                    content.lower()
                )
            ]
            keyword_metrics["keyword_positions"][keyword] = positions
            
            # Check density
            if density > max_density:
                keyword_metrics.setdefault("issues", []).append(
                    f"Keyword '{keyword}' density ({density:.1%}) exceeds recommended maximum of {max_density:.1%}"
                )
        
        return keyword_metrics
    
    def _analyze_readability(self, content: str) -> Dict:
        """Analyze content readability"""
        sentences = nltk.sent_tokenize(content)
        words = word_tokenize(content)
        
        # Calculate average sentence length
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        return {
            "avg_sentence_length": avg_sentence_length,
            "avg_word_length": avg_word_length,
            "sentence_count": len(sentences),
            "paragraph_count": len(content.split('\n\n'))
        }
    
    def _generate_meta_suggestions(
        self,
        content: str,
        target_keywords: Optional[List[str]] = None
    ) -> Dict:
        """Generate meta tag suggestions"""
        words = word_tokenize(content.lower())
        word_freq = Counter(
            word for word in words
            if word.isalnum() and word not in self.stop_words
        )
        
        # Generate title suggestion
        title_words = [word for word, _ in word_freq.most_common(5)]
        if target_keywords:
            title_words = target_keywords[:2] + [w for w in title_words if w not in target_keywords][:3]
        
        title = " ".join(title_words).title()
        
        # Generate description
        sentences = nltk.sent_tokenize(content)
        description = sentences[0] if sentences else ""
        if len(description) > 160:
            description = description[:157] + "..."
        
        return {
            "title": title,
            "description": description,
            "keywords": ", ".join(target_keywords) if target_keywords else ", ".join(word_freq.keys())[:10]
        }
    
    def _analyze_structure(self, content: str) -> Dict:
        """Analyze content structure"""
        # Try to parse as HTML
        try:
            soup = BeautifulSoup(content, 'html.parser')
            headings = {
                f"h{i}": len(soup.find_all(f'h{i}'))
                for i in range(1, 7)
            }
            
            return {
                "headings": headings,
                "links": len(soup.find_all('a')),
                "images": len(soup.find_all('img')),
                "lists": len(soup.find_all(['ul', 'ol']))
            }
        except:
            # Treat as plain text
            return {
                "headings": {},
                "links": 0,
                "images": 0,
                "lists": 0
            }
    
    def _calculate_score(self, metrics: Dict) -> int:
        """Calculate overall SEO score"""
        score = 100
        
        # Word count scoring
        if metrics.get("word_count", 0) < 300:
            score -= 20
        elif metrics.get("word_count", 0) < 600:
            score -= 10
        
        # Readability scoring
        if metrics.get("avg_sentence_length", 0) > 25:
            score -= 10
        
        # Structure scoring
        if not metrics.get("headings", {}).get("h1", 0):
            score -= 10
        
        if metrics.get("links", 0) == 0:
            score -= 5
        
        # Keyword density penalties
        if "issues" in metrics:
            score -= len(metrics["issues"]) * 5
        
        return max(0, min(100, score))
    
    def _generate_suggestions(self, metrics: Dict) -> List[str]:
        """Generate optimization suggestions based on metrics"""
        suggestions = []
        
        # Word count suggestions
        if metrics.get("word_count", 0) < 300:
            suggestions.append("Increase content length to at least 300 words")
        
        # Readability suggestions
        if metrics.get("avg_sentence_length", 0) > 25:
            suggestions.append("Consider breaking down long sentences for better readability")
        
        # Structure suggestions
        headings = metrics.get("headings", {})
        if not headings.get("h1", 0):
            suggestions.append("Add an H1 heading to your content")
        if not headings.get("h2", 0):
            suggestions.append("Consider adding H2 subheadings to structure your content")
        
        if metrics.get("links", 0) == 0:
            suggestions.append("Add relevant internal or external links")
        
        if metrics.get("images", 0) == 0:
            suggestions.append("Consider adding relevant images with alt text")
        
        return suggestions
    
    def _optimize_content_structure(self, content: str, suggestions: List[str]) -> str:
        """Apply basic structural optimizations to content"""
        # This is a placeholder for actual content optimization
        # In a real implementation, this would apply the suggestions
        # to modify the content automatically
        return content 