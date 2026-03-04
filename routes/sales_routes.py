from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.sales_service import create_sale_service

sales_bp = Blueprint("sales", __name__)


@sales_bp.route("/sales", methods=["POST"])
@jwt_required()
def create_sale():

    current_user = get_jwt_identity()
    data = request.get_json()

    response, status = create_sale_service(data, current_user)
    return jsonify(response), status