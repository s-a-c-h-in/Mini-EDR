import sqlite3
import json
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="edr_database.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.initialize_database()
    
    def initialize_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY,
                        timestamp TEXT,
                        event_type TEXT,
                        event_data TEXT,
                        risk_level TEXT
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY,
                        timestamp TEXT,
                        alert_type TEXT,
                        alert_data TEXT,
                        severity TEXT,
                        status TEXT DEFAULT 'active'
                    )
                ''')
                conn.commit()
                self.logger.info("Database initialized")
        except Exception as e:
            self.logger.error(f"Database init error: {e}")
    
    def store_event(self, event_data):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO events (timestamp, event_type, event_data, risk_level)
                    VALUES (?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    event_data.get('type'),
                    json.dumps(event_data),
                    event_data.get('risk_level', 'low')
                ))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Error storing event: {e}")
    
    def get_recent_events(self, limit=100):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT * FROM events 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error getting events: {e}")
            return []
