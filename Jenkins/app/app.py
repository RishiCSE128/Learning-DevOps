from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn


app = FastAPI()

# Define a Todo item model
class Todo(BaseModel):
    name: str
    description: Optional[str] = None
    completed: bool = False

# In-memory storage for Todo items
todos: List[Todo] = []

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    """
    Create a new todo item and add it to the list.
    """
    todos.append(todo)
    return todo

@app.get("/todos/", response_model=List[Todo])
def read_todos():
    """
    Get the list of all todo items.
    """
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    """
    Get a specific todo item by ID.
    """
    try:
        return todos[todo_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    """
    Update an existing todo item by ID.
    """
    try:
        todos[todo_id] = todo
        return todo
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    """
    Delete a todo item by ID.
    """
    try:
        return todos.pop(todo_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")

if __name__ =='__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)