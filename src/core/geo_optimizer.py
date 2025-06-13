from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import spacy
from sentence_transformers import SentenceTransformer
from transformers import pipeline

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
        # Initialize NLP models
        self.nlp = spacy.load("en_core_web_sm")
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_generator = pipeline("question-answering")
        
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
        original_embedding = self.sentence_transformer.encode(original_content)
        optimized_embedding = self.sentence_transformer.encode(optimized_content)
        
        # Calculate semantic similarity with target queries
        query_scores = []
        for query in target_queries:
            query_embedding = self.sentence_transformer.encode(query)
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
        import numpy as np
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