/**
 * このファイルは、ToDoアプリのフロントエンド（index.html, create_todo.html など）
 * で使用されるJavaScript関数を定義します。
 */

// グローバル変数として、利用可能なタグのリストを保持する
let availableTags = [];

// タグ管理リストのUL要素をあらかじめ取得しておく
const tagListUl = document.getElementById('tag-list');

/**
 * ページ読み込み完了時に実行されるメイン関数
 * /v1/tag/ APIを呼び出して、タグ一覧を取得し、UIを更新する
 */
async function loadTags() {
    try {
        const response = await fetch('/v1/tag/');
        if (!response.ok) {
            throw new Error(`Failed to fetch tags: ${response.statusText}`);
        }
        availableTags = await response.json();
        console.log('Available tags loaded:', availableTags);
        
        // 取得したタグで、ToDo一覧のドロップダウンを更新
        populateTagDropdowns();
        // 取得したタグで、タグ管理リストを更新
        populateTagManagementList();
        
    } catch (error) {
        console.error('Error loading tags:', error);
        alert('タグ一覧の読み込みに失敗しました。');
        if (tagListUl) tagListUl.innerHTML = '<li>タグ一覧の読み込みに失敗しました。</li>';
    }
}

/**
 * 取得したタグ一覧 (availableTags) を使って、
 * ToDo一覧ページにある全てのタグ選択ドロップダウンの中身を生成する
 */
function populateTagDropdowns() {
    // ページ内にあるすべてのタグ選択ドロップダウンを取得
    const selects = document.querySelectorAll('select[name="tag_id"]');

    selects.forEach(select => {
        // 既存のオプションをクリア (「選択してください」の最初のオプションは残す)
        while (select.options.length > 1) {
            select.remove(1);
        }

        // availableTags グローバル変数からオプションを追加
        availableTags.forEach(tag => {
            const option = document.createElement('option');
            option.value = tag.id;
            option.textContent = tag.name;
            select.appendChild(option);
        });
    });
}

/**
 * 取得したタグ一覧 (availableTags) を使って、
 * タグ管理セクションのリスト (ul#tag-list) の中身を生成する
 */
function populateTagManagementList() {
    if (!tagListUl) return; // タグ管理リストが存在しないページでは何もしない
    
    tagListUl.innerHTML = ''; // リストをクリア

    if (availableTags.length === 0) {
        tagListUl.innerHTML = '<li>利用可能なタグはありません。</li>';
        return;
    }

    // availableTags グローバル変数からリスト項目を生成
    availableTags.forEach(tag => {
        const li = document.createElement('li');
        li.setAttribute('data-tag-id', tag.id);

        const tagNameSpan = document.createElement('span');
        tagNameSpan.className = 'tag-name';
        tagNameSpan.textContent = tag.name;

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-tag-btn';
        deleteButton.textContent = '削除';
        deleteButton.onclick = () => deleteTag(tag.id, tag.name); // 削除関数を紐付け

        li.appendChild(tagNameSpan);
        li.appendChild(deleteButton);
        tagListUl.appendChild(li);
    });
}

/**
 * [ToDo一覧ページ]
 * 既存のToDoにタグを紐付ける (「追加」ボタンクリック時)
 * API: POST /v1/todo/{todoId}/tags/{tagId}
 * @param {number} todoId - 紐付け対象のToDoのID
 */
async function addTag(todoId) {
    const selectElement = document.getElementById(`tag-select-${todoId}`);
    const tagId = selectElement.value;

    if (!tagId) {
        alert('追加するタグを選択してください。');
        return;
    }

    console.log(`Adding tag ${tagId} to todo ${todoId}`);

    try {
        const response = await fetch(`/v1/todo/${todoId}/tags/${tagId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error adding tag:', errorData);
            alert(`30字以内で入力してください。: ${errorData.detail || response.statusText}`);
        } else {
            const updatedTodo = await response.json();
            console.log('Tag added:', updatedTodo);
            alert(`タグが追加されました！ (Todo: ${updatedTodo.content}, Tag: ${updatedTodo.tags[updatedTodo.tags.length -1].name})`);
            
            // ページをリロードして表示を更新
            window.location.reload(); 
        }
    } catch (error) {
        console.error('Network or other error:', error);
        alert('タグの追加中にエラーが発生しました。');
    }
}

/**
 * [ToDo一覧ページ]
 * ToDoとタグの紐付けを解除する (タグ横の[x]ボタンクリック時)
 * API: DELETE /v1/todo/{todoId}/tags/{tagId}
 * @param {Event} event - イベントオブジェクト
 * @param {number} todoId - 対象のToDoのID
 * @param {number} tagId - 解除するタグのID
 */
async function removeTag(event, todoId, tagId) {
    event.preventDefault(); // デフォルト動作をキャンセル
    event.stopPropagation(); // イベントの伝播を停止

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
            console.error('Error removing tag:', errorDetail);
            alert(`タグの削除に失敗しました: ${errorDetail}`);
        } else {
            console.log('Tag removed successfully');
            alert('タグが削除されました！');
            
            // ページをリロードして表示を更新
            window.location.reload(); 
        }
    } catch (error) {
        console.error('Network or other error:', error);
        alert('タグの削除中にエラーが発生しました。');
    }
}

/**
 * [ToDo一覧ページ]
 * ToDo自体を削除する ([削除]リンククリック時)
 * API: DELETE /v1/todo/{todoId}
 * @param {Event} event - イベントオブジェクト
 * @param {number} todoId - 削除するToDoのID
 */
async function deleteTodo(event, todoId) {
    event.preventDefault(); // リンクのデフォルト動作をキャンセル

    console.log(`Deleting todo ${todoId}`);

    // (環境によっては confirm が動作しないため、確認なしで削除)
    // if (!confirm(`ToDo (ID: ${todoId}) を本当に削除しますか？`)) {
    //     return;
    // }

    try {
        const response = await fetch(`/v1/todo/${todoId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) {
                console.warn("Could not parse error response as JSON");
            }
            console.error('Error deleting todo:', errorDetail);
            alert(`ToDoの削除に失敗しました: ${errorDetail}`);
        } else {
            console.log('Todo deleted successfully');
            alert('ToDoが削除されました!');
            
            // ページをリロードして表示を更新
            window.location.reload();
        }
    } catch (error) {
        console.error('Network or other error:', error);
        alert('ToDoの削除中にエラーが発生しました。');
    }
}

