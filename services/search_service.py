from database.db import get_db

def search_schemes(query='', category='All', age_group='All'):
    """Search schemes in SQLite DB by keyword, category, and age group."""
    db = get_db()
    cursor = db.cursor()
    
    sql = "SELECT * FROM schemes WHERE 1=1"
    params = []
    
    if query and query.strip():
        q = f"%{query.strip()}%"
        sql += " AND (name LIKE ? OR description LIKE ? OR benefits LIKE ? OR eligibility LIKE ? OR category LIKE ?)"
        params.extend([q, q, q, q, q])
        
    if category and category != 'All':
        sql += " AND (category = ? OR category LIKE ?)"
        params.extend([category, f"%{category}%"])
        
    if age_group and age_group != 'All' and age_group != 'All Ages':
        sql += " AND (age_group = ? OR age_group = 'All Ages' OR age_group LIKE ?)"
        params.extend([age_group, f"%{age_group}%"])
        
    sql += " ORDER BY id DESC"
    cursor.execute(sql, params)
    return [dict(row) for row in cursor.fetchall()]

def search_camps(query='', camp_type='All', district='All'):
    """Search health camps in SQLite DB by keyword, type, and district."""
    db = get_db()
    cursor = db.cursor()
    
    sql = "SELECT * FROM camps WHERE 1=1"
    params = []
    
    if query and query.strip():
        q = f"%{query.strip()}%"
        sql += " AND (name LIKE ? OR description LIKE ? OR organizer LIKE ? OR location LIKE ? OR camp_type LIKE ?)"
        params.extend([q, q, q, q, q])
        
    if camp_type and camp_type != 'All':
        sql += " AND (camp_type = ? OR camp_type LIKE ?)"
        params.extend([camp_type, f"%{camp_type}%"])
        
    if district and district != 'All':
        sql += " AND (district = ? OR district LIKE ?)"
        params.extend([district, f"%{district}%"])
        
    sql += " ORDER BY date ASC"
    cursor.execute(sql, params)
    return [dict(row) for row in cursor.fetchall()]

def global_search(query):
    """Perform global search across schemes and health camps."""
    schemes = search_schemes(query=query)
    camps = search_camps(query=query)
    return {
        'schemes': schemes,
        'camps': camps,
        'total': len(schemes) + len(camps)
    }
