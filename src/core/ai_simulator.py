from typing import Dict, List, Optional
import openai
from anthropic import Anthropic
from dataclasses import dataclass
import json
import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential

@dataclass
class SimulationResult:
    query: str
    responses: Dict[str, str]
    inclusion_scores: Dict[str, float]
    average_score: float
    metadata: Dict

class AIResponseSimulator:
    """
    Simulate how different AI assistants would respond to queries
    using the optimized content.
    """
    
    def __init__(self, openai_api_key: str, anthropic_api_key: str):
        """Initialize API clients with proper authentication."""
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.anthropic_client = Anthropic(api_key=anthropic_api_key)
        
        # Define system prompts for each AI assistant
        self.system_prompts = {
            "gpt-4": "You are a helpful AI assistant. Use the provided context to answer questions accurately.",
            "claude-3": "You are Claude, an AI assistant. Please answer based on the given context.",
            "gemini": "You are an AI assistant focused on precise and helpful responses."
        }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def simulate_chatgpt_response(
        self, 
        query: str, 
        content: str,
        model: str = "gpt-4"
    ) -> Dict[str, any]:
        """Simulate ChatGPT's response to a query given the content."""
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.system_prompts["gpt-4"]},
                    {"role": "user", "content": f"Context: {content}\n\nQuery: {query}"}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return {
                "response": response.choices[0].message.content,
                "finish_reason": response.choices[0].finish_reason,
                "model": model
            }
            
        except Exception as e:
            print(f"Error simulating ChatGPT response: {str(e)}")
            return {
                "error": str(e),
                "model": model
            }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def simulate_claude_response(
        self, 
        query: str, 
        content: str,
        model: str = "claude-3-opus-20240229"
    ) -> Dict[str, any]:
        """Simulate Claude's response to a query given the content."""
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": f"Context: {content}\n\nQuery: {query}"
                }],
                system=self.system_prompts["claude-3"]
            )
            
            return {
                "response": response.content[0].text,
                "model": model
            }
            
        except Exception as e:
            print(f"Error simulating Claude response: {str(e)}")
            return {
                "error": str(e),
                "model": model
            }
    
    async def evaluate_content_inclusion_probability(
        self, 
        content: str, 
        queries: List[str]
    ) -> SimulationResult:
        """
        Evaluate how likely the content is to be included in AI responses
        for the given queries.
        """
        results = []
        
        for query in queries:
            # Simulate responses from different AI assistants
            chatgpt_response = await self.simulate_chatgpt_response(query, content)
            claude_response = await self.simulate_claude_response(query, content)
            
            # Calculate inclusion scores
            scores = {
                "gpt-4": self._calculate_inclusion_score(content, chatgpt_response.get("response", "")),
                "claude-3": self._calculate_inclusion_score(content, claude_response.get("response", ""))
            }
            
            results.append({
                "query": query,
                "responses": {
                    "gpt-4": chatgpt_response.get("response", ""),
                    "claude-3": claude_response.get("response", "")
                },
                "scores": scores
            })
        
        # Calculate average scores across all queries
        avg_scores = {
            model: np.mean([r["scores"][model] for r in results])
            for model in ["gpt-4", "claude-3"]
        }
        
        return SimulationResult(
            query=queries[0] if len(queries) == 1 else "multiple_queries",
            responses={
                "gpt-4": results[0]["responses"]["gpt-4"],
                "claude-3": results[0]["responses"]["claude-3"]
            },
            inclusion_scores=avg_scores,
            average_score=np.mean(list(avg_scores.values())),
            metadata={
                "num_queries": len(queries),
                "content_length": len(content),
                "simulation_timestamp": self._get_timestamp()
            }
        )
    
    def _calculate_inclusion_score(self, original_content: str, ai_response: str) -> float:
        """
        Calculate how much of the original content is reflected in the AI response.
        Uses a combination of exact phrase matching and semantic similarity.
        """
        if not ai_response:
            return 0.0
            
        # Normalize texts
        original = original_content.lower()
        response = ai_response.lower()
        
        # Calculate exact phrase matches
        phrases = self._extract_key_phrases(original)
        phrase_matches = sum(1 for phrase in phrases if phrase in response)
        phrase_score = phrase_matches / len(phrases) if phrases else 0
        
        # Calculate semantic similarity (simplified version)
        semantic_score = self._calculate_semantic_similarity(original, response)
        
        # Combine scores (weighted average)
        return 0.4 * phrase_score + 0.6 * semantic_score
    
    def _extract_key_phrases(self, text: str, min_length: int = 3) -> List[str]:
        """Extract meaningful phrases from text."""
        words = text.split()
        phrases = []
        
        for i in range(len(words)):
            for j in range(i + min_length, min(i + 8, len(words) + 1)):
                phrase = " ".join(words[i:j])
                if self._is_meaningful_phrase(phrase):
                    phrases.append(phrase)
                    
        return phrases
    
    def _is_meaningful_phrase(self, phrase: str) -> bool:
        """Check if a phrase is meaningful (contains key parts of speech)."""
        # This is a simplified check - could be enhanced with NLP
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to"}
        words = phrase.split()
        
        # Check if phrase has non-stop words
        return any(word not in stop_words for word in words)
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.
        This is a simplified version - could be enhanced with embeddings.
        """
        # Convert to sets of words for comparison
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() 