'use client';

import { useState, useEffect, FormEvent } from 'react';
import axios from 'axios';

interface Todo {
  id: string;
  task: string;
  completed: boolean;
}

const API_URL = 'http://localhost:8000/api/todos';

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTask, setNewTask] = useState('');
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTaskText, setEditTaskText] = useState('');

  // Fetch all todos on mount
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await axios.get(API_URL);
        setTodos(response.data);
      } catch (error) {
        console.error('Ошибка получения задач:', error);
      }
    };
    fetchTodos();
  }, []);

  // Handle adding a new task
  const handleAddTask = async (e: FormEvent) => {
    e.preventDefault();
    if (!newTask.trim()) return;

    try {
      const response = await axios.post(API_URL, { task: newTask });
      setTodos([...todos, response.data]);
      setNewTask('');
    } catch (error) {
      console.error('Ошибка добавления задачи:', error);
    }
  };

  // Handle toggling task completion
  const handleToggleComplete = async (id: string) => {
    try {
      const response = await axios.patch(`${API_URL}/${id}`);
      setTodos(todos.map(todo => (todo.id === id ? response.data : todo)));
    } catch (error) {
      console.error('Ошибка обновления статуса задачи:', error);
    }
  };

  // Handle deleting a task
  const handleDeleteTask = async (id: string) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('Ошибка удаления задачи:', error);
    }
  };

  // Handle starting task edit
  const handleEditTask = (id: string, task: string) => {
    setEditingId(id);
    setEditTaskText(task);
  };

  // Handle saving edited task
  const handleSaveEdit = async (id: string) => {
    if (!editTaskText.trim()) return;

    try {
      const response = await axios.put(`${API_URL}/${id}`, { task: editTaskText });
      setTodos(todos.map(todo => (todo.id === id ? response.data : todo)));
      setEditingId(null);
      setEditTaskText('');
    } catch (error) {
      console.error('Ошибка редактирования задачи:', error);
    }
  };

  // Handle canceling edit
  const handleCancelEdit = () => {
    setEditingId(null);
    setEditTaskText('');
  };

  // Handle clearing all completed tasks
  const handleClearCompleted = async () => {
    try {
      await axios.delete(`${API_URL}/completed`);
      setTodos(todos.filter(todo => !todo.completed));
    } catch (error) {
      console.error('Ошибка удаления завершенных задач:', error);
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-8">
      <div className="w-full max-w-md bg-gray-800 p-6 rounded-lg shadow-lg animate-fadeIn">
        <h1 className="text-3xl font-bold mb-6 text-center text-cyan-400">
          Список задач
        </h1>

        {/* Form to add a new task */}
        <form onSubmit={handleAddTask} className="flex gap-2 mb-6">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="Добавить новую задачу..."
            className="flex-grow p-2 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
          />
          <button
            type="submit"
            className="bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200"
          >
            Добавить
          </button>
        </form>

        {/* Clear completed tasks button */}
        {todos.some(todo => todo.completed) && (
          <button
            onClick={handleClearCompleted}
            className="w-full mb-4 bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors duration-200"
          >
            Очистить завершенные
          </button>
        )}

        {/* List of tasks */}
        <ul className="space-y-3">
          {todos.map((todo) => (
            <li
              key={todo.id}
              className="flex items-center justify-between p-3 bg-gray-700 rounded-md animate-slideIn"
            >
              {editingId === todo.id ? (
                <input
                  type="text"
                  value={editTaskText}
                  onChange={(e) => setEditTaskText(e.target.value)}
                  className="flex-grow p-1 rounded bg-gray-600 border border-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              ) : (
                <span
                  onClick={() => handleToggleComplete(todo.id)}
                  className={`cursor-pointer flex-grow ${todo.completed ? 'line-through text-gray-500' : ''}`}
                >
                  {todo.task}
                </span>
              )}
              <div className="flex gap-2">
                {editingId === todo.id ? (
                  <>
                    <button
                      onClick={() => handleSaveEdit(todo.id)}
                      className="bg-green-600 hover:bg-green-700 text-white text-xs font-bold py-1 px-2 rounded-full transition-colors"
                    >
                      Сохранить
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="bg-gray-600 hover:bg-gray-700 text-white text-xs font-bold py-1 px-2 rounded-full transition-colors"
                    >
                      Отмена
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => handleEditTask(todo.id, todo.task)}
                    className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold py-1 px-2 rounded-full transition-colors"
                  >
                    Редактировать
                  </button>
                )}
                <button
                  onClick={() => handleDeleteTask(todo.id)}
                  className="bg-red-600 hover:bg-red-700 text-white text-xs font-bold py-1 px-2 rounded-full transition-colors"
                >
                  ✕
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}