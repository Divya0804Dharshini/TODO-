from flask import Flask, request, jsonify, session, render_template_string
import db

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    with open('templates/index.html') as f:
        return render_template_string(f.read())

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if db.get_user_by_email(data['email']):
        return jsonify({'status': 'fail', 'reason': 'Email already registered'}), 409
    db.create_user(data['username'], data['email'], data['password'])  # <-- fixed here
    return jsonify({'status': 'success'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = db.get_user_by_email(data['email'])
    if user and user['password'] == data['password']:
        session['user_id'] = user['user_id']  # <-- fixed here
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'status': 'logged out'})

@app.route('/add-task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return jsonify({'status': 'unauthorized'}), 401
    data = request.json
    db.create_task(
        session['user_id'],
        data['task_name'],           # <-- updated key
        data['description'],         # <-- new field required
        data['due_date'],            # <-- renamed key
        data['priority'],
        data['category_id']
    )
    return jsonify({'status': 'task added'})

@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return jsonify([])
    return jsonify(db.get_user_tasks(session['user_id']))

@app.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    if 'user_id' not in session:
        return jsonify({'status': 'unauthorized'}), 401
    db.delete_task(session['user_id'], task_id)
    return jsonify({'status': 'deleted'})

@app.route('/update-task/<int:task_id>', methods=['PUT'])
def update(task_id):
    if 'user_id' not in session:
        return jsonify({'status': 'unauthorized'}), 401
    data = request.json
    db.update_task(
        task_id,
        data['task_name'],         # <-- renamed key
        data['due_date'],          # <-- renamed key
        data['priority'],
        data['category_id']
    )
    return jsonify({'status': 'updated'})

# ---------- Category Endpoints ----------

@app.route('/add-category', methods=['POST'])
def add_category():
    data = request.json
    db.create_category(data['name'], data['description'])
    return jsonify({'status': 'category added'})

@app.route('/categories')
def categories():
    return jsonify(db.get_all_categories())

@app.route('/delete-category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    db.delete_category(category_id)
    return jsonify({'status': 'deleted'})

@app.route('/update-category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    db.update_category(category_id, data['name'], data['description'])
    return jsonify({'status': 'updated'})

if __name__ == '__main__':
    app.run(debug=True)
