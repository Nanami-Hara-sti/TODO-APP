import React, { useState, useEffect, useCallback } from 'react';
import './App.css';

const API_BASE_URL = '';

/**
 * Todoアイテム一つ分を管理するコンポーネント
 * @param {object} props - todo, onUpdate, onDelete, onError
 */
function formatDateTime(dt) {
  if (!dt) return '';
  
  try {
    const date = new Date(dt);
    
    // 無効な日付の場合は元の文字列を返す
    if (isNaN(date.getTime())) return dt;
    
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${month}/${day} ${hours}:${minutes}`;
  } catch (error) {
    console.error('日時フォーマットエラー:', error);
    return dt; // エラーの場合は元の値を返す
  }
}

function TodoItem({ todo, onUpdate, onDelete, onError }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(todo.title);
  const [editedDescription, setEditedDescription] = useState(todo.description);
  const [editedStatus, setEditedStatus] = useState(todo.status);

  // 更新処理
  const handleUpdate = () => {
    if (!editedTitle.trim() || !editedDescription.trim()) {
      onError("タイトルと詳細は必須です。");
      return;
    }
    // 親コンポーネントの更新関数を呼び出す
    onUpdate(todo.id, {
      title: editedTitle,
      description: editedDescription,
      status: editedStatus,
    });
    setIsEditing(false); // 編集モードを終了
  };

  // キャンセル処理
  const handleCancel = () => {
    setIsEditing(false);
    // 編集をキャンセルした場合、元の値に戻す
    setEditedTitle(todo.title);
    setEditedDescription(todo.description);
    setEditedStatus(todo.status);
  };

  // 編集モードの場合の表示
  if (isEditing) {
    return (
      <li className="todo-item editing">
        <input
          type="text"
          value={editedTitle}
          onChange={(e) => setEditedTitle(e.target.value)}
          maxLength="255"
        />
        <textarea
          value={editedDescription}
          onChange={(e) => setEditedDescription(e.target.value)}
          maxLength="1000"
        />
        <select value={editedStatus} onChange={(e) => setEditedStatus(e.target.value)}>
          <option value="未着手">未着手</option>
          <option value="進行中">進行中</option>
          <option value="完了">完了</option>
        </select>
        <div className="todo-actions">
          <button onClick={handleUpdate} className="save">保存</button>
          <button onClick={handleCancel} className="cancel">キャンセル</button>
        </div>
      </li>
    );
  }

  // 通常表示
  return (
    <li className={`todo-item status-${todo.status}`}>
      <div className="todo-content">
        <h3>{todo.title} <span>({todo.status})</span></h3>
        <p>{todo.description}</p>
        <div style={{ fontSize: '0.85em', color: '#888', marginTop: '8px' }}>
          <div>作成: {formatDateTime(todo.created_at)}</div>
          <div>更新: {formatDateTime(todo.updated_at)}</div>
        </div>
      </div>
      <div className="todo-actions">
        <button onClick={() => setIsEditing(true)}>編集</button>
        <button onClick={() => onDelete(todo.id)} className="delete">削除</button>
      </div>
    </li>
  );
}

/**
 * メインのAppコンポーネント
 */
function App() {
  // Stateの定義
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("未着手");
  const [todos, setTodos] = useState([]);
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Read (全件取得)
  const fetchTodos = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/todos`);
      if (!response.ok) {
        throw new Error(`TODOの取得に失敗しました。 Status: ${response.status}`);
      }
      const data = await response.json();
      setTodos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  // Create (新規作成)
  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setApiResponse(null);
    setError(null);

    const data = { title, description, status };

    try {
      const response = await fetch(`${API_BASE_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`APIエラー: ${response.status} - ${errorText}`);
      }

      const responseData = await response.json();
      setApiResponse(responseData);
      await fetchTodos();
      // setTodos(prev => [...prev, responseData]); // リストに新しいTODOを追加

      // フォームをクリア
      setTitle("");
      setDescription("");
      setStatus("未着手");

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Update (更新)
  const handleUpdate = async (id, updatedTodoData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedTodoData),
      });
      if (!response.ok) throw new Error('更新に失敗しました');
      
      await fetchTodos();
      setApiResponse(await response.json());
      // const updatedTodoFromServer = await response.json();
      // setTodos(todos.map(todo => (todo.id === id ? updatedTodoFromServer : todo)));
      // setApiResponse(updatedTodoFromServer);

    } catch (err) {
      setError(err.message);
    } finally {
        setIsLoading(false);
    }
  };

  // Delete (削除)
  const handleDelete = async (id) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('削除に失敗しました');

      await fetchTodos();
      // setTodos(todos.filter(todo => todo.id !== id));
      setApiResponse({ message: `ID:${id} のTODOを削除しました。` });

    } catch (err) {
      setError(err.message);
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>TODOアプリ</h1>
      </header>
      
      <main>
        {/* 新規TODO作成フォーム */}
        <div className="todo-form-container">
          <h2>新しいTODOを作成</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="title">タイトル:</label>
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                maxLength="255"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">詳細:</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                maxLength="1000"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="status">ステータス:</label>
              <select 
                id="status" 
                value={status} 
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="未着手">未着手</option>
                <option value="進行中">進行中</option>
                <option value="完了">完了</option>
              </select>
            </div>
            <button type="submit" disabled={isLoading}>
              {isLoading ? '作成中...' : '作成する'}
            </button>
          </form>
        </div>

        {/* APIレスポンス表示エリア (デバッグ用) */}
        {(error || apiResponse) && (
            <div className="response-area">
                <h2>API Response:</h2>
                {isLoading && <p>APIへリクエスト送信中...</p>}
                {error && <div className="error"><p>エラー:</p><pre>{error}</pre></div>}
                {apiResponse && (
                <div className="success">
                    <p>成功:</p>
                    <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
                </div>
                )}
            </div>
        )}

        {/* TODO一覧 */}
        <div className="todo-list-container">
          <h2>TODO一覧</h2>
          {isLoading && !todos.length && <p>TODOを読み込み中...</p>}
          <ul>
            {todos.map(todo => (
              <TodoItem 
                key={todo.id}
                todo={todo}
                onUpdate={handleUpdate}
                onDelete={handleDelete}
                onError={setError}
              />
            ))}
          </ul>
        </div>
      </main>
    </div>
  );
}

export default App;