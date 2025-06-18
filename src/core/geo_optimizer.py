from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import spacy
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import re
import numpy as np

@dataclass
class OptimizationResult:
    optimized_content: str
    qa_pairs: List[Dict[str, str]]
    entities: List[Dict[str, str]]
    confidence_score: float
    metadata: Dict[str, any]

class GEOOptimizer:
    """
    Advanced Generative Engine Optimization (GEO) for AI assistant content optimization.
    """
    
    def __init__(self):
        """Initialize the GEO optimizer with required models"""
        # Load spaCy model for NLP tasks
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize sentence transformer for semantic analysis
        self.transformer = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize zero-shot classification pipeline
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
    def optimize_for_ai_assistants(
        self, 
        content: str, 
        target_queries: List[str],
        optimization_level: str = "balanced"
    ) -> OptimizationResult:
        """
        Optimize content for AI assistant inclusion using multiple strategies.
        
        Args:
            content: The input content to optimize
            target_queries: List of target queries to optimize for
            optimization_level: One of ["conservative", "balanced", "aggressive"]
            
        Returns:
            OptimizationResult containing optimized content and metadata
        """
        # Extract key entities and concepts
        entities = self.extract_entities(content)
        
        # Generate Q&A pairs
        qa_pairs = self.generate_qa_pairs(content)
        
        # Enhance semantic structure
        enhanced_content = self._enhance_semantic_structure(content, entities)
        
        # Add natural language patterns
        optimized_content = self._add_nl_patterns(enhanced_content, target_queries)
        
        # Calculate confidence score
        confidence = self._calculate_optimization_confidence(
            original_content=content,
            optimized_content=optimized_content,
            target_queries=target_queries
        )
        
        return OptimizationResult(
            optimized_content=optimized_content,
            qa_pairs=qa_pairs,
            entities=entities,
            confidence_score=confidence,
            metadata={
                "optimization_level": optimization_level,
                "target_queries": target_queries,
                "entity_count": len(entities),
                "qa_pair_count": len(qa_pairs)
            }
        )
    
    def generate_qa_pairs(self, content: str) -> List[Dict[str, str]]:
        """Extract and format Q&A pairs for better AI retrieval."""
        doc = self.nlp(content)
        qa_pairs = []
        
        # Split into meaningful chunks
        chunks = [sent.text for sent in doc.sents]
        
        for chunk in chunks:
            # Generate relevant questions for each chunk
            questions = self._generate_questions(chunk)
            
            for question in questions:
                answer = self.qa_generator(
                    question=question,
                    context=chunk
                )
                
                if answer['score'] > 0.7:  # Confidence threshold
                    qa_pairs.append({
                        "question": question,
                        "answer": answer['answer'],
                        "confidence": answer['score']
                    })
        
        return qa_pairs
    
    def enhance_with_entities(self, content: str) -> Tuple[str, List[Dict]]:
        """Link named entities to knowledge graphs and enhance content."""
        doc = self.nlp(content)
        entities = []
        enhanced_content = content
        
        for ent in doc.ents:
            entity_info = {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            entities.append(entity_info)
            
            # Enhance entity mentions with context
            enhanced_content = self._enhance_entity_mention(
                enhanced_content, 
                entity_info
            )
            
        return enhanced_content, entities
    
    def _enhance_semantic_structure(self, content: str, entities: List[Dict]) -> str:
        """Enhance content's semantic structure for better AI understanding."""
        # Add semantic markers
        enhanced = content
        
        # Add topic sentences
        enhanced = self._add_topic_sentences(enhanced)
        
        # Add entity context
        for entity in entities:
            enhanced = self._add_entity_context(enhanced, entity)
        
        # Add semantic transitions
        enhanced = self._add_semantic_transitions(enhanced)
        
        return enhanced
    
    def _add_nl_patterns(self, content: str, target_queries: List[str]) -> str:
        """Add natural language patterns that align with AI query patterns."""
        enhanced = content
        
        # Add query-aligned phrases
        for query in target_queries:
            relevant_patterns = self._generate_nl_patterns(query)
            enhanced = self._integrate_patterns(enhanced, relevant_patterns)
        
        return enhanced
    
    def _calculate_optimization_confidence(
        self, 
        original_content: str,
        optimized_content: str,
        target_queries: List[str]
    ) -> float:
        """Calculate confidence score for the optimization."""
        # Encode original and optimized content
        original_embedding = self.transformer.encode(original_content)
        optimized_embedding = self.transformer.encode(optimized_content)
        
        # Calculate semantic similarity with target queries
        query_scores = []
        for query in target_queries:
            query_embedding = self.transformer.encode(query)
            original_score = self._cosine_similarity(original_embedding, query_embedding)
            optimized_score = self._cosine_similarity(optimized_embedding, query_embedding)
            improvement = optimized_score - original_score
            query_scores.append(improvement)
        
        # Calculate overall confidence score
        confidence = sum(query_scores) / len(query_scores)
        return max(0.0, min(1.0, confidence + 0.5))  # Normalize to [0,1]
    
    def _generate_questions(self, text: str) -> List[str]:
        """Generate relevant questions from text."""
        doc = self.nlp(text)
        questions = []
        
        # Extract key information
        for sent in doc.sents:
            # Generate different question types based on sentence structure
            if any(token.dep_ == "nsubj" for token in sent):
                questions.append(self._generate_what_question(sent))
            if any(token.dep_ == "pobj" for token in sent):
                questions.append(self._generate_how_question(sent))
                
        return [q for q in questions if q]  # Filter out None values
    
    def _generate_what_question(self, sent) -> Optional[str]:
        """Generate a 'what' question from a sentence."""
        subject = next((token for token in sent if token.dep_ == "nsubj"), None)
        if subject:
            return f"What does {subject.text} do?"
        return None
    
    def _generate_how_question(self, sent) -> Optional[str]:
        """Generate a 'how' question from a sentence."""
        verb = next((token for token in sent if token.pos_ == "VERB"), None)
        if verb:
            return f"How does one {verb.lemma_}?"
        return None
    
    def _cosine_similarity(self, v1, v2) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    def _enhance_entity_mention(self, content: str, entity_info: Dict) -> str:
        """Enhance entity mentions with additional context."""
        # Add brief context after first mention
        first_mention_pos = content.find(entity_info['text'])
        if first_mention_pos != -1:
            context = self._generate_entity_context(entity_info)
            if context:
                insert_pos = first_mention_pos + len(entity_info['text'])
                return (
                    content[:insert_pos] + 
                    f" ({context})" + 
                    content[insert_pos:]
                )
        return content
    
    def _generate_entity_context(self, entity_info: Dict) -> Optional[str]:
        """Generate brief context for an entity based on its type."""
        if entity_info['label'] == 'PERSON':
            return "a key figure in this context"
        elif entity_info['label'] == 'ORG':
            return "an organization"
        elif entity_info['label'] == 'GPE':
            return "a location"
        return None
    
    def _add_topic_sentences(self, content: str) -> str:
        """Add clear topic sentences to improve content structure."""
        paragraphs = content.split('\n\n')
        enhanced_paragraphs = []
        
        for para in paragraphs:
            if len(para.strip()) > 0:
                doc = self.nlp(para)
                # Check if paragraph needs a topic sentence
                if not self._has_topic_sentence(doc):
                    topic = self._generate_topic_sentence(doc)
                    if topic:
                        para = topic + " " + para
                enhanced_paragraphs.append(para)
                
        return '\n\n'.join(enhanced_paragraphs)
    
    def _has_topic_sentence(self, doc) -> bool:
        """Check if the paragraph has a clear topic sentence."""
        first_sent = next(doc.sents)
        return any(token.dep_ == "nsubj" for token in first_sent)
    
    def _generate_topic_sentence(self, doc) -> Optional[str]:
        """Generate a topic sentence based on paragraph content."""
        # Extract key noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        if noun_phrases:
            return f"This section discusses {noun_phrases[0]}."
        return None
    
    def _add_semantic_transitions(self, content: str) -> str:
        """Add semantic transitions between sections."""
        paragraphs = content.split('\n\n')
        enhanced = []
        
        for i, para in enumerate(paragraphs):
            if i > 0 and len(para.strip()) > 0:
                transition = self._generate_transition(
                    paragraphs[i-1], 
                    para
                )
                if transition:
                    enhanced.append(transition)
            enhanced.append(para)
            
        return '\n\n'.join(enhanced)
    
    def _generate_transition(self, prev_para: str, next_para: str) -> Optional[str]:
        """Generate a semantic transition between paragraphs."""
        prev_doc = self.nlp(prev_para)
        next_doc = self.nlp(next_para)
        
        # Extract key topics
        prev_topics = [token.text for token in prev_doc if token.pos_ == "NOUN"]
        next_topics = [token.text for token in next_doc if token.pos_ == "NOUN"]
        
        if prev_topics and next_topics:
            return f"Building on the discussion of {prev_topics[0]}, let's explore {next_topics[0]}."
        return None
    
    def _generate_nl_patterns(self, query: str) -> List[str]:
        """Generate natural language patterns that align with the query."""
        doc = self.nlp(query)
        patterns = []
        
        # Generate different pattern types
        patterns.extend(self._generate_definition_patterns(doc))
        patterns.extend(self._generate_explanation_patterns(doc))
        patterns.extend(self._generate_example_patterns(doc))
        
        return patterns
    
    def _generate_definition_patterns(self, doc) -> List[str]:
        """Generate definition-style patterns."""
        patterns = []
        for token in doc:
            if token.pos_ == "NOUN":
                patterns.append(f"{token.text} refers to")
                patterns.append(f"{token.text} is defined as")
        return patterns
    
    def _generate_explanation_patterns(self, doc) -> List[str]:
        """Generate explanation-style patterns."""
        patterns = []
        for token in doc:
            if token.pos_ == "VERB":
                patterns.append(f"To {token.lemma_},")
                patterns.append(f"When {token.lemma_}ing,")
        return patterns
    
    def _generate_example_patterns(self, doc) -> List[str]:
        """Generate example-style patterns."""
        patterns = []
        for token in doc:
            if token.pos_ == "NOUN":
                patterns.append(f"For example, {token.text}")
                patterns.append(f"To illustrate {token.text},")
        return patterns
    
    def _integrate_patterns(self, content: str, patterns: List[str]) -> str:
        """Integrate natural language patterns into content."""
        paragraphs = content.split('\n\n')
        enhanced = []
        
        for i, para in enumerate(paragraphs):
            if i < len(patterns) and len(para.strip()) > 0:
                enhanced.append(f"{patterns[i]} {para}")
            else:
                enhanced.append(para)
                
        return '\n\n'.join(enhanced)
    
    def optimize_content(
        self,
        content: str,
        target_platforms: List[str],
        optimization_goals: Optional[List[str]] = None
    ) -> Dict:
        """
        Optimize content for AI platforms
        
        Args:
            content: The content to optimize
            target_platforms: List of target platforms (e.g., ['chatgpt', 'claude', 'voice'])
            optimization_goals: List of optimization goals (e.g., ['context', 'factual', 'voice_search'])
            
        Returns:
            Dict containing optimization results and suggestions
        """
        if not content:
            raise ValueError("Content cannot be empty")
        
        if not target_platforms:
            raise ValueError("At least one target platform must be specified")
        
        # Initialize results
        results = {
            "original_content": content,
            "optimized_content": content,
            "metrics": {},
            "suggestions": [],
            "score": 0
        }
        
        # Analyze context clarity
        context_metrics = self._analyze_context_clarity(content)
        results["metrics"]["context_clarity"] = context_metrics
        
        # Analyze factual consistency
        factual_metrics = self._analyze_factual_consistency(content)
        results["metrics"]["factual_consistency"] = factual_metrics
        
        # Platform-specific optimization
        platform_metrics = {}
        for platform in target_platforms:
            platform_metrics[platform] = self._optimize_for_platform(content, platform)
        results["metrics"]["platform_metrics"] = platform_metrics
        
        # Voice search optimization if requested
        if optimization_goals and "voice_search" in optimization_goals:
            voice_metrics = self._optimize_for_voice_search(content)
            results["metrics"]["voice_search"] = voice_metrics
        
        # Calculate overall score
        results["score"] = self._calculate_score(results["metrics"])
        
        # Generate optimization suggestions
        results["suggestions"] = self._generate_suggestions(results["metrics"])
        
        # Apply optimizations
        results["optimized_content"] = self._apply_optimizations(
            content,
            results["suggestions"],
            target_platforms
        )
        
        return results
    
    def _analyze_context_clarity(self, content: str) -> Dict:
        """Analyze content clarity and context"""
        doc = self.nlp(content)
        sentences = list(doc.sents)
        
        # Calculate metrics
        metrics = {
            "sentence_count": len(sentences),
            "avg_sentence_length": np.mean([len(s) for s in sentences]) if sentences else 0,
            "unique_entities": len(set([ent.text for ent in doc.ents])),
            "complex_sentence_ratio": sum(1 for s in sentences if len(s) > 20) / len(sentences) if sentences else 0,
            "transition_density": len(re.findall(r'\b(however|therefore|moreover|furthermore|consequently)\b', content.lower())) / len(sentences) if sentences else 0
        }
        
        return metrics
    
    def _analyze_factual_consistency(self, content: str) -> Dict:
        """Analyze factual consistency and verifiability"""
        doc = self.nlp(content)
        
        # Identify potential factual statements
        factual_statements = []
        for sent in doc.sents:
            if any(token.dep_ in ['nsubj', 'nsubjpass'] for token in sent):
                factual_statements.append(sent.text)
        
        # Analyze statements
        metrics = {
            "citation_count": len(re.findall(r'\[\d+\]|\(\d{4}\)', content)),
            "verifiable_statements": len(factual_statements),
            "statement_confidence": self._calculate_statement_confidence(factual_statements)
        }
        
        return metrics
    
    def _optimize_for_platform(self, content: str, platform: str) -> Dict:
        """Optimize content for specific AI platform"""
        if platform == "chatgpt":
            return self._optimize_for_chatgpt(content)
        elif platform == "claude":
            return self._optimize_for_claude(content)
        elif platform == "voice":
            return self._optimize_for_voice_search(content)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
    
    def _optimize_for_chatgpt(self, content: str) -> Dict:
        """Optimize content for ChatGPT"""
        # Analyze content structure and clarity
        doc = self.nlp(content)
        sentences = list(doc.sents)
        
        metrics = {
            "structure_score": self._calculate_structure_score(sentences),
            "clarity_score": self._calculate_clarity_score(sentences),
            "context_score": self._calculate_context_score(content)
        }
        
        return metrics
    
    def _optimize_for_claude(self, content: str) -> Dict:
        """Optimize content for Claude"""
        # Analyze content for Claude-specific metrics
        doc = self.nlp(content)
        
        metrics = {
            "platform_score": self._calculate_platform_score(doc),
            "suggestions": self._generate_platform_suggestions(doc)
        }
        
        return metrics
    
    def _optimize_for_voice_search(self, content: str) -> Dict:
        """Optimize content for voice search"""
        # Analyze content for voice search optimization
        doc = self.nlp(content)
        
        metrics = {
            "question_count": len(re.findall(r'\?', content)),
            "conversational_phrases": len(re.findall(r'\b(how|what|when|where|why|who)\b', content.lower())),
            "natural_language_score": self._calculate_natural_language_score(doc)
        }
        
        return metrics
    
    def _calculate_statement_confidence(self, statements: List[str]) -> float:
        """Calculate confidence score for factual statements"""
        if not statements:
            return 0.0
        
        # Use zero-shot classification to assess statement confidence
        confidence_scores = []
        for statement in statements:
            result = self.classifier(
                statement,
                candidate_labels=["factual", "opinion", "uncertain"],
                multi_label=False
            )
            confidence_scores.append(result["scores"][0])
        
        return np.mean(confidence_scores) if confidence_scores else 0.0
    
    def _calculate_structure_score(self, sentences: List) -> float:
        """Calculate structure score for content"""
        if not sentences:
            return 0.0
        
        # Calculate various structure metrics
        avg_length = np.mean([len(s) for s in sentences])
        length_variance = np.var([len(s) for s in sentences])
        
        # Normalize scores
        length_score = 1.0 - min(1.0, abs(avg_length - 15) / 15)
        variance_score = 1.0 - min(1.0, length_variance / 100)
        
        return (length_score + variance_score) / 2
    
    def _calculate_clarity_score(self, sentences: List) -> float:
        """Calculate clarity score for content"""
        if not sentences:
            return 0.0
        
        # Calculate clarity metrics
        complex_sentences = sum(1 for s in sentences if len(s) > 20)
        clarity_ratio = 1.0 - (complex_sentences / len(sentences))
        
        return clarity_ratio
    
    def _calculate_context_score(self, content: str) -> float:
        """Calculate context score for content"""
        # Use sentence transformer to analyze semantic coherence
        sentences = [s.text for s in self.nlp(content).sents]
        if not sentences:
            return 0.0
        
        embeddings = self.transformer.encode(sentences)
        similarities = []
        
        for i in range(len(embeddings) - 1):
            similarity = np.dot(embeddings[i], embeddings[i + 1]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i + 1])
            )
            similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_platform_score(self, doc) -> float:
        """Calculate platform-specific optimization score"""
        # Implement platform-specific scoring logic
        return 0.0  # Placeholder
    
    def _calculate_natural_language_score(self, doc) -> float:
        """Calculate natural language score for voice search"""
        # Analyze natural language patterns
        return 0.0  # Placeholder
    
    def _generate_platform_suggestions(self, doc) -> List[str]:
        """Generate platform-specific optimization suggestions"""
        suggestions = []
        # Implement platform-specific suggestion generation
        return suggestions
    
    def _calculate_score(self, metrics: Dict) -> int:
        """Calculate overall optimization score"""
        score = 100
        
        # Context clarity penalties
        if metrics.get("context_clarity", {}).get("complex_sentence_ratio", 0) > 0.3:
            score -= 10
        
        if metrics.get("context_clarity", {}).get("transition_density", 0) < 0.1:
            score -= 5
        
        # Factual consistency penalties
        if metrics.get("factual_consistency", {}).get("citation_count", 0) == 0:
            score -= 10
        
        if metrics.get("factual_consistency", {}).get("statement_confidence", 0) < 0.7:
            score -= 15
        
        # Platform-specific penalties
        platform_metrics = metrics.get("platform_metrics", {})
        for platform, platform_data in platform_metrics.items():
            if platform == "chatgpt":
                if platform_data.get("structure_score", 0) < 0.7:
                    score -= 5
                if platform_data.get("clarity_score", 0) < 0.7:
                    score -= 5
            elif platform == "voice":
                if platform_data.get("natural_language_score", 0) < 0.7:
                    score -= 10
        
        return max(0, min(100, score))
    
    def _generate_suggestions(self, metrics: Dict) -> List[str]:
        """Generate optimization suggestions based on metrics"""
        suggestions = []
        
        # Context clarity suggestions
        if metrics.get("context_clarity", {}).get("complex_sentence_ratio", 0) > 0.3:
            suggestions.append("Simplify complex sentences for better AI comprehension")
        
        if metrics.get("context_clarity", {}).get("transition_density", 0) < 0.1:
            suggestions.append("Add more transition words to improve flow")
        
        # Factual consistency suggestions
        if metrics.get("factual_consistency", {}).get("citation_count", 0) == 0:
            suggestions.append("Add citations or references to support claims")
        
        if metrics.get("factual_consistency", {}).get("statement_confidence", 0) < 0.7:
            suggestions.append("Review and strengthen factual statements")
        
        # Platform-specific suggestions
        platform_metrics = metrics.get("platform_metrics", {})
        for platform, platform_data in platform_metrics.items():
            if platform == "chatgpt":
                if platform_data.get("structure_score", 0) < 0.7:
                    suggestions.append("Improve content structure for better ChatGPT comprehension")
                if platform_data.get("clarity_score", 0) < 0.7:
                    suggestions.append("Enhance content clarity for ChatGPT")
            elif platform == "voice":
                if platform_data.get("natural_language_score", 0) < 0.7:
                    suggestions.append("Make content more conversational for voice search")
        
        return suggestions
    
    def _apply_optimizations(
        self,
        content: str,
        suggestions: List[str],
        target_platforms: List[str]
    ) -> str:
        """Apply optimizations to content based on suggestions"""
        # This is a placeholder for actual content optimization
        # In a real implementation, this would apply the suggestions
        # to modify the content automatically
        return content 