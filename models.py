#!/usr/bin/env python3
"""
Quantum Security System - Database Models
Copyright © 2025 Ervin Remus Radosavlevici
Official Owner: Ervin Remus Radosavlevici
Contact: radosavlevici210@icloud.com
Official Timestamp: 2025-01-20 12:00:00 UTC
Private and Public Repository Rights Reserved
Licensed under MIT License with additional copyright protections
All rights reserved.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app import db

class SecurityLog(db.Model):
    """Model for security event logs"""
    __tablename__ = 'security_logs'

    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)
    event_data = Column(Text)
    result = Column(Text)
    timestamp = Column(DateTime, default=func.now())

    def __repr__(self):
        return f'<SecurityLog {self.id}: {self.event_type}>'

class ThreatDetection(db.Model):
    """Model for threat detections"""
    __tablename__ = 'threat_detections'

    id = Column(Integer, primary_key=True)
    threat_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)  # low, medium, high
    description = Column(Text)
    source_ip = Column(String(45))  # IPv6 compatible
    resolved = Column(Boolean, default=False)
    detected_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime)

    def __repr__(self):
        return f'<ThreatDetection {self.id}: {self.threat_type}>'

# Copyright Protection Notice
# © 2025 Ervin Remus Radosavlevici
# Email: radosavlevici210@icloud.com
# 
# ANTI-THEFT PROTECTION:
# This code is protected against unauthorized use and theft.
# All usage is monitored and logged.
# Report theft to: radosavlevici210@icloud.comm