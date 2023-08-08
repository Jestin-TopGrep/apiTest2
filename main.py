from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Tasks(BaseModel):
    id: int
    title: str
    description: str


tasks = [
    Tasks(id=1, title="Buy groceries", description="Milk, eggs, bread"),
    Tasks(id=2, title="Finish report", description="Complete project report by Friday"),
]

# get all tasks
@app.get('/tasks')
def get_tasks():
    return tasks

# get tasks by id
@app.get('/tasks/{task_id}')
def get_by_id(task_id: int):
    if task_id <= len(tasks):
        for task in tasks:
            if task.id == task_id:
                return task
    raise HTTPException(status_code=404, detail="Task not found")

# post tasks
@app.post('/tasks')
def add_tasks(task: Tasks):
    tasks.append(task)
    return {"message": f"Task '{task.title}' added successfully", "task": task}

# update tasks
@app.put('/tasks/{task_id}')
def update_by_id(task_id: int, updated_task: Tasks):
    if task_id > 0 and task_id <= len(tasks):
        for task in tasks:
            if task.id == task_id:
                task.title = updated_task.title
                task.description = updated_task.description
        return {"message": f"Task updated successfully", "task": updated_task}
    raise HTTPException(status_code=404, detail="No task with the provided id")


@app.delete('/tasks/{task_id}')
def delete_by_id(task_id: int):
    if task_id > 0 and task_id <= len(tasks):
        for task in tasks:
            if task.id == task_id:
                tasks.remove(task)
                return {"message": f"Task deleted successfully"}
        raise HTTPException(status_code=404, detail="Task not found")