/**
 * ToDo関連のAPI通信を担当するモジュール
 */


/**
 * [API] 新しいToDoを作成する
 * API: POST /v1/todo/
 * @param {object} todoData - { content: string, deadline: string | null }
 */
export async function createTodo(todoData) {
    console.log('Creating new todo:', todoData);
    try {
        const response = await fetch('/v1/todo/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todoData),
        });

        if (!response.ok) {
            // サーバーからエラー詳細（例：バリデーションエラー）があればそれを取得
            const errorData = await response.json();
            // error.message としてスローし、UI側でキャッチできるようにする
            throw new Error(errorData.detail || response.statusText);
        }
        return await response.json(); // 作成されたToDoオブジェクトを返す
    } catch (error) {
        console.error('Error creating todo:', error);
        throw error; // エラーを呼び出し元 (createTodoPage.js) に投げる
    }
}

/**
 * [API] 既存のToDoを更新する (editTodoPage.js が使用)
 * API: PUT /v1/todo/{todoId}
 * @param {number} todoId - 更新するToDoのID
 * @param {object} todoData - { content, deadline, completed }
 */
export async function updateTodo(todoId, todoData) {
    console.log(`Updating todo ${todoId} with data:`, todoData);
    try {
        const response = await fetch(`/v1/todo/${todoId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todoData), // フォームの全データを送信
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || response.statusText);
        }
        return await response.json(); // 更新されたToDoオブジェクトを返す
    } catch (error) {
        console.error('Error updating todo:', error);
        throw error; // エラーを呼び出し元 (editTodoPage.js) に投げる
    }
}



/**
 * [API] ToDoにタグを紐付ける
 * API: POST /v1/todo/{todoId}/tags/{tagId}
 */
export async function addTagToTodo(todoId, tagId) {
    console.log(`Adding tag ${tagId} to todo ${todoId}`);
    try {
        const response = await fetch(`/v1/todo/${todoId}/tags/${tagId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || response.statusText);
        }
        return await response.json(); // 更新されたToDoオブジェクトを返す
    } catch (error) {
        console.error('Error adding tag:', error);
        throw error; // エラーを呼び出し元に投げる
    }
}

/**
 * [API] ToDoとタグの紐付けを解除する
 * API: DELETE /v1/todo/{todoId}/tags/{tagId}
 */
export async function removeTagFromTodo(todoId, tagId) {
    console.log(`Removing tag ${tagId} from todo ${todoId}`);
    try {
        const response = await fetch(`/v1/todo/${todoId}/tags/${tagId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) { console.warn("Could not parse error response as JSON"); }
            throw new Error(errorDetail);
        }
        return true; // 成功したことを示す
    } catch (error) {
        console.error('Network or other error:', error);
        throw error; // エラーを呼び出し元に投げる
    }
}

/**
 * [API] ToDo自体を削除する
 * API: DELETE /v1/todo/{todoId}
 */
export async function deleteTodo(todoId) {
    console.log(`Deleting todo ${todoId}`);
    try {
        const response = await fetch(`/v1/todo/${todoId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) { console.warn("Could not parse error response as JSON"); }
            throw new Error(errorDetail);
        }
        return true; // 成功したことを示す
    } catch (error) {
        console.error('Network or other error:', error);
        throw error;
    }
}

/**
 * [API] ToDoの完了/未完了ステータスを切り替える
 * API: PUT /v1/todo/{todoId}
 */
export async function toggleTodoStatus(todoId, isCompleted) {
    console.log(`Toggling todo ${todoId} status to: ${isCompleted}`);
    const updateData = { completed: isCompleted };

    try {
        const response = await fetch(`/v1/todo/${todoId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData),
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try { const errorData = await response.json(); errorDetail = errorData.detail || errorDetail; } catch (e) {}
            throw new Error(errorDetail);
        }
        return await response.json(); // 更新されたToDoオブジェクトを返す
    } catch (error) {
        console.error('Network or other error:', error);
        throw error;
    }
}