/**
 * [ToDo一覧ページ]
 * 新しいタグをデータベースに作成する (フォーム送信時)
 * API: POST /v1/tag/
 * @param {Event} event - フォーム送信イベント
 */
async function createTag(event) {
    event.preventDefault(); // フォームのデフォルト送信をキャンセル
    const tagNameInput = document.getElementById('new-tag-name');
    const tagName = tagNameInput.value.trim();

    if (!tagName) {
        alert('タグ名を入力してください。');
        return;
    }

    console.log(`Creating new tag: ${tagName}`);

    try {
        const response = await fetch('/v1/tag/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: tagName }),
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    if (response.status === 400 && errorData.detail.includes("already exists")) {
                        errorDetail = `タグ名「${tagName}」は既に使用されています。`;
                    } else {
                        errorDetail = errorData.detail;
                    }
                }
            } catch (e) { console.warn("Could not parse error response as JSON"); }
            console.error('Error creating tag:', errorDetail);
            alert(`タグが作成できませんでした。: ${errorDetail}`);
        } else {
            const newTag = await response.json();
            console.log('Tag created:', newTag);
            alert(`タグ「${newTag.name}」が作成されました！`);

            // ★★★ ページをリロードして更新 ★★★
            window.location.reload(); 
        }
    } catch (error) {
        console.error('Network or other error:', error);
        alert('タグの作成中にエラーが発生しました。');
    }
}

/**
 * [ToDo一覧ページ]
 * データベースからタグ自体を削除する ([削除]ボタンクリック時)
 * API: DELETE /v1/tag/{tagId}
 * @param {number} tagId - 削除するタグのID
 * @param {string} tagName - 確認ダイアログ表示用のタグ名
 */
async function deleteTag(tagId, tagName) {
    console.log(`Attempting to delete tag: ${tagName} (ID: ${tagId})`);

    if (!confirm(`タグ「${tagName}」をデータベースから完全に削除しますか？\n（注意：元に戻せません）`)) {
        return;
    }

    try {
        const response = await fetch(`/v1/tag/${tagId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) {
                console.warn("Could not parse error response as JSON");
            }
            console.error('Error deleting tag:', errorDetail);
            alert(`タグ「${tagName}」の削除に失敗しました: ${errorDetail}\n（他のToDoで使用されている可能性があります）`);
        } else {
            console.log(`Tag ${tagId} (${tagName}) deleted successfully`);
            alert(`タグ「${tagName}」が削除されました！`);

            // UIを動的に更新 (ページリロードの代わり)
            availableTags = availableTags.filter(tag => tag.id !== tagId); // グローバルリストから削除
            populateTagDropdowns(); // 全てのドロップダウンを更新
            populateTagManagementList(); // タグ管理リストを更新
        }
    } catch (error) {
        console.error('Network or other error during tag deletion:', error);
        alert(`タグ「${tagName}」の削除中にエラーが発生しました。`);
    }
}


/**
 * [ToDo一覧ページ]
 * ToDoの完了/未完了ステータスを切り替える (チェックボックス変更時)
 * API: PUT /v1/todo/{todoId}
 * @param {number} todoId - 対象のToDoのID
 * @param {boolean} isCompleted - チェックボックスの新しい状態 (true:完了, false:未完了)
 */
async function toggleTodoStatus(todoId, isCompleted) {
    console.log(`Toggling todo ${todoId} status to: ${isCompleted}`);

    // 更新するデータを準備 (completed のみ)
    const updateData = {
        completed: isCompleted
    };

    try {
        const response = await fetch(`/v1/todo/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData), // completed の情報だけを送る
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try { const errorData = await response.json(); errorDetail = errorData.detail || errorDetail; } catch (e) {}
            console.error('Error updating todo status:', errorDetail);
            alert(`ToDoステータスの更新に失敗しました: ${errorDetail}`);
            // エラーが発生した場合、チェックボックスの状態を元に戻す (任意)
            const checkbox = document.getElementById(`todo-${todoId}`);
            if (checkbox) checkbox.checked = !isCompleted;
        } else {
            const updatedTodo = await response.json();
            console.log('Todo status updated:', updatedTodo);

            // UIを更新 (ページリロードの代わりにクラスを付け替える)
            const listItem = document.querySelector(`li[data-todo-id="${todoId}"]`);
            if (listItem) {
                if (isCompleted) {
                    listItem.classList.add('completed');
                } else {
                    listItem.classList.remove('completed');
                }
            }
            // (必要であれば、完了/未完了に応じて他のUI要素も更新)
        }
    } catch (error) {
        console.error('Network or other error:', error);
        alert('ToDoステータスの更新中にエラーが発生しました。');
        // エラーが発生した場合、チェックボックスの状態を元に戻す (任意)
         const checkbox = document.getElementById(`todo-${todoId}`);
         if (checkbox) checkbox.checked = !isCompleted;
    }
}

// ページのHTMLが読み込み終わったら、`loadTags` を実行してタグ一覧を取得する
document.addEventListener('DOMContentLoaded', loadTags);

