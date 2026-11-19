from flask import Blueprint, jsonify
from models.repository import DocumentRepository

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/documents')
def list_documents():
    repo = DocumentRepository(api_bp.config['DOCS_DIR'])
    documents = repo.list()
    
    result = []
    for doc in documents:
        result.append({
            'slug': doc.slug,
            'title': doc.title,
            'section': doc.section,
            'order': doc.order,
            'tags': doc.tags
        })
    
    return jsonify(result)


@api_bp.route('/api/documents/<path:slug>')
def get_document(slug):
    repo = DocumentRepository(api_bp.config['DOCS_DIR'])
    doc = repo.get(slug)
    
    if not doc:
        return jsonify({'error': 'Document not found'}), 404
    
    return jsonify({
        'slug': doc.slug,
        'title': doc.title,
        'content': doc.content,
        'section': doc.section,
        'order': doc.order,
        'tags': doc.tags
    })
