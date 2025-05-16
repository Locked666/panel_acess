from flask import Blueprint, request, jsonify,session
from services.dashboard_service import get_dashboard_data



dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')



@dashboard_bp.route('/gastos', methods=['GET'])
def gastos():
    if session.get('userAdminConnect') is None:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    try:
        data = get_dashboard_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'status': 'error - 500', 'message': str(e)}), 500
   