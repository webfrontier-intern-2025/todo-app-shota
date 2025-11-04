/**
 * このファイルは、ToDoアプリの司令塔（メイン）です。
 * 各モジュールをインポートし、HTMLからのイベントを処理します。
 */

// APIモジュールから関数をインポート
import { addTagToTodo, removeTagFromTodo, deleteTodo, toggleTodoStatus } from './todo.js';
import { fetchTags, createTag, deleteTag } from './tag.js';

// UIモジュールから関数をインポート
import { populateTagDropdowns, populateTagManagementList } from './ui.js';

// グローバル変数として、利用可能なタグのリストを保持する
let availableTags = [];

/**
 * ページ読み込み完了時に実行されるメイン関数
 * タグ一覧を取得し、UIを更新する
 */
async function loadInitialData() {
    try {
        availableTags = await fetchTags(); // API経由でタグを取得
        console.log('Available tags loaded:', availableTags);
        
        // 取得したタグで、UIを更新
        populateTagDropdowns(availableTags);
        // タグ管理リストを更新 (削除ハンドラを渡す)
        populateTagManagementList(availableTags, handleTagDelete); 
        
    } catch (error) {
        console.error('Error loading tags:', error);
        alert('タグ一覧の読み込みに失敗しました。');
        const tagListUl = document.getElementById('tag-list');
        if (tagListUl) tagListUl.innerHTML = '<li>タグ一覧の読み込みに失敗しました。</li>';
    }
}

// -----------------------------------------------------------------
// HTMLのonclick属性から呼び出されるグローバルなイベントハンドラ
// -----------------------------------------------------------------
// ★重要★
// type="module" を使うと、通常の関数はHTMLから直接呼び出せなくなります。
// そのため、HTMLのonclick属性から呼び出す関数は、
// `window` オブジェクトにアタッチしてグローバルにする必要があります。

/**
 * [HTML onclick] ToDoにタグを追加
 */
window.addTag = async function(todoId) {
    const selectElement = document.getElementById(`tag-select-${todoId}`);
    const tagId = selectElement.value;
    if (!tagId) {
        alert('追加するタグを選択してください。');
        return;
    }
    try {
        await addTagToTodo(todoId, tagId); // API呼び出し
        alert('タグが追加されました！');
        window.location.reload(); // 成功したらリロード (一番簡単なUI更新)
    } catch (error) {
        alert(`エラー: ${error.message}`);
    }
};

/**
 * [HTML onclick] ToDoからタグを削除
 */
window.removeTag = async function(event, todoId, tagId) {
    event.preventDefault();
    event.stopPropagation();
    try {
        await removeTagFromTodo(todoId, tagId); // API呼び出し
        alert('タグが削除されました！');
        window.location.reload();
    } catch (error) {
        alert(`タグの削除に失敗しました: ${error.message}`);
    }
};

/**
 * [HTML onclick] ToDo自体を削除
 */
window.deleteTodo = async function(event, todoId) {
    event.preventDefault();
    try {
        await deleteTodo(todoId); // API呼び出し
        alert('ToDoが削除されました!');
        window.location.reload();
    } catch (error) {
        alert(`ToDoの削除に失敗しました: ${error.message}`);
    }
};

/**
 * [HTML onchange] ToDoのステータスを切り替え
 */
window.toggleTodoStatus = async function(todoId, checkboxElement) {
    const isCompleted = checkboxElement.checked;
    try {
        const updatedTodo = await toggleTodoStatus(todoId, isCompleted); // API呼び出し
        
        // UIを動的に更新 (リロードしない方法)
        const listItem = document.querySelector(`li[data-todo-id="${todoId}"]`);
        if (listItem) {
            listItem.classList.toggle('completed', isCompleted);
        }
    } catch (error) {
        alert(`ToDoステータスの更新に失敗しました: ${error.message}`);
        // エラーが発生した場合、チェックボックスの状態を元に戻す
        checkboxElement.checked = !isCompleted; 
    }
};

/**
 * [UIコールバック] タグ管理リストの削除ボタンハンドラ
 */
async function handleTagDelete(tagId, tagName) {
    if (!confirm(`タグ「${tagName}」をデータベースから完全に削除しますか？\n（注意：元に戻せません）`)) {
        return;
    }
    try {
        await deleteTag(tagId); // API呼び出し
        alert(`タグ「${tagName}」が削除されました！`);

        // UIを動的に更新 (リロードの代わり)
        availableTags = availableTags.filter(tag => tag.id !== tagId); // グローバルリストから削除
        populateTagDropdowns(availableTags); // 全てのドロップダウンを更新
        populateTagManagementList(availableTags, handleTagDelete); // タグ管理リストを更新
        
    } catch (error) {
        alert(`タグ「${tagName}」の削除に失敗しました: ${error.message}`);
    }
}

/**
 * [HTML onsubmit] 新しいタグを作成 (フォーム)
 */
window.createTag = async function(event) {
    event.preventDefault();
    const tagNameInput = document.getElementById('new-tag-name');
    const tagName = tagNameInput.value.trim();
    if (!tagName) {
        alert('タグ名を入力してください。');
        return;
    }

    try {
        await createTag(tagName); // API呼び出し
        alert(`タグ「${tagName}」が作成されました！`);
        window.location.reload(); // リロードして全体を更新
    } catch (error) {
        alert(`タグが作成できませんでした。: ${error.message}`);
    }
};


// ページのHTMLが読み込み終わったら、`loadInitialData` を実行して初期データを取得する
document.addEventListener('DOMContentLoaded', loadInitialData);
