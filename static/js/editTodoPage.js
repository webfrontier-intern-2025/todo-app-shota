/**
 * /todo/edit/{id} ページ (edit_todo.html) 専用のスクリプト
 */
import { updateTodo } from './todo.js';

/**
 * フォーム送信イベントを処理する
 * @param {Event} event 
 */
async function handleUpdateTodo(event) {
    event.preventDefault(); 

    // フォーム要素からデータを取得
    const contentInput = document.getElementById('content');
    const deadlineInput = document.getElementById('deadline');
    const completedInput = document.getElementById('completed');
    
    // todoIdをボタンのdata属性から取得
    const submitButton = event.target.querySelector('button[type="submit"]');
    const todoId = submitButton.dataset.todoId;

    const content = contentInput.value;
    const deadline = deadlineInput.value || null;
    const completed = completedInput.checked;

    if (!content.trim()) {
        alert('内容を入力してください。');
        return;
    }

    const todoData = {
        content: content,
        deadline: deadline,
        completed: completed
    };

    try {
        const updatedTodo = await updateTodo(todoId, todoData); // APIモジュールを呼び出す
        console.log('Todo updated:', updatedTodo);
        alert('ToDoが更新されました!');
        
        // 成功したら一覧ページに戻る
        window.location.href = '/'; 

    } catch (error) {
        console.error('Network or other error:', error);
        // エラーメッセージを `error.message` から取得
        alert(`todoが更新できませんでした。: ${error.message}`);
    }
}

// フォームの送信イベントリスナーを登録
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('edit-todo-form');
    if (form) {
        // HTMLのonsubmit属性の代わりに、ここでリスナーを登録
        form.addEventListener('submit', handleUpdateTodo);
    }
});
