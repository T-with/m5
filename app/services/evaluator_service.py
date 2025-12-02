import sqlite3
from typing import List, Dict, Optional
from fastapi import HTTPException, status
from app.database import get_db
from app.models.evaluator import EvaluatorCreate
import hashlib

class EvaluatorService:
    
    @staticmethod
    def create(data: EvaluatorCreate) -> Dict:
        try:
            # Hash password
            password_hash = hashlib.sha256(data.password.encode()).hexdigest()
            
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO evaluators (name, email, password, company, position)
                    VALUES (?, ?, ?, ?, ?)
                ''', (data.name, data.email, password_hash, data.company, data.position))
                evaluator_id = cursor.lastrowid
                conn.commit()
                
            return {
                'success': True,
                'evaluator_id': evaluator_id,
                'message': 'Evaluator registered successfully'
            }
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered'
            )
    
    @staticmethod
    def list_all() -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.*, COUNT(r.id) as evaluation_count
                FROM evaluators e
                LEFT JOIN ratings r ON e.id = r.evaluator_id
                GROUP BY e.id
                ORDER BY e.created_at DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_by_id(evaluator_id: int) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM evaluators WHERE id = ?', (evaluator_id,))
            evaluator = cursor.fetchone()
            
            if not evaluator:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Evaluator not found'
                )
            
            return dict(evaluator)
    
    @staticmethod
    def verify_password(evaluator_id: int, password: str) -> bool:
        """Verify evaluator's password"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM evaluators WHERE id = ?', (evaluator_id,))
            evaluator = cursor.fetchone()
            
            if not evaluator:
                return False
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            return password_hash == evaluator['password']