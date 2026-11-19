from flask import Flask, render_template
from controllers.docs_controller import docs_bp
from controllers.api_controller import api_bp


def create_app():
    app = Flask(__name__, template_folder='views')
    app.config['DOCS_DIR'] = 'docs'
    app.config['SECRET_KEY'] = 'dev-key'
    
    docs_bp.config = app.config
    api_bp.config = app.config
    
    app.register_blueprint(docs_bp)
    app.register_blueprint(api_bp)
    
    # Глобальный обработчик 404
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    # Глобальный обработчик 500
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('404.html'), 500
    
    @app.context_processor
    def inject_menu():
        from models.repository import DocumentRepository
        try:
            repo = DocumentRepository(app.config['DOCS_DIR'])
            documents = repo.list()
            sections = {}
            for doc in documents:
                if doc.section not in sections:
                    sections[doc.section] = []
                sections[doc.section].append(doc)
            return {'sections': sections}
        except Exception as e:
            print(f"Error loading menu: {e}")
            return {'sections': {}}
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)
