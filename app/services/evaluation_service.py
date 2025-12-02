import sqlite3
from typing import List, Dict
from fastapi import HTTPException, status
from app.database import get_db
from app.models.evaluation import EvaluationCreate

class EvaluationService:
    
    @staticmethod
    def create(data: EvaluationCreate) -> Dict:
        """Create a new evaluation"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Check if job seeker exists
            cursor.execute('SELECT id FROM freelancers WHERE id = ?', (data.job_seeker_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            # Check if evaluator exists
            cursor.execute('SELECT id FROM evaluators WHERE id = ?', (data.evaluator_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Evaluator not found'
                )
            
            # Insert evaluation (using ratings table)
            try:
                cursor.execute('''
                    INSERT INTO ratings (freelancer_id, evaluator_id, rating, review_text)
                    VALUES (?, ?, ?, ?)
                ''', (
                    data.job_seeker_id,
                    data.evaluator_id,
                    data.score,
                    data.comment
                ))
                
                evaluation_id = cursor.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='You have already evaluated this job seeker'
                )
        
        return {
            'success': True,
            'evaluation_id': evaluation_id,
            'message': 'Evaluation submitted successfully'
        }
    
    @staticmethod
    def get_by_job_seeker(job_seeker_id: int) -> List[Dict]:
        """Get all evaluations for a job seeker"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM freelancers WHERE id = ?', (job_seeker_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            cursor.execute('''
                SELECT r.id,
                       r.freelancer_id as job_seeker_id,
                       r.evaluator_id,
                       r.rating as score,
                       r.review_text as comment,
                       r.created_at as evaluation_date,
                       e.name as evaluator_name,
                       e.company as evaluator_company,
                       f.name as job_seeker_name
                FROM ratings r
                JOIN evaluators e ON r.evaluator_id = e.id
                JOIN freelancers f ON r.freelancer_id = f.id
                WHERE r.freelancer_id = ?
                ORDER BY r.created_at DESC
            ''', (job_seeker_id,))
            
            evaluations = [dict(row) for row in cursor.fetchall()]
            
            # Calculate average score
            if evaluations:
                cursor.execute('''
                    SELECT AVG(rating) as avg_score
                    FROM ratings
                    WHERE freelancer_id = ?
                ''', (job_seeker_id,))
                result = cursor.fetchone()
                avg_score = round(result['avg_score'], 2) if result['avg_score'] else 0.0
                
                for evaluation in evaluations:
                    evaluation['average_score'] = avg_score
        
        return evaluations
    
    @staticmethod
    def get_by_evaluator(evaluator_id: int) -> List[Dict]:
        """Get all evaluations by an evaluator"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM evaluators WHERE id = ?', (evaluator_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Evaluator not found'
                )
            
            cursor.execute('''
                SELECT r.id,
                       r.freelancer_id as job_seeker_id,
                       r.evaluator_id,
                       r.rating as score,
                       r.review_text as comment,
                       r.created_at as evaluation_date,
                       e.name as evaluator_name,
                       e.company as evaluator_company,
                       f.name as job_seeker_name
                FROM ratings r
                JOIN evaluators e ON r.evaluator_id = e.id
                JOIN freelancers f ON r.freelancer_id = f.id
                WHERE r.evaluator_id = ?
                ORDER BY r.created_at DESC
            ''', (evaluator_id,))
            
            evaluations = [dict(row) for row in cursor.fetchall()]
            
            # Add average score for each job seeker
            for evaluation in evaluations:
                cursor.execute('''
                    SELECT AVG(rating) as avg_score
                    FROM ratings
                    WHERE freelancer_id = ?
                ''', (evaluation['job_seeker_id'],))
                result = cursor.fetchone()
                evaluation['average_score'] = round(result['avg_score'], 2) if result['avg_score'] else 0.0
        
        return evaluations
    
    @staticmethod
    def list_all() -> List[Dict]:
        """List all evaluations"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.id,
                       r.freelancer_id as job_seeker_id,
                       r.evaluator_id,
                       r.rating as score,
                       r.review_text as comment,
                       r.created_at as evaluation_date,
                       e.name as evaluator_name,
                       e.company as evaluator_company,
                       f.name as job_seeker_name
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
                ''', (evaluation['job_seeker_id'],))
                result = cursor.fetchone()
                evaluation['average_score'] = round(result['avg_score'], 2) if result['avg_score'] else 0.0
            
            return evaluations