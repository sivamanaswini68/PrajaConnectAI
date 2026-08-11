import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from database.db import get_db, close_db, init_db, get_or_create_user
from services.search_service import search_schemes, search_camps, global_search
from services.ai_service import get_ai_response
from services.translation_service import translate_ui, get_translated_scheme

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "prajaconnect_hackathon_super_secret_key_2026")

# Teardown database connection
app.teardown_appcontext(close_db)

# Ensure database tables and seed data are initialized
with app.app_context():
    init_db()

@app.before_request
def ensure_user_session():
    """Ensure every visitor gets an isolated session user record without mandatory login."""
    if 'user_uuid' not in session:
        session['user_uuid'] = str(uuid.uuid4())
    if 'language' not in session:
        session['language'] = 'English'
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Attach current user DB record to g context
    g.current_user = get_or_create_user(
        session['user_uuid'],
        language=session.get('language', 'English')
    )

@app.context_processor
def inject_global_vars():
    """Inject language, user info, and translation helper into all Jinja templates."""
    user = getattr(g, 'current_user', None)
    current_lang = session.get('language', 'English')
    if user and user['language']:
        current_lang = user['language']
        
    def _t(text):
        return translate_ui(text, current_lang)
        
    return {
        'current_user': user,
        'current_language': current_lang,
        '_t': _t,
        'get_translated_scheme': lambda s: get_translated_scheme(s, current_lang)
    }

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home Page matching Image 2 visual reference layout."""
    featured_schemes = search_schemes(query='')[:2]
    featured_camps = search_camps(query='')[:3]
    return render_template('index.html', 
                           active_page='home',
                           featured_schemes=featured_schemes,
                           featured_camps=featured_camps)

@app.route('/schemes')
def schemes():
    """Government Schemes discovery with category & age filtering."""
    cat = request.args.get('category', 'All')
    age = request.args.get('age_group', 'All')
    query = request.args.get('query', '')
    
    results = search_schemes(query=query, category=cat, age_group=age)
    return render_template('schemes.html',
                           active_page='schemes',
                           schemes=results,
                           selected_category=cat,
                           selected_age=age,
                           selected_query=query)

@app.route('/scheme/<int:scheme_id>')
def scheme_detail(scheme_id):
    """Detailed scheme page."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM schemes WHERE id = ?", (scheme_id,))
    scheme = cursor.fetchone()
    if not scheme:
        return render_template('404.html', message="Scheme not found."), 404
    
    current_lang = session.get('language', 'English')
    translated_scheme = get_translated_scheme(dict(scheme), current_lang)
    return render_template('scheme_detail.html', active_page='schemes', scheme=translated_scheme)

@app.route('/apply/<int:scheme_id>', methods=['POST'])
def apply_scheme(scheme_id):
    """Create a real application record in SQLite for the current user."""
    db = get_db()
    cursor = db.cursor()
    user = g.current_user
    
    # Check if application already exists
    cursor.execute("SELECT * FROM applications WHERE user_id = ? AND scheme_id = ?", (user['id'], scheme_id))
    existing = cursor.fetchone()
    
    if not existing:
        today_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO applications (user_id, scheme_id, status, submitted_date) VALUES (?, ?, ?, ?)",
            (user['id'], scheme_id, 'Draft', today_str)
        )
        db.commit()
        
    return redirect(url_for('applications'))

@app.route('/camps')
def camps():
    """Health & Wellness Camps discovery."""
    camp_type = request.args.get('type', 'All')
    district = request.args.get('district', 'All')
    query = request.args.get('query', '')
    
    results = search_camps(query=query, camp_type=camp_type, district=district)
    return render_template('camps.html',
                           active_page='camps',
                           camps=results,
                           selected_type=camp_type,
                           selected_district=district,
                           selected_query=query)

