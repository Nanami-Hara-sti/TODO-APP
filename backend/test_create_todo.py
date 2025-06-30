"""
TODO API POST機能のテスト
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from sql_app.database import get_db
from test_database import get_test_db, create_test_database, cleanup_test_database
import datetime
import json

# テスト用のデータベースを使用するようにDependencyを置き換え
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    """各テスト実行前にテスト用データベースを初期化"""
    create_test_database()
    yield
    cleanup_test_database()

class TestCreateTodo:
    """TODO作成機能のテストクラス"""
    
    def test_create_todo_success(self, test_db):
        """正常なTODO作成のテスト"""
        todo_data = {
            "title": "テストTODO",
            "description": "テスト用の詳細説明",
            "status": "未着手"
        }
        
        response = client.post("/todos", json=todo_data)
        
        # ステータスコードの確認
        assert response.status_code == 200
        
        # レスポンスデータの確認
        response_data = response.json()
        assert "id" in response_data
        assert response_data["title"] == todo_data["title"]
        assert response_data["description"] == todo_data["description"]
        assert response_data["status"] == todo_data["status"]
        assert "created_at" in response_data
        assert "updated_at" in response_data
        
        # 日時フォーマットの確認（ISO 8601形式）
        assert response_data["created_at"].endswith("Z")
        assert response_data["updated_at"].endswith("Z")
        
        # 作成日時と更新日時が適切に設定されているか確認
        created_at = datetime.datetime.fromisoformat(response_data["created_at"].replace("Z", "+00:00"))
        updated_at = datetime.datetime.fromisoformat(response_data["updated_at"].replace("Z", "+00:00"))
        assert isinstance(created_at, datetime.datetime)
        assert isinstance(updated_at, datetime.datetime)
    
    def test_create_todo_minimal_data(self, test_db):
        """最小限のデータでTODO作成のテスト"""
        todo_data = {
            "title": "最小限TODO"
        }
        
        response = client.post("/todos", json=todo_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == "最小限TODO"
        assert response_data["description"] is None
        assert response_data["status"] == "未着手"  # デフォルト値
    
    def test_create_todo_with_different_status(self, test_db):
        """異なるステータスでのTODO作成テスト"""
        statuses = ["未着手", "進行中", "完了"]
        
        for status in statuses:
            todo_data = {
                "title": f"{status}のTODO",
                "description": f"{status}状態のテスト",
                "status": status
            }
            
            response = client.post("/todos", json=todo_data)
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["status"] == status
    
    def test_create_todo_empty_title(self, test_db):
        """空のタイトルでのTODO作成テスト（バリデーションエラー）"""
        todo_data = {
            "title": "",
            "description": "空のタイトルテスト"
        }
        
        response = client.post("/todos", json=todo_data)
        
        # バリデーション強化により422エラーが返される
        assert response.status_code == 422
        
        # エラーレスポンスの詳細を確認
        error_response = response.json()
        assert "detail" in error_response
        
        # タイトルフィールドのエラーメッセージを確認
        errors = error_response["detail"]
        title_error = None
        for error in errors:
            if error.get("loc") and "title" in error["loc"]:
                title_error = error
                break
        
        assert title_error is not None, "タイトルフィールドのエラーが見つかりません"
    
    def test_create_todo_missing_title(self, test_db):
        """タイトルなしでのTODO作成テスト（バリデーションエラー）"""
        todo_data = {
            "description": "タイトルなしテスト"
        }
        
        response = client.post("/todos", json=todo_data)
        
        # FastAPIのバリデーションエラーを期待
        assert response.status_code == 422
    
    def test_create_todo_long_title(self, test_db):
        """長いタイトルでのTODO作成テスト"""
        long_title = "a" * 255  # 255文字のタイトル
        todo_data = {
            "title": long_title,
            "description": "長いタイトルのテスト"
        }
        
        response = client.post("/todos", json=todo_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == long_title
    
    def test_create_todo_very_long_title(self, test_db):
        """非常に長いタイトルでのTODO作成テスト（バリデーションエラー）"""
        very_long_title = "a" * 300  # 300文字のタイトル（制限255文字を超える）
        todo_data = {
            "title": very_long_title,
            "description": "非常に長いタイトルのテスト"
        }
        
        response = client.post("/todos", json=todo_data)
        
        # スキーマで最大255文字に制限されているため422エラーが返される
        assert response.status_code == 422
        
        # エラーレスポンスの詳細を確認
        error_response = response.json()
        assert "detail" in error_response
        
        # タイトルフィールドのエラーメッセージを確認
        errors = error_response["detail"]
        title_error = None
        for error in errors:
            if error.get("loc") and "title" in error["loc"]:
                title_error = error
                break
        
        assert title_error is not None, "タイトルフィールドのエラーが見つかりません"
        assert "String should have at most 255 characters" in title_error["msg"] or "max_length" in title_error["msg"]
    
    def test_create_todo_long_description(self, test_db):
        """長い詳細説明でのTODO作成テスト"""
        long_description = "d" * 1000  # 1000文字の詳細説明
        todo_data = {
            "title": "長い詳細説明TODO",
            "description": long_description
        }
        
        response = client.post("/todos", json=todo_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["description"] == long_description
    
    def test_create_multiple_todos(self, test_db):
        """複数のTODO作成テスト"""
        todos = [
            {"title": "TODO1", "description": "1番目のTODO"},
            {"title": "TODO2", "description": "2番目のTODO"},
            {"title": "TODO3", "description": "3番目のTODO"}
        ]
        
        created_todos = []
        for todo_data in todos:
            response = client.post("/todos", json=todo_data)
            assert response.status_code == 200
            created_todos.append(response.json())
        
        # IDが連番になっているか確認
        for i, todo in enumerate(created_todos):
            assert todo["title"] == todos[i]["title"]
            assert todo["description"] == todos[i]["description"]
            assert todo["id"] == i + 1  # IDは1から始まる
    
    def test_create_todo_invalid_json(self, test_db):
        """不正なJSONでのテスト"""
        invalid_json = '{"title": "test", "description": }'
        
        response = client.post(
            "/todos",
            content=invalid_json,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_create_todo_invalid_status(self, test_db):
        """不正なステータスでのTODO作成テスト（バリデーションエラー）"""
        todo_data = {
            "title": "不正ステータスTODO",
            "description": "不正なステータスのテスト",
            "status": "不正なステータス"
        }
        
        response = client.post("/todos", json=todo_data)
        
        # バリデーション強化により422エラーが返される
        assert response.status_code == 422
        
        # エラーレスポンスの詳細を確認
        error_response = response.json()
        assert "detail" in error_response
        
        # ステータスフィールドのエラーメッセージを確認
        errors = error_response["detail"]
        status_error = None
        for error in errors:
            if error.get("loc") and "status" in error["loc"]:
                status_error = error
                break
        
        assert status_error is not None, "ステータスフィールドのエラーが見つかりません"
        assert "Input should be" in status_error["msg"] or "value is not a valid enumeration member" in status_error["msg"]
    
    def test_create_todo_response_structure(self, test_db):
        """TODOレスポンスの構造検証テスト"""
        todo_data = {
            "title": "レスポンス構造テスト",
            "description": "レスポンスの構造を詳細に検証",
            "status": "進行中"
        }
        
        response = client.post("/todos", json=todo_data)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # 必須フィールドの存在確認
        required_fields = ["id", "title", "description", "status", "created_at", "updated_at"]
        for field in required_fields:
            assert field in response_data, f"必須フィールド '{field}' が存在しません"
        
        # データ型の確認
        assert isinstance(response_data["id"], int)
        assert isinstance(response_data["title"], str)
        assert isinstance(response_data["description"], str)
        assert isinstance(response_data["status"], str)
        assert isinstance(response_data["created_at"], str)
        assert isinstance(response_data["updated_at"], str)
        
        # ISO 8601フォーマットの確認
        import re
        iso_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z'
        assert re.match(iso_pattern, response_data["created_at"]), "created_atがISO 8601形式ではありません"
        assert re.match(iso_pattern, response_data["updated_at"]), "updated_atがISO 8601形式ではありません"
    
    def test_create_todo_performance(self, test_db):
        """TODO作成のパフォーマンステスト"""
        import time
        
        todo_data = {
            "title": "パフォーマンステスト",
            "description": "レスポンス時間を測定"
        }
        
        start_time = time.time()
        response = client.post("/todos", json=todo_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        # レスポンス時間が1秒以内であることを確認
        assert response_time < 1.0, f"レスポンス時間が遅すぎます: {response_time:.3f}秒"
        
        print(f"TODO作成のレスポンス時間: {response_time:.3f}秒")
    
    def test_create_todo_valid_statuses(self, test_db):
        """有効なステータス値でのTODO作成テスト"""
        valid_statuses = ["未着手", "進行中", "完了"]
        
        for status in valid_statuses:
            todo_data = {
                "title": f"有効ステータステスト_{status}",
                "description": f"{status}ステータスの検証",
                "status": status
            }
            
            response = client.post("/todos", json=todo_data)
            
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["status"] == status
            assert response_data["title"] == f"有効ステータステスト_{status}"
    
    def test_create_todo_various_invalid_statuses(self, test_db):
        """様々な不正ステータス値でのバリデーションテスト"""
        invalid_statuses = [
            "処理中",
            "PENDING", 
            "完成",
            "作業中",
            "123",
            "null"
        ]
        
        for invalid_status in invalid_statuses:
            todo_data = {
                "title": f"不正ステータステスト_{invalid_status}",
                "description": f"{invalid_status}ステータスの検証",
                "status": invalid_status
            }
            
            response = client.post("/todos", json=todo_data)
            
            assert response.status_code == 422, f"ステータス '{invalid_status}' でバリデーションエラーが発生しませんでした"
            
            error_response = response.json()
            assert "detail" in error_response
