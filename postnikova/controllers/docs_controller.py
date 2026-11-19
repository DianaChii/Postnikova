from flask import Blueprint, render_template, request, abort
from models.repository import DocumentRepository
from services.renderer import MarkdownRenderer

docs_bp = Blueprint('docs', __name__)


@docs_bp.route('/')
def index():
    repo = DocumentRepository(docs_bp.config['DOCS_DIR'])
    documents = repo.list()
    sections = {}
    for doc in documents:
        if doc.section not in sections:
            sections[doc.section] = []
        sections[doc.section].append(doc)
    return render_template('index.html', sections=sections)


@docs_bp.route('/docs/<path:slug>')
def show(slug):
    repo = DocumentRepository(docs_bp.config['DOCS_DIR'])
    doc = repo.get(slug)
    if not doc:
        abort(404)
    renderer = MarkdownRenderer()
    html, toc = renderer.render(doc.content)
    doc.html = html
    doc.toc = toc
    return render_template('document.html', doc=doc)


@docs_bp.route('/search')
def search():
    query = request.args.get('q', '')
    repo = DocumentRepository(docs_bp.config['DOCS_DIR'])
    documents = repo.list()
    results = []
    if query:
        query_lower = query.lower()
        for doc in documents:
            if query_lower in doc.title.lower() or query_lower in doc.content.lower():
                results.append(doc)
    return render_template('search.html', query=query, results=results)


@docs_bp.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
