"""
AI Analyzer for Movie Review App
"""
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AIAnalyzer:
    def __init__(self):
        pass
    
    def analyze_sentiment(self, review_text):
        """Analyze sentiment of review text"""
        if not review_text.strip():
            return "Neutral", 0.0
        
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(review_text)
        except Exception:
            translated = review_text
        
        try:
            analysis = TextBlob(translated)
            polarity = analysis.sentiment.polarity
            
            if polarity > 0.2:
                return "Positive", polarity
            elif polarity < -0.2:
                return "Negative", polarity
            else:
                return "Neutral", polarity
        except Exception:
            return "Neutral", 0.0
    
    def suggest_rating_from_review(self, review_content):
        """Suggest rating based on review sentiment"""
        sentiment, polarity = self.analyze_sentiment(review_content)
        suggested_rating = round(5.5 + polarity * 4.5)
        suggested_rating = max(1, min(10, suggested_rating))
        return suggested_rating, sentiment, polarity
    
    def get_recommendations(self, user_ratings, all_movies, top_n=10):
        """Get AI-based movie recommendations"""
        try:
            # Prepare data for recommendations
            movie_list = []
            for movie_id, movie in all_movies.items():
                movie_list.append({
                    "movie_id": movie_id,
                    "title": movie["Series_Title"],
                    "genres": movie["Genre"]
                })
            movies_df = pd.DataFrame(movie_list)
            
            # Get user ratings dataframe
            user_ratings_df = pd.DataFrame(user_ratings)
            
            # TF-IDF vectorization
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
            
            # Find liked movies (rating >= 6)
            liked_movie_indices = []
            for idx, row in user_ratings_df.iterrows():
                if row["rating"] >= 6:
                    movie_idx = movies_df[movies_df["movie_id"] == row["movie_id"]].index
                    if len(movie_idx) > 0:
                        liked_movie_indices.append(movie_idx[0])
            
            if not liked_movie_indices:
                return None, "Rate some movies with 6+ stars to get better recommendations!"
            
            # Create user profile
            user_profile = tfidf_matrix[liked_movie_indices].mean(axis=0).A1
            
            # Calculate similarities
            similarities = cosine_similarity([user_profile], tfidf_matrix).flatten()
            
            # Get recommendations
            recommendations = []
            rated_movie_ids = [rating["movie_id"] for rating in user_ratings]
            
            for idx, sim in enumerate(similarities):
                movie_id = movies_df.iloc[idx]["movie_id"]
                if movie_id not in rated_movie_ids:
                    movie_data = all_movies[movie_id]
                    recommendations.append((
                        sim, 
                        movies_df.iloc[idx]["title"], 
                        movies_df.iloc[idx]["genres"],
                        movie_data.get('IMDB_Rating', 'N/A'),
                        movie_data['Released_Year']
                    ))
            
            recommendations.sort(reverse=True, key=lambda x: x[0])
            return recommendations[:top_n], None
            
        except Exception as e:
            return None, f"Failed to generate recommendations: {str(e)}"