/**
 * /todo/new ページ (create_todo.html) 専用のスクリプト
 */
import { createTodo } from './todo.js';

/**
 * フォーム送信イベントを処理する
 * @param {Event} event 
 */
async function handleCreateTodo(event) {
    event.preventDefault(); 

    const form = document.getElementById('create-todo-form');
    const contentInput = document.getElementById('content');
    const deadlineInput = document.getElementById('deadline');

    const content = contentInput.value;
    const deadline = deadlineInput.value || null; 

    if (!content.trim()) {
        alert('内容を入力してください。');
        return;
    }

    const todoData = {
        content: content,
        deadline: deadline 
    };

    try {
        const createdTodo = await createTodo(todoData); // APIモジュールを呼び出す
        console.log('Todo created:', createdTodo);
        alert('ToDoが作成されました!');
        
        form.reset(); // フォームをリセット
        
        // 任意: 成功したら一覧ページに戻る
        // window.location.href = '/'; 

    } catch (error) {
        console.error('Network or other error:', error);
        // エラーメッセージを `error.message` から取得
        alert(`todoが作成できませんでした。: ${error.message}`);
    }
}

// フォームの送信イベントリスナーを登録
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('create-todo-form');
    if (form) {
        // HTMLのonsubmit属性の代わりに、ここでリスナーを登録
        form.addEventListener('submit', handleCreateTodo);
    }
});
