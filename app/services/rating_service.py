import sqlite3
from typing import Dict, List
from fastapi import HTTPException, status
from app.database import get_db
from app.models.rating import RatingCreate

class RatingService:
    
    @staticmethod
    def create_rating(rating_data: RatingCreate) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Check if freelancer exists
            cursor.execute('SELECT id FROM freelancers WHERE id = ?', (rating_data.freelancer_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            # Check if evaluator exists
            cursor.execute('SELECT id FROM evaluators WHERE id = ?', (rating_data.evaluator_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Evaluator not found'
                )

            # Check if rating already exists (PREVENT DUPLICATES)
            cursor.execute('''
                SELECT id FROM ratings 
                WHERE freelancer_id = ? AND evaluator_id = ?
            ''', (rating_data.freelancer_id, rating_data.evaluator_id))
            
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Cannot rate the same freelancer twice'
                )
                
            # Insert rating (UNIQUE constraint prevents duplicate)
            try:
                cursor.execute('''
                    INSERT INTO ratings (freelancer_id, evaluator_id, rating, review_text)
                    VALUES (?, ?, ?, ?)
                ''', (
                    rating_data.freelancer_id,
                    rating_data.evaluator_id,
                    rating_data.rating,
                    rating_data.review_text
                ))
                
                rating_id = cursor.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='You have already evaluated this job seeker'
                )
        
        return {
            'success': True,
            'rating_id': rating_id,
            'message': 'Evaluation submitted successfully'
        }
    
    @staticmethod
    def get_freelancer_ratings(freelancer_id: int) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM freelancers WHERE id = ?', (freelancer_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            # Get all ratings with evaluator info
            cursor.execute('''
                SELECT r.*, e.name as evaluator_name, e.company as evaluator_company,
                       f.name as job_seeker_name
                FROM ratings r
                JOIN evaluators e ON r.evaluator_id = e.id
                JOIN freelancers f ON r.freelancer_id = f.id
                WHERE r.freelancer_id = ? 
                ORDER BY r.created_at DESC
            ''', (freelancer_id,))
            ratings = [dict(row) for row in cursor.fetchall()]
            
            # Calculate average
            cursor.execute('''
                SELECT AVG(rating) as avg_rating, COUNT(*) as count 
                FROM ratings 
                WHERE freelancer_id = ?
            ''', (freelancer_id,))
            result = cursor.fetchone()
            
            # Add average score to each rating
            avg_score = result['avg_rating'] or 0
            for rating in ratings:
                rating['average_score'] = round(avg_score, 2)
            
            # ✅ FIX: Return both 'count' and 'total_reviews' fields
            rating_info = {
                'average': round(avg_score, 2),
                'count': result['count'],          # Frontend expects this field
                'total_reviews': result['count']    # Backward compatibility
            }
            
            # Get rating distribution
            cursor.execute('''
                SELECT rating, COUNT(*) as count 
                FROM ratings 
                WHERE freelancer_id = ? 
                GROUP BY rating
                ORDER BY rating DESC
            ''', (freelancer_id,))
            rating_distribution = {str(row['rating']): row['count'] for row in cursor.fetchall()}
        
        return {
            'rating_info': rating_info,
            'rating_distribution': rating_distribution,
            'reviews': ratings
        }
    
    @staticmethod
    def get_rating_statistics(freelancer_id: int) -> Dict:
        """Get detailed rating statistics with percentages"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM freelancers WHERE id = ?', (freelancer_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            # Get rating counts
            cursor.execute('''
                SELECT rating, COUNT(*) as count 
                FROM ratings 
                WHERE freelancer_id = ? 
                GROUP BY rating
            ''', (freelancer_id,))
            
            rating_counts = {i: 0 for i in range(1, 6)}
            total = 0
            for row in cursor.fetchall():
                rating_counts[row['rating']] = row['count']
                total += row['count']
            
            # Calculate average
            cursor.execute('''
                SELECT AVG(rating) as avg_rating 
                FROM ratings 
                WHERE freelancer_id = ?
            ''', (freelancer_id,))
            avg_rating = cursor.fetchone()['avg_rating'] or 0
            
            # Calculate percentages
            rating_percentages = {}
            for rating, count in rating_counts.items():
                percentage = (count / total * 100) if total > 0 else 0
                rating_percentages[rating] = {
                    'count': count,
                    'percentage': round(percentage, 1)
                }
        
        return {
            'average': round(avg_rating, 2),
            'total_reviews': total,
            'count': total,  # Add count field
            'rating_breakdown': rating_percentages
        }
    
    @staticmethod
    def get_all_evaluations() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.*, 
                       e.name as evaluator_name, 
                       e.company as evaluator_company,
                       f.name as job_seeker_name,
                       r.rating as score,
                       r.review_text as comment,
                       r.created_at as evaluation_date
                FROM ratings r
                JOIN evaluators e ON r.evaluator_id = e.id
                JOIN freelancers f ON r.freelancer_id = f.id
                ORDER BY r.created_at DESC
            ''')
            evaluations = [dict(row) for row in cursor.fetchall()]
            
            # Calculate average score for each job seeker
            for evaluation in evaluations:
                cursor.execute('''
                    SELECT AVG(rating) as avg_score
                    FROM ratings
                    WHERE freelancer_id = ?
                ''', (evaluation['freelancer_id'],))
                result = cursor.fetchone()
                evaluation['average_score'] = round(result['avg_score'], 2) if result['avg_score'] else 0.0
            
            return evaluations