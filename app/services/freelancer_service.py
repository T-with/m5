import sqlite3
import hashlib
from typing import List, Dict, Optional
from fastapi import HTTPException, status
from app.database import get_db
from app.models.freelancer import FreelancerCreate, FreelancerUpdate

class FreelancerService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create_freelancer(data: FreelancerCreate) -> Dict:
        """Create a new freelancer with password"""
        try:
            # Hash password
            password_hash = FreelancerService.hash_password(data.password)
            
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO freelancers (
                        name, email, password, phone, location, 
                        profile_picture, about_me, work_experience, 
                        skills, job_type, availability
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.name, data.email, password_hash, data.phone, data.location,
                    data.profile_picture, data.about_me, data.work_experience,
                    data.skills, data.job_type, data.availability or 'available'
                ))
                freelancer_id = cursor.lastrowid
                conn.commit()
                
            return {
                'success': True,
                'freelancer_id': freelancer_id,
                'message': 'Freelancer registered successfully'
            }
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered'
            )
    
    @staticmethod
    def verify_password(email: str, password: str) -> Optional[Dict]:
        """Verify freelancer password and return freelancer data"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, name, email, password FROM freelancers WHERE email = ?',
                (email,)
            )
            freelancer = cursor.fetchone()
            
            if not freelancer:
                return None
            
            password_hash = FreelancerService.hash_password(password)
            if password_hash != freelancer['password']:
                return None
            
            return {
                'success': True,
                'freelancer_id': freelancer['id'],
                'name': freelancer['name'],
                'email': freelancer['email']
            }
    
    @staticmethod
    def list_freelancers() -> List[Dict]:
        """List all freelancers"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    f.*,
                    COUNT(DISTINCT r.id) as rating_count,
                    COALESCE(AVG(r.rating), 0) as average_rating
                FROM freelancers f
                LEFT JOIN ratings r ON f.id = r.freelancer_id
                GROUP BY f.id
                ORDER BY f.created_at DESC
            ''')
            
            freelancers = []
            for row in cursor.fetchall():
                freelancer = dict(row)
                # Create rating_info dict expected by the model
                freelancer['rating_info'] = {
                    # New names (used by admin page)
                    'average': float(freelancer.get('average_rating', 0) or 0),
                    'total_reviews': int(freelancer.get('rating_count', 0) or 0),
                    # Old names (backwards compatibility)
                    'average_rating': float(freelancer.get('average_rating', 0) or 0),
                    'total_ratings': int(freelancer.get('rating_count', 0) or 0)
                }
                # Keep for backwards compatibility
                freelancer['average_score'] = float(freelancer.get('average_rating', 0) or 0)
                freelancer['evaluation_count'] = int(freelancer.get('rating_count', 0) or 0)
                freelancers.append(freelancer)
            
            return freelancers
    
    @staticmethod
    def get_freelancer(freelancer_id: int, include_reviews: bool = False) -> Dict:
        """Get freelancer by ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    f.*,
                    COUNT(DISTINCT r.id) as rating_count,
                    COALESCE(AVG(r.rating), 0) as average_rating
                FROM freelancers f
                LEFT JOIN ratings r ON f.id = r.freelancer_id
                WHERE f.id = ?
                GROUP BY f.id
            ''', (freelancer_id,))
            
            freelancer = cursor.fetchone()
            if not freelancer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Freelancer not found'
                )
            
            result = dict(freelancer)
            
            # Add rating_info for compatibility with response models that expect it
            result['rating_info'] = {
                'average_rating': float(result.get('average_rating', 0) or 0),
                'total_ratings': int(result.get('rating_count', 0) or 0)
            }
            
            # Include reviews if requested
            if include_reviews:
                cursor.execute('''
                    SELECT * FROM ratings 
                    WHERE freelancer_id = ? 
                    ORDER BY created_at DESC 
                    LIMIT 5
                ''', (freelancer_id,))
                result['recent_reviews'] = [dict(row) for row in cursor.fetchall()]
            
            return result
    
    @staticmethod
    def update_freelancer(freelancer_id: int, data: FreelancerUpdate) -> Dict:
        """Update freelancer information"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Build update query dynamically
            update_fields = []
            values = []
            
            update_data = data.dict(exclude_unset=True)
            
            # Handle password separately if provided
            if 'password' in update_data and update_data['password']:
                update_data['password'] = FreelancerService.hash_password(update_data['password'])
            
            for key, value in update_data.items():
                if value is not None:
                    update_fields.append(f'{key} = ?')
                    values.append(value)
            
            if not update_fields:
                return {'success': True, 'message': 'No changes to update'}
            
            update_fields.append('updated_at = CURRENT_TIMESTAMP')
            values.append(freelancer_id)
            
            query = f"UPDATE freelancers SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            return {
                'success': True,
                'message': 'Freelancer updated successfully'
            }
    
    @staticmethod
    def delete_freelancer(freelancer_id: int) -> Dict:
        """Delete freelancer"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM freelancers WHERE id = ?', (freelancer_id,))
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Freelancer not found'
                )
            
            conn.commit()
            return {
                'success': True,
                'message': 'Freelancer deleted successfully'
            }