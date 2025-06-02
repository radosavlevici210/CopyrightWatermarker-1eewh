#!/usr/bin/env python3
"""
Quantum Security System - Routes and API Endpoints
Copyright © 2025 Ervin Remus Radosavlevici
Official Owner: Ervin Remus Radosavlevici
Contact: radosavlevici210@icloud.com
Official Timestamp: 2025-01-20 12:00:00 UTC
Private and Public Repository Rights Reserved
Licensed under MIT License with additional copyright protections
All rights reserved.
"""

from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import SecurityLog, ThreatDetection
from quantum_security import (
    quantum_encryption, neural_defense, quantum_firewall, 
    quantum_teleportation
)
import json
import time
from datetime import datetime, timedelta

@app.route('/')
def index():
    """Main dashboard page"""
    # Get recent security events
    recent_logs = SecurityLog.query.order_by(SecurityLog.timestamp.desc()).limit(10).all()
    recent_threats = ThreatDetection.query.filter_by(resolved=False).order_by(ThreatDetection.detected_at.desc()).limit(5).all()

    # Get statistics
    total_events = SecurityLog.query.count()
    total_threats = ThreatDetection.query.count()
    unresolved_threats = ThreatDetection.query.filter_by(resolved=False).count()

    # Get events by type for chart
    event_types = db.session.query(
        SecurityLog.event_type,
        db.func.count(SecurityLog.id).label('count')
    ).group_by(SecurityLog.event_type).all()

    return render_template('index.html',
                         recent_logs=recent_logs,
                         recent_threats=recent_threats,
                         total_events=total_events,
                         total_threats=total_threats,
                         unresolved_threats=unresolved_threats,
                         event_types=event_types)

@app.route('/encryption')
def encryption():
    """Encryption management page"""
    return render_template('encryption.html')

@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    """API endpoint for encryption"""
    try:
        data = request.get_json()
        text_data = data.get('data', '')

        if not text_data:
            return jsonify({'error': 'No data provided for encryption'}), 400

        encrypted_result = quantum_encryption.encrypt_data(text_data)

        return jsonify({
            'success': True,
            'encrypted_data': encrypted_result,
            'watermark': quantum_encryption.get_watermark()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """API endpoint for decryption"""
    try:
        data = request.get_json()
        encrypted_data = data.get('encrypted_data', {})

        if not encrypted_data:
            return jsonify({'error': 'No encrypted data provided'}), 400

        decrypted_result = quantum_encryption.decrypt_data(encrypted_data)

        return jsonify({
            'success': True,
            'decrypted_data': decrypted_result,
            'watermark': quantum_encryption.get_watermark()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/neural-defense')
def neural_defense_page():
    """Neural defense management page"""
    return render_template('neural_defense.html')

@app.route('/api/neural-defense', methods=['POST'])
def api_neural_defense():
    """API endpoint for neural defense analysis"""
    try:
        data = request.get_json()
        neural_data = data.get('neural_data', [])

        if not neural_data:
            return jsonify({'error': 'No neural data provided for analysis'}), 400

        # Convert to list of floats if needed
        if isinstance(neural_data, str):
            try:
                neural_data = [float(x.strip()) for x in neural_data.split(',')]
            except ValueError:
                return jsonify({'error': 'Invalid neural data format'}), 400

        analysis_result = neural_defense.detect_anomaly(neural_data)

        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'watermark': neural_defense.get_watermark()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/firewall')
def firewall_page():
    """Firewall management page"""
    return render_template('firewall.html')

@app.route('/api/firewall-check', methods=['POST'])
def api_firewall_check():
    """API endpoint for firewall packet checking"""
    try:
        data = request.get_json()
        packet_data = {
            'ip': data.get('ip', request.remote_addr),
            'data': data.get('data', ''),
            'user_agent': data.get('user_agent', request.headers.get('User-Agent', ''))
        }

        firewall_result = quantum_firewall.check_packet(packet_data)

        return jsonify({
            'success': True,
            'firewall_result': firewall_result,
            'watermark': quantum_firewall.get_watermark()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/monitoring')
def monitoring():
    """Security monitoring page"""
    # Get recent logs and threats
    recent_logs = SecurityLog.query.order_by(SecurityLog.timestamp.desc()).limit(20).all()
    recent_threats = ThreatDetection.query.order_by(ThreatDetection.detected_at.desc()).limit(10).all()

    return render_template('monitoring.html',
                         recent_logs=recent_logs,
                         recent_threats=recent_threats)

@app.route('/api/quantum-teleport', methods=['POST'])
def api_quantum_teleport():
    """API endpoint for quantum teleportation"""
    try:
        data = request.get_json()
        quantum_data = data.get('quantum_data', '')

        if not quantum_data:
            return jsonify({'error': 'No quantum data provided for teleportation'}), 400

        teleport_result = quantum_teleportation.teleport_quantum_state(quantum_data)

        return jsonify({
            'success': True,
            'teleportation': teleport_result,
            'watermark': quantum_teleportation.get_watermark()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def api_logs():
    """API endpoint to get security logs"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        logs = SecurityLog.query.order_by(SecurityLog.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'logs': [{
                'id': log.id,
                'event_type': log.event_type,
                'event_data': log.event_data,
                'result': log.result,
                'timestamp': log.timestamp.isoformat()
            } for log in logs.items],
            'total': logs.total,
            'pages': logs.pages,
            'current_page': logs.page
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/threats')
def api_threats():
    """API endpoint to get threat detections"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        threats = ThreatDetection.query.order_by(ThreatDetection.detected_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'threats': [{
                'id': threat.id,
                'threat_type': threat.threat_type,
                'severity': threat.severity,
                'description': threat.description,
                'source_ip': threat.source_ip,
                'resolved': threat.resolved,
                'detected_at': threat.detected_at.isoformat(),
                'resolved_at': threat.resolved_at.isoformat() if threat.resolved_at else None
            } for threat in threats.items],
            'total': threats.total,
            'pages': threats.pages,
            'current_page': threats.page
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/threats/<int:threat_id>/resolve', methods=['POST'])
def api_resolve_threat(threat_id):
    """API endpoint to resolve a threat"""
    try:
        threat = ThreatDetection.query.get_or_404(threat_id)
        threat.resolved = True
        threat.resolved_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Threat {threat_id} resolved successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    try:
        # Get basic stats
        total_events = SecurityLog.query.count()
        total_threats = ThreatDetection.query.count()
        unresolved_threats = ThreatDetection.query.filter_by(resolved=False).count()

        # Get events by type
        event_types = db.session.query(
            SecurityLog.event_type,
            db.func.count(SecurityLog.id).label('count')
        ).group_by(SecurityLog.event_type).all()

        # Get threats by severity
        threat_severities = db.session.query(
            ThreatDetection.severity,
            db.func.count(ThreatDetection.id).label('count')
        ).group_by(ThreatDetection.severity).all()

        return jsonify({
            'total_events': total_events,
            'total_threats': total_threats,
            'unresolved_threats': unresolved_threats,
            'event_types': dict(event_types),
            'threat_severities': dict(threat_severities)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Copyright Protection Notice
# © 2025 Ervin Remus Radosavlevici
# Email: radosavlevici210@icloud.com
# 
# ANTI-THEFT PROTECTION:
# This code is protected against unauthorized use and theft.
# All usage is monitored and logged.
# Report theft to: radosavlevici210@icloud.com