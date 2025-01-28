import google.generativeai as genai
import os
import json
from pathlib import Path
import numpy as np

class GeminiClient:
    def __init__(self, rag_data_path=None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.rag_embeddings = []
        self.rag_data = []  # Stores dicts with 'text' and 'tags'
        
        if rag_data_path:
            self._load_and_embed_rag_data(rag_data_path)

    def _load_and_embed_rag_data(self, data_path):
        """Load JSON tweet samples and generate embeddings"""
        data_dir = Path(data_path)
        for json_file in data_dir.glob("*.json"):
            with open(json_file, 'r') as f:
                try:
                    tweets = json.load(f)
                    for tweet in tweets:
                        if 'text' in tweet:
                            text = tweet['text'].strip()
                            tags = tweet.get('tags', [])
                            
                            # Generate embedding from text content only
                            embedding = genai.embed_content(
                                model='models/embedding-001',
                                content=text,
                                task_type="retrieval_document"
                            )['embedding']
                            
                            self.rag_embeddings.append(embedding)
                            self.rag_data.append({'text': text, 'tags': tags})
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse {json_file}")

    def _get_similar_tweets(self, query, top_k=3):
        """Retrieve top-k similar tweets using cosine similarity"""
        if not self.rag_data:
            return []
            
        query_embed = genai.embed_content(
            model='models/embedding-001',
            content=query,
            task_type="retrieval_query"
        )['embedding']
        
        similarities = []
        for emb in self.rag_embeddings:
            cos_sim = np.dot(query_embed, emb) / (
                np.linalg.norm(query_embed) * np.linalg.norm(emb)
            )
            similarities.append(cos_sim)
            
        sorted_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.rag_data[i] for i in sorted_indices]

    def generate_tweet(self, trend_context=""):
        """Generate tweet and tags using RAG-enhanced prompt"""
        examples = self._get_similar_tweets(trend_context, top_k=3)
        
        prompt = f"""
        Create an engaging Twitter post that aligns with current trends and follows these guidelines:

        **Trend Context**: {trend_context}

        **Examples of Successful Tweets** (learn structure from these):
        {chr(10).join(
            f'- Tweet: "{ex["text"]}"\n  Tags: {", ".join(ex["tags"])}' 
            for ex in examples
        ) if examples else '- No examples available'}

        **Requirements**:
        - Do NOT include hashtags in the tweet text
        - Keep text under 280 characters (tags excluded from count)
        - Use informal but professional tone
        - Add emojis where appropriate
        - Include 3-5 tags after the tweet for indexing
        - Tags should be relevant comma-separated keywords
        - Format: Tweet text followed by \nTags: tag1, tag2, tag3

        Return ONLY in this format:
        [Your engaging tweet text]
        Tags: [comma-separated keywords]
        """
        
        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)

    def _parse_response(self, response_text):
        """Extract tweet text and tags from model response"""
        cleaned = response_text.strip('" \n')
        
        # Split into content and tags parts
        if "\nTags:" in cleaned:
            content, tags_part = cleaned.split("\nTags:", 1)
            tags = [t.strip() for t in tags_part.split(",") if t.strip()]
        else:
            content = cleaned
            tags = []
        
        # Final cleanup and validation
        content = content.strip()
        if len(content) > 280:
            content = content[:277] + "..."
        
        return {
            'text': content,
            'tags': tags[:5]  # Keep max 5 tags
        }