```python
from flask import render_template, request
from app import app, db
from .models import Result

@app.route('/results', methods=['GET'])
def get_results():
    results = Result.query.all()
    return render_template('results.html', results=results)

@app.route('/result', methods=['POST'])
def add_result():
    result = request.form.get('result')
    new_result = Result(result=result)
    db.session.add(new_result)
    db.session.commit()
    return 'Result added successfully'

@app.route('/result/<int:id>', methods=['GET'])
def get_result(id):
    result = Result.query.get(id)
    if result:
        return render_template('result.html', result=result)
    else:
        return 'Result not found'

@app.route('/result/<int:id>', methods=['DELETE'])
def delete_result(id):
    result = Result.query.get(id)
    if result:
        db.session.delete(result)
        db.session.commit()
        return 'Result deleted successfully'
    else:
        return 'Result not found'
```
