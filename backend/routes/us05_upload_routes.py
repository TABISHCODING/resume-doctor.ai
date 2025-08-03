from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, User, Resume
from services.file_parser import FileParser
from services.keyword_parser import KeywordParser
import os
import uuid
from datetime import datetime

# Create blueprint for upload routes
upload_bp = Blueprint('upload', __name__, url_prefix='/api')

# Initialize keyword parser
keyword_parser = KeywordParser()

@upload_bp.route('/upload_resume', methods=['POST'])
@jwt_required()
def upload_resume():
    """
    Upload and parse resume file
    Expected: multipart/form-data with 'resume' file and optional 'title'
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No resume file provided'
            }), 400
        
        file = request.files['resume']
        title = request.form.get('title', '').strip()
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Validate file type
        is_valid, file_type, error = FileParser.validate_file_type(file.filename)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Create file path
        upload_folder = current_app.config['RESUME_UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Save file
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Create resume record
        resume = Resume(
            user_id=current_user_id,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            title=title or original_filename
        )
        
        db.session.add(resume)
        db.session.commit()
        
        # Parse file in background (for now, we'll do it synchronously)
        success, extracted_text, parse_error = FileParser.parse_resume_file(file_path, file_type)
        
        if success:
            resume.extracted_text = extracted_text
            resume.upload_status = 'completed'

            # US-05: Automatically extract keywords after successful text extraction
            try:
                keywords = keyword_parser.extract_keywords(extracted_text)
                resume.set_keywords(
                    technical_skills=keywords['technical_skills'],
                    soft_skills=keywords['soft_skills'],
                    other_keywords=keywords['other_keywords']
                )
                current_app.logger.info(f"Keywords automatically extracted for resume {resume.id}")
            except Exception as keyword_error:
                current_app.logger.error(f"Failed to extract keywords for resume {resume.id}: {keyword_error}")
                # Don't fail the upload if keyword extraction fails

        else:
            resume.upload_status = 'failed'
            resume.error_message = parse_error

        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded and processed successfully' if success else 'Resume uploaded but parsing failed',
            'resume': resume.to_dict(include_keywords=True),
            'parsing_success': success,
            'parsing_error': parse_error if not success else None,
            'keywords_extracted': resume.keywords_extracted if success else False
        }), 201
        
    except Exception as e:
        db.session.rollback()
        
        # Clean up file if it was saved
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        
        return jsonify({
            'success': False,
            'message': 'Upload failed. Please try again.',
            'error': str(e)
        }), 500

@upload_bp.route('/resumes', methods=['GET'])
@jwt_required()
def get_user_resumes():
    """Get all resumes for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        resumes = Resume.query.filter_by(
            user_id=current_user_id,
            is_active=True
        ).order_by(Resume.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'resumes': [resume.to_dict() for resume in resumes],
            'count': len(resumes)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error fetching resumes',
            'error': str(e)
        }), 500

@upload_bp.route('/resumes/<int:resume_id>', methods=['GET'])
@jwt_required()
def get_resume_details(resume_id):
    """Get detailed information about a specific resume"""
    try:
        current_user_id = get_jwt_identity()
        
        resume = Resume.query.filter_by(
            id=resume_id,
            user_id=current_user_id,
            is_active=True
        ).first()
        
        if not resume:
            return jsonify({
                'success': False,
                'message': 'Resume not found'
            }), 404
        
        resume_data = resume.to_dict()
        
        # Include extracted text if available
        if resume.extracted_text:
            resume_data['extracted_text'] = resume.extracted_text
        
        return jsonify({
            'success': True,
            'resume': resume_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error fetching resume details',
            'error': str(e)
        }), 500

@upload_bp.route('/resumes/<int:resume_id>', methods=['DELETE'])
@jwt_required()
def delete_resume(resume_id):
    """Delete a resume"""
    try:
        current_user_id = get_jwt_identity()
        
        resume = Resume.query.filter_by(
            id=resume_id,
            user_id=current_user_id
        ).first()
        
        if not resume:
            return jsonify({
                'success': False,
                'message': 'Resume not found'
            }), 404
        
        # Delete physical file
        file_deleted = resume.delete_file()
        
        # Delete database record
        db.session.delete(resume)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resume deleted successfully',
            'file_deleted': file_deleted
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error deleting resume',
            'error': str(e)
        }), 500


