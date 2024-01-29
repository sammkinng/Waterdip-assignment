from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []


# Bulk add tasks
@app.route('/v1/tasks', methods=['POST'])
def bulk_add_tasks():
    data = request.json
    new_task_ids = []

    for task_data in data.get('tasks', []):
        new_task = {
            "id": len(tasks) + 1,
            "title": task_data.get('title'),
            "is_completed": task_data.get('is_completed', False)
        }
        tasks.append(new_task)
        new_task_ids.append({"id": new_task["id"]})

    return jsonify({"tasks": new_task_ids}), 201


# List all tasks
@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    return jsonify({"tasks": tasks}), 200

# Get a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "There is no task at that id"}), 404

    return jsonify(task), 200

# Edit the title or completion of a specific task
@app.route('/v1/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "There is no task at that id"}), 404

    data = request.json
    task["title"] = data.get('title', task["title"])
    task["is_completed"] = data.get('is_completed', task["is_completed"])

    return '', 204

# Bulk delete tasks
@app.route('/v1/tasks', methods=['DELETE'])
def bulk_delete_tasks():
    data = request.json
    task_ids_to_delete = {task_data['id'] for task_data in data.get('tasks', [])}

    global tasks
    tasks = [t for t in tasks if t["id"] not in task_ids_to_delete]

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
