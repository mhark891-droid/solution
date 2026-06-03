import datetime
import pathlib
import json

class TasksTracker:
    def __init__(self, name, file_name):
        self._name = name
        self._tasks = []
        self._next_id = 1
        self.date = datetime.datetime.now()
        self.file = pathlib.Path(file_name)
        self.load_from_json()

    def _save(self):
        with self.file.open('w', encoding='utf-8') as f:
            json.dump(self._tasks, f, indent = 4)
        
    def add(self, task):
        if not isinstance(task, str):
            raise TypeError("Task must be a string.")
        for tasks in self._tasks:
            if task in tasks.values():
                self._tasks = [t for t in self._tasks if tasks['description'] != task]
        else:
            task_info = {
                'id': self._next_id, 
                'description': task, 
                'status': None, 
                'created_at': self.date.strftime("%Y-%m-%d %H:%M"), 
                'completed_at': None
            }
            self._tasks.append(task_info)
            print(f"Tasks added succesfully ID: {self._next_id} | at : {self.date.strftime("%Y-%m-%d %H:%M")}.")
            self._next_id += 1
            self._save()

    def update_task(self, tasks_id, new_task):
        if not isinstance(tasks_id, int) and not isinstance(new_task, str):
            raise TypeError("Task ID should be a an integer while new tasks should always be str.")
        for task in self._tasks:
            if task['id'] == tasks_id:
                task['description'] = new_task
        print(f"Tasks ID: {tasks_id} has been sucessfully updated!")
        self._save()

    def delete_task(self, task_id):
        if not isinstance(task_id, int):
            raise TypeError("Task ID should be an integer")
        for task in self._tasks:
            if task['id'] == task_id:
                self._tasks = [task for task in self._tasks if task['id'] != task_id]
        print(f'Task ID: {task_id} deleted.')
        self._save()

    def mark_tasks(self, task_id, task_status):
        task_stats = ('todo', 'in-progress', 'done')
        if not isinstance(task_status, str) and not isinstance(task_id, int):
            raise TypeError("Tasks status should be an intiger.")
        if task_status not in task_stats:
            raise ValueError("Task status must be one of these ('todo', 'in-progress', 'done')")
        for task in self._tasks:
            if task['id'] == task_id:
                task['status'] = task_status.lower()
                if task['status'] == 'done':
                    task['completed_at'] = self.date.strftime("%Y-%m-%d %H:%M")
        self._save()
                    
    def list_of_tasks(self):
        title = f"{self._name.title()}'s 'Tasks'"
        print(f"\n{title.center(len(title) * 3, '-')}")
        for task in self._tasks:
            for key, val in task.items():
                print(f"{key.title():<14} | {val}")
            print()
            
    def list_by_status(self, status):
        if not isinstance(status, str):
            raise TypeError("Status must be a string.")
        for tasks in self._tasks:
            if tasks['status'] == status.lower():
                print(f"Tasks: {tasks['description'].title():<5} | Status: {tasks['status'].title()}")

    def clear_tasks(self):
        self._tasks.clear()
        self._save()

    def load_from_json(self):
        if self.file.exists():
            with self.file.open('r', encoding='utf-8') as f:
                self._tasks = json.load(f)
            if self._tasks:
                self._nex_id = max(task['id'] for task in self._tasks) + 1
        

t = TasksTracker("Mhark", 'new_tasks_tracker.json')


t.add('Washing')
t.add('cleaning')
t.mark_tasks(2, 'todo')
t.mark_tasks(1, 'done')

t.list_of_tasks()
