from typing import List, Dict, Optional
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import pipeline
import openai
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GEOOptimizer:
    def __init__(self):
        """Initialize the GEO Optimizer with necessary models and configurations"""
        # Set up API keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Initialize AI clients
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        if self.anthropic_api_key:
            self.anthropic = Anthropic(api_key=self.anthropic_api_key)
        
        # Initialize sentiment analyzer
        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis")
        except:
            self.sentiment_analyzer = None
    
    def optimize_content(
        self,
        content: str,
        target_platforms: List[str] = ["chatgpt", "claude", "voice"],
        optimization_goals: List[str] = ["context", "factual", "voice_search"]
    ) -> Dict:
        """
        Optimize content for AI platforms
        
        Args:
            content: The content to optimize
            target_platforms: List of target AI platforms
            optimization_goals: List of optimization goals
            
        Returns:
            Dict containing optimization results and suggestions
        """
        results = {
            "original_content": content,
            "optimized_content": content,
            "metrics": {},
            "suggestions": [],
            "score": 0
        }
        
        # Context clarity analysis
        context_metrics = self._analyze_context_clarity(content)
        results["metrics"].update(context_metrics)
        
        # Factual consistency analysis
        if "factual" in optimization_goals:
            factual_metrics = self._analyze_factual_consistency(content)
            results["metrics"].update(factual_metrics)
        
        # Voice search optimization
        if "voice_search" in optimization_goals:
            voice_metrics = self._optimize_for_voice_search(content)
            results["metrics"].update(voice_metrics)
        
        # Platform-specific optimization
        for platform in target_platforms:
            platform_metrics = self._optimize_for_platform(content, platform)
            results["metrics"][f"{platform}_metrics"] = platform_metrics
        
        # Generate suggestions
        results["suggestions"] = self._generate_suggestions(results["metrics"])
        
        # Calculate overall score
        results["score"] = self._calculate_score(results["metrics"])
        
        # Apply optimizations
        results["optimized_content"] = self._apply_optimizations(
            content,
            results["suggestions"],
            target_platforms
        )
        
        return results
    
    def _analyze_context_clarity(self, content: str) -> Dict:
        """Analyze the clarity and context of the content"""
        sentences = sent_tokenize(content)
        words = word_tokenize(content)
        
        metrics = {
            "context_clarity": {
                "sentence_count": len(sentences),
                "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
                "unique_entities": len(set(words)) / len(words) if words else 0
            }
        }
        
        # Analyze sentence complexity
        complex_sentences = sum(1 for s in sentences if len(word_tokenize(s)) > 25)
        metrics["context_clarity"]["complex_sentence_ratio"] = complex_sentences / len(sentences) if sentences else 0
        
        # Analyze contextual transitions
        transition_words = ["however", "therefore", "furthermore", "moreover", "consequently"]
        transition_count = sum(1 for word in words if word.lower() in transition_words)
        metrics["context_clarity"]["transition_density"] = transition_count / len(sentences) if sentences else 0
        
        return metrics
    
    def _analyze_factual_consistency(self, content: str) -> Dict:
        """Analyze the factual consistency of the content"""
        sentences = sent_tokenize(content)
        
        metrics = {
            "factual_consistency": {
                "claim_count": 0,
                "citation_count": 0,
                "verifiable_statements": 0
            }
        }
        
        # Count potential claims (sentences with numbers, statistics, or specific assertions)
        claim_patterns = [
            r'\d+%',  # Percentages
            r'\d+(?:\.\d+)?',  # Numbers
            r'according to',  # Citations
            r'research shows',  # Research references
            r'studies indicate'  # Study references
        ]
        
        for sentence in sentences:
            for pattern in claim_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    metrics["factual_consistency"]["claim_count"] += 1
                    break
        
        # Count citations
        citation_patterns = [
            r'\(\d{4}\)',  # Year citations
            r'et al\.',  # Academic citations
            r'according to .+?[,.]',  # Attribution phrases
        ]
        
        for sentence in sentences:
            for pattern in citation_patterns:
                if re.search(pattern, sentence):
                    metrics["factual_consistency"]["citation_count"] += 1
                    break
        
        # Estimate verifiable statements
        metrics["factual_consistency"]["verifiable_statements"] = (
            metrics["factual_consistency"]["claim_count"] +
            metrics["factual_consistency"]["citation_count"]
        )
        
        return metrics
    
    def _optimize_for_voice_search(self, content: str) -> Dict:
        """Optimize content for voice search"""
        sentences = sent_tokenize(content)
        
        metrics = {
            "voice_search": {
                "question_count": 0,
                "conversational_phrases": 0,
                "natural_language_score": 0
            }
        }
        
        # Count questions
        question_patterns = [r'\?', r'what', r'how', r'why', r'when', r'where', r'who']
        metrics["voice_search"]["question_count"] = sum(
            1 for s in sentences
            if any(re.search(f"\\b{p}\\b", s.lower()) for p in question_patterns)
        )
        
        # Count conversational phrases
        conversational_patterns = [
            r'you can',
            r'let\'s',
            r'here\'s',
            r'imagine',
            r'think about'
        ]
        
        metrics["voice_search"]["conversational_phrases"] = sum(
            1 for s in sentences
            if any(re.search(pattern, s.lower()) for pattern in conversational_patterns)
        )
        
        # Calculate natural language score
        avg_sentence_length = sum(len(word_tokenize(s)) for s in sentences) / len(sentences) if sentences else 0
        metrics["voice_search"]["natural_language_score"] = (
            100 - abs(15 - avg_sentence_length) * 3  # Optimal length around 15 words
        )
        
        return metrics
    
    def _optimize_for_platform(self, content: str, platform: str) -> Dict:
        """Apply platform-specific optimizations"""
        metrics = {
            "platform_score": 0,
            "suggestions": []
        }
        
        if platform == "chatgpt":
            # ChatGPT optimization
            metrics.update(self._optimize_for_chatgpt(content))
        elif platform == "claude":
            # Claude optimization
            metrics.update(self._optimize_for_claude(content))
        elif platform == "voice":
            # Voice assistant optimization
            metrics.update(self._optimize_for_voice_search(content))
        
        return metrics
    
    def _optimize_for_chatgpt(self, content: str) -> Dict:
        """Optimize content specifically for ChatGPT"""
        metrics = {
            "chatgpt_metrics": {
                "structure_score": 0,
                "clarity_score": 0,
                "context_score": 0
            }
        }
        
        # Analyze structure
        paragraphs = content.split('\n\n')
        metrics["chatgpt_metrics"]["structure_score"] = min(100, len(paragraphs) * 10)
        
        # Analyze clarity
        sentences = sent_tokenize(content)
        avg_sentence_length = sum(len(word_tokenize(s)) for s in sentences) / len(sentences) if sentences else 0
        metrics["chatgpt_metrics"]["clarity_score"] = 100 - abs(15 - avg_sentence_length) * 3
        
        # Analyze context
        context_patterns = [r'for example', r'specifically', r'in other words', r'to illustrate']
        context_matches = sum(
            1 for pattern in context_patterns
            if re.search(pattern, content, re.IGNORECASE)
        )
        metrics["chatgpt_metrics"]["context_score"] = min(100, context_matches * 20)
        
        return metrics
    
    def _optimize_for_claude(self, content: str) -> Dict:
        """Optimize content specifically for Claude"""
        metrics = {
            "claude_metrics": {
                "reasoning_score": 0,
                "evidence_score": 0,
                "coherence_score": 0
            }
        }
        
        # Analyze reasoning patterns
        reasoning_patterns = [r'therefore', r'because', r'consequently', r'as a result']
        reasoning_matches = sum(
            1 for pattern in reasoning_patterns
            if re.search(pattern, content, re.IGNORECASE)
        )
        metrics["claude_metrics"]["reasoning_score"] = min(100, reasoning_matches * 20)
        
        # Analyze evidence presentation
        evidence_patterns = [r'according to', r'research shows', r'data indicates']
        evidence_matches = sum(
            1 for pattern in evidence_patterns
            if re.search(pattern, content, re.IGNORECASE)
        )
        metrics["claude_metrics"]["evidence_score"] = min(100, evidence_matches * 25)
        
        # Analyze coherence
        paragraphs = content.split('\n\n')
        coherence_score = 100 if len(paragraphs) >= 3 else len(paragraphs) * 33
        metrics["claude_metrics"]["coherence_score"] = coherence_score
        
        return metrics
    
    def _calculate_score(self, metrics: Dict) -> int:
        """Calculate overall GEO score"""
        score = 100
        
        # Context clarity scoring
        if "context_clarity" in metrics:
            clarity = metrics["context_clarity"]
            if clarity["complex_sentence_ratio"] > 0.3:
                score -= 10
            if clarity["transition_density"] < 0.2:
                score -= 10
        
        # Factual consistency scoring
        if "factual_consistency" in metrics:
            factual = metrics["factual_consistency"]
            if factual["citation_count"] == 0:
                score -= 15
            if factual["verifiable_statements"] < 3:
                score -= 10
        
        # Voice search optimization scoring
        if "voice_search" in metrics:
            voice = metrics["voice_search"]
            if voice["natural_language_score"] < 70:
                score -= 10
            if voice["conversational_phrases"] == 0:
                score -= 5
        
        return max(0, min(100, score))
    
    def _generate_suggestions(self, metrics: Dict) -> List[str]:
        """Generate optimization suggestions based on metrics"""
        suggestions = []
        
        # Context clarity suggestions
        if "context_clarity" in metrics:
            clarity = metrics["context_clarity"]
            if clarity["complex_sentence_ratio"] > 0.3:
                suggestions.append("Simplify complex sentences for better AI comprehension")
            if clarity["transition_density"] < 0.2:
                suggestions.append("Add more transition words to improve flow")
        
        # Factual consistency suggestions
        if "factual_consistency" in metrics:
            factual = metrics["factual_consistency"]
            if factual["citation_count"] == 0:
                suggestions.append("Add citations or references to support claims")
            if factual["verifiable_statements"] < 3:
                suggestions.append("Include more verifiable facts or statistics")
        
        # Voice search optimization suggestions
        if "voice_search" in metrics:
            voice = metrics["voice_search"]
            if voice["question_count"] == 0:
                suggestions.append("Add natural questions to optimize for voice search")
            if voice["conversational_phrases"] == 0:
                suggestions.append("Include more conversational phrases")
        
        return suggestions
    
    def _apply_optimizations(
        self,
        content: str,
        suggestions: List[str],
        target_platforms: List[str]
    ) -> str:
        """Apply optimization suggestions to content"""
        # This is a placeholder for actual content optimization
        # In a real implementation, this would use AI to modify the content
        # based on the suggestions and target platforms
        return content 