import sqlite3
import json
from typing import List, Dict, Optional
from datetime import datetime
from fastapi import HTTPException, status
from app.database import get_db

class BookingRequestService:
    
    @staticmethod
    def create_booking_request(
        listing_id: int, 
        client_role: str, 
        client_id: int, 
        request_data: dict
    ) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get listing and freelancer info
            cursor.execute("""
                SELECT l.*, f.name as freelancer_name 
                FROM listings l
                JOIN freelancers f ON l.freelancer_id = f.id 
                WHERE l.id = ?
            """, (listing_id,))
            listing = cursor.fetchone()
            
            if not listing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Listing not found'
                )
            
            # Get client info
            if client_role == 'job_seeker':
                cursor.execute('SELECT name FROM freelancers WHERE id = ?', (client_id,))
            else:
                cursor.execute('SELECT name FROM evaluators WHERE id = ?', (client_id,))
            
            client = cursor.fetchone()
            if not client:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Client not found'
                )
            
            # Calculate freelancer's price (base + selected addons)
            freelancer_price = float(listing['base_price'])
            selected_addons = request_data.get('selected_addons', [])
            
            for addon in selected_addons:
                freelancer_price += float(addon['price'])
            
            # Calculate price difference percentage
            price_difference_percent = None
            if request_data.get('client_budget'):
                client_budget = float(request_data['client_budget'])
                price_difference_percent = ((client_budget - freelancer_price) / freelancer_price) * 100
            
            # Insert booking request
            cursor.execute("""
                INSERT INTO booking_requests (
                    listing_id, freelancer_id, client_role, client_id, client_name,
                    requested_date, requested_time, location, description, 
                    selected_addons, client_budget, freelancer_price, price_difference_percent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                listing_id,
                listing['freelancer_id'],
                client_role,
                client_id,
                client['name'],
                request_data['requested_date'],
                request_data.get('requested_time'),
                request_data['location'],
                request_data.get('description'),
                json.dumps(selected_addons),
                request_data.get('client_budget'),
                freelancer_price,
                price_difference_percent
            ))
            
            booking_id = cursor.lastrowid
            conn.commit()
            
            # Create notification for freelancer
            from app.services.notification_service import NotificationService
            NotificationService.create_notification(
                user_role='job_seeker',
                user_id=listing['freelancer_id'],
                notification_type='booking_request',
                title='New Booking Request',
                message=f'New booking request from {client["name"]} for {listing["title"]}',
                related_id=booking_id,
                related_type='booking_request'
            )
            
            return {
                'success': True,
                'booking_id': booking_id,
                'message': 'Booking request sent successfully'
            }
    
    @staticmethod
    def get_freelancer_bookings(freelancer_id: int) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    br.*,
                    l.title as listing_title,
                    CASE 
                        WHEN br.client_role = 'job_seeker' THEN f.name
                        WHEN br.client_role = 'evaluator' THEN e.name
                    END as client_name
                FROM booking_requests br
                JOIN listings l ON br.listing_id = l.id
                LEFT JOIN freelancers f ON br.client_role = 'job_seeker' AND br.client_id = f.id
                LEFT JOIN evaluators e ON br.client_role = 'evaluator' AND br.client_id = e.id
                WHERE br.freelancer_id = ?
                ORDER BY br.created_at DESC
            """, (freelancer_id,))
            
            bookings = []
            for row in cursor.fetchall():
                booking = dict(row)
                booking['selected_addons'] = json.loads(booking['selected_addons'])
                bookings.append(booking)
            
            return bookings
    
    @staticmethod
    def get_client_bookings(client_role: str, client_id: int) -> List[Dict]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    br.*,
                    l.title as listing_title,
                    f.name as freelancer_name
                FROM booking_requests br
                JOIN listings l ON br.listing_id = l.id
                JOIN freelancers f ON br.freelancer_id = f.id
                WHERE br.client_role = ? AND br.client_id = ?
                ORDER BY br.created_at DESC
            """, (client_role, client_id))
            
            bookings = []
            for row in cursor.fetchall():
                booking = dict(row)
                booking['selected_addons'] = json.loads(booking['selected_addons'])
                bookings.append(booking)
            
            return bookings
    
    @staticmethod
    def update_booking_status(
        booking_id: int, 
        freelancer_id: int, 
        update_data: dict
    ) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get booking info
            cursor.execute("""
                SELECT br.*, l.title as listing_title
                FROM booking_requests br
                JOIN listings l ON br.listing_id = l.id
                WHERE br.id = ? AND br.freelancer_id = ?
            """, (booking_id, freelancer_id))
            
            booking = cursor.fetchone()
            if not booking:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Booking request not found or not authorized'
                )
            
            # Update booking
            update_fields = []
            values = []
            
            if 'status' in update_data:
                update_fields.append('status = ?')
                values.append(update_data['status'])
            
            if 'freelancer_price' in update_data:
                update_fields.append('freelancer_price = ?')
                values.append(update_data['freelancer_price'])
                
                # Recalculate price difference
                if booking['client_budget']:
                    new_difference = ((float(booking['client_budget']) - float(update_data['freelancer_price'])) 
                                    / float(update_data['freelancer_price'])) * 100
                    update_fields.append('price_difference_percent = ?')
                    values.append(new_difference)
            
            update_fields.append('updated_at = ?')
            values.append(datetime.now().isoformat())
            values.append(booking_id)
            
            query = f"UPDATE booking_requests SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            # Create notification for client
            if 'status' in update_data:
                from app.services.notification_service import NotificationService
                
                notification_types = {
                    'accepted': 'booking_accepted',
                    'declined': 'booking_declined',
                    'in_progress': 'booking_accepted',
                    'completed': 'booking_completed'
                }
                
                notification_messages = {
                    'accepted': f'Your booking request for "{booking["listing_title"]}" has been accepted!',
                    'declined': f'Your booking request for "{booking["listing_title"]}" has been declined.',
                    'in_progress': f'Your booking for "{booking["listing_title"]}" is now in progress.',
                    'completed': f'Your booking for "{booking["listing_title"]}" has been completed.'
                }
                
                if update_data['status'] in notification_types:
                    NotificationService.create_notification(
                        user_role=booking['client_role'],
                        user_id=booking['client_id'],
                        notification_type=notification_types[update_data['status']],
                        title='Booking Status Update',
                        message=notification_messages[update_data['status']],
                        related_id=booking_id,
                        related_type='booking_request'
                    )
            
            return {
                'success': True,
                'message': 'Booking request updated successfully'
            }
    
    @staticmethod
    def get_booking_by_id(booking_id: int) -> Dict:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT br.*, l.title as listing_title
                FROM booking_requests br
                JOIN listings l ON br.listing_id = l.id
                WHERE br.id = ?
            """, (booking_id,))
            
            booking = cursor.fetchone()
            if not booking:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Booking request not found'
                )
            
            result = dict(booking)
            result['selected_addons'] = json.loads(result['selected_addons'])
            return result