@app.route('/camp/<int:camp_id>')
def camp_detail(camp_id):
    """Detailed health camp view."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM camps WHERE id = ?", (camp_id,))
    camp = cursor.fetchone()
    if not camp:
        return render_template('404.html', message="Health camp not found."), 404
    return render_template('camp_detail.html', active_page='camps', camp=dict(camp))

@app.route('/applications')
def applications():
    """Citizen application tracker (isolated per user session)."""
    db = get_db()
    cursor = db.cursor()
    user = g.current_user
    
    cursor.execute("""
        SELECT a.id, a.status, a.submitted_date, a.notes, s.id as scheme_id, s.name as scheme_name, s.category
        FROM applications a
        JOIN schemes s ON a.scheme_id = s.id
        WHERE a.user_id = ?
        ORDER BY a.id DESC
    """, (user['id'],))
    
    apps_list = [dict(row) for row in cursor.fetchall()]
    return render_template('applications.html', active_page='applications', applications=apps_list)

@app.route('/applications/update_status/<int:app_id>', methods=['POST'])
def update_application_status(app_id):
    """Update status of application in SQLite database."""
    new_status = request.form.get('status', 'Submitted')
    db = get_db()
    cursor = db.cursor()
    user = g.current_user
    
    cursor.execute(
        "UPDATE applications SET status = ? WHERE id = ? AND user_id = ?",
        (new_status, app_id, user['id'])
    )
    db.commit()
    return redirect(url_for('applications'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Citizen Profile management."""
    user = g.current_user
    if request.method == 'POST':
        name = request.form.get('name', 'Citizen')
        age = int(request.form.get('age', 35))
        gender = request.form.get('gender', 'Other')
        state = request.form.get('state', 'Andhra Pradesh')
        district = request.form.get('district', 'Visakhapatnam')
        language = request.form.get('language', 'English')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE users 
            SET name = ?, age = ?, gender = ?, state = ?, district = ?, language = ?
            WHERE id = ?
        """, (name, age, gender, state, district, language, user['id']))
        db.commit()
        
        session['language'] = language
        return redirect(url_for('profile'))
        
    return render_template('profile.html', active_page='profile', user=dict(user))

@app.route('/assistant')
def assistant():
    """AI Chat Assistant Page."""
    return render_template('assistant.html', 
                           active_page='assistant', 
                           chat_history=session.get('chat_history', []))

@app.route('/assistant/chat', methods=['POST'])
def assistant_chat():
    """AI Chat Endpoint handling asynchronous requests."""
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        provider = data.get('provider', 'local')
        language = data.get('language', session.get('language', 'English'))
        
        if not user_message:
            return jsonify({'success': False, 'response': 'Please enter a message.'})
            
        user_profile = dict(g.current_user) if g.current_user else None
        
        # Get AI response grounded in SQLite RAG
        result = get_ai_response(
            user_message=user_message,
            provider=provider,
            language=language,
            user_profile=user_profile
        )
        
        # Append to session history (capped at last 10 messages)
        history = session.get('chat_history', [])
        history.append({'role': 'user', 'content': user_message})
        history.append({'role': 'ai', 'content': result['response']})
        session['chat_history'] = history[-10:]
        
        return jsonify({
            'success': result['success'],
            'response': result['response']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'response': 'AI service is temporarily unavailable. Please try again or switch AI provider.'
        })

@app.route('/assistant/clear', methods=['POST'])
def clear_chat():
    """Clear chat session history."""
    session['chat_history'] = []
    return jsonify({'success': True})

@app.route('/search')
def search():
    """Global search route."""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('home'))
    res = global_search(query)
    return render_template('search.html', 
                           query=query, 
                           schemes=res['schemes'], 
                           camps=res['camps'], 
                           total_results=res['total'])

@app.route('/set_language', methods=['POST'])
def set_language():
    """Change preferred language in session."""
    data = request.get_json() or {}
    lang = data.get('language', 'English')
    session['language'] = lang
    if g.current_user:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET language = ? WHERE id = ?", (lang, g.current_user['id']))
        db.commit()
    return jsonify({'success': True, 'language': lang})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message="Page not found."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', message="Something went wrong. Please try again."), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting PrajaConnectAI Flask Web Server on http://127.0.0.1:{port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
