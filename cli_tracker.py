import argparse
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
            json.dump(self._tasks, f, indent=4)

    def add(self, task):
        if not isinstance(task, str):
            raise TypeError("Task must be a string.")
        if any(t['description'] == task for t in self._tasks):
            print("Task already exists, skipping.")
            return
        task_info = {
            'id': self._next_id,
            'description': task,
            'status': None,
            'created_at': self.date.strftime("%Y-%m-%d %H:%M"),
            'completed_at': None
        }
        self._tasks.append(task_info)
        print(f"Task added successfully ID: {self._next_id} | at : {self.date.strftime('%Y-%m-%d %H:%M')}.")
        self._next_id += 1
        self._save()

    def update_task(self, task_id, new_task):
        if not isinstance(task_id, int) or not isinstance(new_task, str):
            raise TypeError("Task ID must be int and new task must be str.")
        for task in self._tasks:
            if task['id'] == task_id:
                task['description'] = new_task
                print(f"Task ID: {task_id} updated.")
        self._save()

    def delete_task(self, task_id):
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        self._tasks = [task for task in self._tasks if task['id'] != task_id]
        print(f'Task ID: {task_id} deleted.')
        self._save()

    def mark_tasks(self, task_id, task_status):
        valid_status = ('todo', 'in-progress', 'done')
        if not isinstance(task_id, int) or not isinstance(task_status, str):
            raise TypeError("Task ID must be int and status must be str.")
        if task_status not in valid_status:
            raise ValueError("Task status must be one of: todo, in-progress, done")
        for task in self._tasks:
            if task['id'] == task_id:
                task['status'] = task_status.lower()
                if task['status'] == 'done':
                    task['completed_at'] = self.date.strftime("%Y-%m-%d %H:%M")
        self._save()

    def list_of_tasks(self):
        title = f"{self._name.title()}'s Tasks"
        print(f"\n{title.center(len(title) * 3, '-')}")
        for task in self._tasks:
            for key, val in task.items():
                print(f"{key.title():<14} | {val}")
            print()

    def list_by_status(self, status):
        if not isinstance(status, str):
            raise TypeError("Status must be a string.")
        for task in self._tasks:
            if task['status'] == status.lower():
                print(f"Task: {task['description']} | Status: {task['status']}")

    def clear_tasks(self):
        self._tasks.clear()
        self._save()

    def load_from_json(self):
        if self.file.exists():
            with self.file.open('r', encoding='utf-8') as f:
                self._tasks = json.load(f)
            if self._tasks:
                self._next_id = max(task['id'] for task in self._tasks) + 1


def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("description", help="Task description")

    # Update command
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("description", help="New description")

    # Delete command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Mark command
    mark_parser = subparsers.add_parser("mark")
    mark_parser.add_argument("id", type=int, help="Task ID")
    mark_parser.add_argument("status", choices=["todo", "in-progress", "done"], help="Task status")

    # List command
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=["todo", "in-progress", "done"], help="Filter by status")

    args = parser.parse_args()
    tracker = TasksTracker("Mhark", "tasks.json")

    if args.command == "add":
        tracker.add(args.description)
    elif args.command == "update":
        tracker.update_task(args.id, args.description)
    elif args.command == "delete":
        tracker.delete_task(args.id)
    elif args.command == "mark":
        tracker.mark_tasks(args.id, args.status)
    elif args.command == "list":
        if args.status:
            tracker.list_by_status(args.status)
        else:
            tracker.list_of_tasks()

if __name__ == "__main__":
    main()
