import sqlite3
from typing import List, Dict
from fastapi import HTTPException, status
from app.database import get_db
from app.models.job_seeker import JobSeekerCreate, JobSeekerUpdate
from datetime import datetime

class JobSeekerService:
    
    @staticmethod
    def create(data: JobSeekerCreate) -> Dict:
        """Create a new job seeker"""
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO freelancers 
                    (name, email, phone, location, profile_picture, work_experience, 
                     skills, job_type, availability)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.name,
                    data.email,
                    data.phone,
                    data.location,
                    data.profile_picture,
                    data.work_experience,
                    data.skills,
                    data.job_type,
                    data.availability
                ))
                job_seeker_id = cursor.lastrowid
                conn.commit()
                
            return {
                'success': True,
                'job_seeker_id': job_seeker_id,
                'message': 'Job seeker created successfully'
            }
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered'
            )
    
    @staticmethod
    def list_all() -> List[Dict]:
        """List all job seekers"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.*,
                       COALESCE(AVG(r.rating), 0) as average_score,
                       COUNT(r.id) as evaluation_count
                FROM freelancers f
                LEFT JOIN ratings r ON f.id = r.freelancer_id
                GROUP BY f.id
                ORDER BY f.created_at DESC
            ''')
            job_seekers = []
            for row in cursor.fetchall():
                job_seeker = dict(row)
                
                avg_score = job_seeker.get('average_score')
                job_seeker['average_score'] = round(float(avg_score), 2) if avg_score is not None else 0.0
                job_seeker['evaluation_count'] = int(job_seeker.get('evaluation_count') or 0)
                job_seekers.append(job_seeker)
        
        return job_seekers
    
    @staticmethod
    def get_by_id(job_seeker_id: int) -> Dict:
        """Get job seeker by ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.*,
                       AVG(r.rating) as average_score,
                       COUNT(r.id) as evaluation_count
                FROM freelancers f
                LEFT JOIN ratings r ON f.id = r.freelancer_id
                WHERE f.id = ?
                GROUP BY f.id
            ''', (job_seeker_id,))
            job_seeker = cursor.fetchone()
            
            if not job_seeker:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            result = dict(job_seeker)
            result['average_score'] = round(result.get('average_score') or 0, 2)
            result['evaluation_count'] = result.get('evaluation_count') or 0
            
        return result
    
    @staticmethod
    def update(job_seeker_id: int, data: JobSeekerUpdate) -> Dict:
        """Update job seeker"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM freelancers WHERE id = ?', (job_seeker_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='No fields to update'
                )
            
            update_fields = []
            values = []
            for field, value in update_data.items():
                update_fields.append(f'{field} = ?')
                values.append(value)
            
            update_fields.append('updated_at = ?')
            values.append(datetime.now().isoformat())
            values.append(job_seeker_id)
            
            query = f"UPDATE freelancers SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        return {
            'success': True,
            'message': 'Job seeker updated successfully'
        }
    
    @staticmethod
    def delete(job_seeker_id: int) -> Dict:
        """Delete job seeker"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM freelancers WHERE id = ?', (job_seeker_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Job seeker not found'
                )
            
            cursor.execute('DELETE FROM ratings WHERE freelancer_id = ?', (job_seeker_id,))
            cursor.execute('DELETE FROM freelancers WHERE id = ?', (job_seeker_id,))
            conn.commit()
        
        return {
            'success': True,
            'message': 'Job seeker deleted successfully'
        }