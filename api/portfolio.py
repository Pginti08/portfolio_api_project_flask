from flask import Blueprint, request, jsonify
from utils.resume_parser import parse_resume

portfolio_bp = Blueprint('portfolio', __name__)


@portfolio_bp.route('/generate', methods=['POST'])
def generate_portfolio():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume uploaded."}), 400

    resume_file = request.files['resume']
    data = parse_resume(resume_file)

    # Structure data for portfolio
    portfolio_data = {
        "hero": {"name": data.get("name", ""), "bio": data.get("bio", "")},
        "about": {"about": data.get("bio", "")},
        "skills": data.get("skills", []),
        "experience": data.get("experience", []),
        "education": data.get("education", []),
        "projects": data.get("projects", []),
        "contact": data.get("contact", ""),
    }
    return jsonify(portfolio_data)
