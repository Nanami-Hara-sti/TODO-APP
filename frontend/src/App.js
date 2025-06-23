import logo from './logo.svg';
// frontend/src/App.js

import React, { useState } from 'react';
import './App.css'; // 簡単なスタイリングのため

function App() {
  // フォームの各入力値を管理するためのState
  const [title, setTitle] = useState("Sample Title");
  const [description, setDescription] = useState("Sample Description");
  const [status, setStatus] = useState("未着手"); // 初期値を設定

  // APIからのレスポンスやエラー、ローディング状態を管理するためのState
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // フォームが送信されたときの処理
  const handleSubmit = async (event) => {
    // フォームのデフォルトの送信動作（ページリロード）を防ぐ
    event.preventDefault();

    // ローディング開始、過去のレスポンスやエラーをクリア
    setIsLoading(true);
    setApiResponse(null);
    setError(null);

    const current_time = new Date().toISOString();
    const data = {
      // id: Math.floor(Math.random() * 1000) + 1,
      title: title,
      description: description,
      status: status,
      // created_at: current_time,
      // updated_at: current_time
    };

    try {
      // バックエンドAPIのエンドポイント
      const url = "http://localhost:8000/todos";

      // fetch APIを使ってPOSTリクエストを送信
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data), // JavaScriptオブジェクトをJSON文字列に変換
      });

      // レスポンスのステータスがOKでない場合はエラーを投げる
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API Error: ${response.status} - ${errorText}`);
      }

      // レスポンスのJSONをパース
      const responseData = await response.json();
      setApiResponse(responseData);

    } catch (err) {
      // ネットワークエラーや上記で投げたエラーをキャッチ
      setError(err.message);
    } finally {
      // ローディング終了
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>API Test (React)</h1>
      
      {/* フォーム */}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title:</label>
          <textarea
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength="255"
            required
          />
        </div>
        <div>
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            maxLength="1000"
            required
          />
        </div>
        <div>
          <label htmlFor="status">Status:</label>
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
        {/* 送信ボタン。ローディング中は無効化する */}
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Submitting...' : 'Submit'}
        </button>
      </form>

      {/* APIレスポンス表示エリア */}
      <div className="response-area">
        <h2>API Response:</h2>
        {isLoading && <p>Sending request to API...</p>}
        {error && <div className="error"><p>Error:</p><pre>{error}</pre></div>}
        {apiResponse && (
          <div className="success">
            <p>Success (Status Code: 200)</p>
            <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;