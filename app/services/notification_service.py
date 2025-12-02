import sqlite3
from typing import List, Dict
from datetime import datetime
from app.database import get_db

class NotificationService:
    
    @staticmethod
    def create_notification(
        user_role: str,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        related_id: int = None,
        related_type: str = None
    ) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO notifications (
                    user_role, user_id, type, title, message, related_id, related_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_role, user_id, notification_type, title, message, related_id, related_type))
            
            notification_id = cursor.lastrowid
            conn.commit()
            
            return {
                'success': True,
                'notification_id': notification_id
            }
    
    @staticmethod
    def get_user_notifications(user_role: str, user_id: int, unread_only: bool = False) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT * FROM notifications 
                WHERE user_role = ? AND user_id = ?
            '''
            params = [user_role, user_id]
            
            if unread_only:
                query += ' AND is_read = FALSE'
            
            query += ' ORDER BY created_at DESC'
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def mark_notification_read(notification_id: int, user_id: int) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE notifications 
                SET is_read = TRUE 
                WHERE id = ? AND user_id = ?
            ''', (notification_id, user_id))
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'Notification marked as read'
            }
    
    @staticmethod
    def mark_all_notifications_read(user_role: str, user_id: int) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE notifications 
                SET is_read = TRUE 
                WHERE user_role = ? AND user_id = ?
            ''', (user_role, user_id))
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'All notifications marked as read'
            }
    
    @staticmethod
    def get_unread_count(user_role: str, user_id: int) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) as count 
                FROM notifications 
                WHERE user_role = ? AND user_id = ? AND is_read = FALSE
            ''', (user_role, user_id))
            
            result = cursor.fetchone()
            return result['count'] if result else 0
    
    @staticmethod
    def delete_notification(notification_id: int, user_id: int) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM notifications 
                WHERE id = ? AND user_id = ?
            ''', (notification_id, user_id))
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'Notification deleted'
            }