import sqlite3
from typing import List, Dict, Any

DB_PATH = "/app/data/freelancer.db"


def get_connection() -> sqlite3.Connection:
    """
    Open a new SQLite connection to the freelancer DB.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_name(role: str, user_id: int) -> str:
    """
    Look up the display name for a user based on their role and ID.

    role: "job_seeker" -> freelancers table
          "evaluator"  -> evaluators table
    """
    table = "freelancers" if role == "job_seeker" else "evaluators"

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT name FROM {table} WHERE id = ? LIMIT 1;", (user_id,))
        row = cur.fetchone()
        if row is None:
            return ""
        return row["name"]
    finally:
        conn.close()


class MessageRepository:
    @staticmethod
    def get_user_name(role: str, user_id: int) -> str:
        """
        Helper for fetching names within this repository.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()

            if role == "job_seeker":
                cur.execute("SELECT name FROM freelancers WHERE id = ?;", (user_id,))
            else:
                cur.execute("SELECT name FROM evaluators WHERE id = ?;", (user_id,))

            row = cur.fetchone()
            return row["name"] if row else ""
        finally:
            conn.close()

    @staticmethod
    def build_conversation_id(
        sender_role: str,
        sender_id: int,
        receiver_role: str,
        receiver_id: int,
    ) -> str:
        """
        Build a stable conversation_id, independent of who sends first.
        """
        parties = sorted(
            [(sender_role, sender_id), (receiver_role, receiver_id)],
            key=lambda x: (x[0], x[1]),
        )
        (role1, id1), (role2, id2) = parties
        return f"{role1}:{id1}|{role2}:{id2}"

    @staticmethod
    def insert_message(
        conversation_id: str,
        sender_role: str,
        sender_id: int,
        receiver_role: str,
        receiver_id: int,
        content: str,
    ) -> int:
        """
        Insert a message row and return its DB id.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO messages (
                    conversation_id,
                    sender_role,
                    sender_id,
                    receiver_role,
                    receiver_id,
                    content
                )
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    conversation_id,
                    sender_role,
                    sender_id,
                    receiver_role,
                    receiver_id,
                    content,
                ),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

    @staticmethod
    def add_attachment(
        message_id: int,
        file_path: str,
        original_filename: str,
        mime_type: str,
        size_bytes: int,
    ) -> int:
        """
        Insert a file attachment for a given message and return the attachment id.

        file_path should be a server-side path (e.g. /app/data/uploads/uuid.ext).
        The API layer can later turn this into a public URL.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO message_attachments (
                    message_id,
                    file_path,
                    original_filename,
                    mime_type,
                    size_bytes
                )
                VALUES (?, ?, ?, ?, ?);
                """,
                (message_id, file_path, original_filename, mime_type, size_bytes),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_attachments_for_message(message_id: int) -> List[Dict[str, Any]]:
        """
        Return all attachments for a specific message.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    id,
                    message_id,
                    file_path,
                    original_filename,
                    mime_type,
                    size_bytes,
                    created_at
                FROM message_attachments
                WHERE message_id = ?
                ORDER BY id ASC;
                """,
                (message_id,),
            )
            rows = cur.fetchall()

            attachments: List[Dict[str, Any]] = []

            for row in rows:
                created_raw = str(row["created_at"]) if row["created_at"] is not None else ""
                created_at = created_raw.replace(" ", "T") if created_raw else ""

                attachments.append(
                    {
                        "id": row["id"],
                        "message_id": row["message_id"],
                        "file_path": row["file_path"],
                        "original_filename": row["original_filename"],
                        "mime_type": row["mime_type"],
                        "size_bytes": row["size_bytes"],
                        "created_at": created_at,
                    }
                )

            return attachments
        finally:
            conn.close()

    ''' @staticmethod
    def add_attachment(
        message_id: int,
        file_path: str,
        original_filename: str,
        mime_type: str,
        size_bytes: int,
    ) -> int:
        """
        Insert a file attachment for a given message and return the attachment id.

        file_path should be a server-side path (e.g. /app/data/uploads/uuid.ext).
        The API layer can later turn this into a public URL.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO message_attachments (
                    message_id,
                    file_path,
                    original_filename,
                    mime_type,
                    size_bytes
                )
                VALUES (?, ?, ?, ?, ?);
                """,
                (message_id, file_path, original_filename, mime_type, size_bytes),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_attachments_for_message(message_id: int) -> List[Dict[str, Any]]:
        """
        Return all attachments for a specific message.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    id,
                    message_id,
                    file_path,
                    original_filename,
                    mime_type,
                    size_bytes,
                    created_at
                FROM message_attachments
                WHERE message_id = ?
                ORDER BY id ASC;
                """,
                (message_id,),
            )
            rows = cur.fetchall()

            attachments: List[Dict[str, Any]] = []

            for row in rows:
                created_raw = str(row["created_at"]) if row["created_at"] is not None else ""
                created_at = created_raw.replace(" ", "T") if created_raw else ""

                attachments.append(
                    {
                        "id": row["id"],
                        "message_id": row["message_id"],
                        "file_path": row["file_path"],
                        "original_filename": row["original_filename"],
                        "mime_type": row["mime_type"],
                        "size_bytes": row["size_bytes"],
                        "created_at": created_at,
                    }
                )

            return attachments
        finally:
            conn.close()
'''
    
    @staticmethod
    def get_attachment(attachment_id: int) -> dict | None:
        """
        Look up a single attachment row by id.
        Returns a dict with file_path, original_filename, mime_type, size_bytes, created_at
        or None if not found.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    id,
                    message_id,
                    file_path,
                    original_filename,
                    mime_type,
                    size_bytes,
                    created_at
                FROM message_attachments
                WHERE id = ?;
                """,
                (attachment_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None

            created_raw = (
                str(row["created_at"]) if row["created_at"] is not None else ""
            )
            created_at = created_raw.replace(" ", "T") if created_raw else ""

            return {
                "id": row["id"],
                "message_id": row["message_id"],
                "file_path": row["file_path"],
                "original_filename": row["original_filename"],
                "mime_type": row["mime_type"],
                "size_bytes": row["size_bytes"],
                "created_at": created_at,
            }
        finally:
            conn.close()



    @staticmethod
    def list_conversations_for_user(user_role: str, user_id: int) -> List[Dict[str, Any]]:
        """
        Return one row per conversation for this user.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    id,
                    conversation_id,
                    sender_role,
                    sender_id,
                    receiver_role,
                    receiver_id,
                    content,
                    created_at
                FROM messages
                WHERE
                    (sender_role = ? AND sender_id = ?)
                    OR
                    (receiver_role = ? AND receiver_id = ?)
                ORDER BY created_at DESC, id DESC;
                """,
                (user_role, user_id, user_role, user_id),
            )
            rows = cur.fetchall()

            seen_conversations = set()
            summaries: List[Dict[str, Any]] = []

            for row in rows:
                conv_id = row["conversation_id"]
                if conv_id in seen_conversations:
                    continue
                seen_conversations.add(conv_id)

                if row["sender_role"] == user_role and row["sender_id"] == user_id:
                    other_role = row["receiver_role"]
                    other_id = row["receiver_id"]
                else:
                    other_role = row["sender_role"]
                    other_id = row["sender_id"]

                other_name = get_user_name(other_role, other_id)

                created_raw = str(row["created_at"]) if row["created_at"] is not None else ""
                last_message_time = created_raw.replace(" ", "T") if created_raw else ""

                attachments = MessageRepository.get_attachments_for_message(row["id"])
                has_attachments = len(attachments) > 0

                summaries.append(
                    {
                        "conversation_id": conv_id,
                        "other_party_role": other_role,
                        "other_party_id": other_id,
                        "other_party_name": other_name,
                        "last_message": row["content"],
                        "last_message_time": last_message_time,
                        "has_attachments": has_attachments, 
                    }
                )

            return summaries
        finally:
            conn.close()

    @staticmethod
    def get_conversation_messages(conversation_id: str) -> List[Dict[str, Any]]:
        """
        Return all messages in a conversation in chronological order.
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    id,
                    conversation_id,
                    sender_role,
                    sender_id,
                    receiver_role,
                    receiver_id,
                    content,
                    created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at ASC, id ASC;
                """,
                (conversation_id,),
            )

            rows = cur.fetchall()
            messages: List[Dict[str, Any]] = []

            for row in rows:
                sender_role = row["sender_role"]
                sender_id = row["sender_id"]
                receiver_role = row["receiver_role"]
                receiver_id = row["receiver_id"]

                sender_name = MessageRepository.get_user_name(sender_role, sender_id)
                receiver_name = MessageRepository.get_user_name(receiver_role, receiver_id)

                created_raw = str(row["created_at"]) if row["created_at"] is not None else ""
                created_at = created_raw.replace(" ", "T") if created_raw else ""

                attachments = MessageRepository.get_attachments_for_message(row["id"])

                messages.append(
                    {
                        "id": row["id"],
                        "conversation_id": row["conversation_id"],
                        "sender_role": sender_role,
                        "sender_id": sender_id,
                        "sender_name": sender_name,
                        "receiver_role": receiver_role,
                        "receiver_id": receiver_id,
                        "receiver_name": receiver_name,
                        "content": row["content"],
                        "created_at": created_at,
                        "attachments": attachments, 
                    }
                )

            return messages
        finally:
            conn.close()

    @staticmethod
    def search_users(query: str) -> List[Dict[str, Any]]:
        """
        Search freelancers (job seekers) and evaluators by name or email.
        Returns: [{ role, id, name, email }, ...]
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            pattern = f"%{query}%"
            results: List[Dict[str, Any]] = []

            # Job seekers
            cur.execute(
                """
                SELECT id, name, email
                FROM freelancers
                WHERE name LIKE ? OR email LIKE ?
                ORDER BY name ASC
                LIMIT 25;
                """,
                (pattern, pattern),
            )
            for row in cur.fetchall():
                results.append(
                    {
                        "role": "job_seeker",
                        "id": row["id"],
                        "name": row["name"],
                        "email": row["email"],
                    }
                )

            # Evaluators
            cur.execute(
                """
                SELECT id, name, email
                FROM evaluators
                WHERE name LIKE ? OR email LIKE ?
                ORDER BY name ASC
                LIMIT 25;
                """,
                (pattern, pattern),
            )
            for row in cur.fetchall():
                results.append(
                    {
                        "role": "evaluator",
                        "id": row["id"],
                        "name": row["name"],
                        "email": row["email"],
                    }
                )

            return results
        finally:
            conn.close()

