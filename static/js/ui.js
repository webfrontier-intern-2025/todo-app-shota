/**
 * Tag関連のUI描画を担当するモジュール
 */

/**
 * 取得したタグ一覧を使って、
 * ToDo一覧ページにある全てのタグ選択ドロップダウンの中身を生成する
 */
export function populateTagDropdowns(tags) {
    const selects = document.querySelectorAll('select[name="tag_id"]');
    selects.forEach(select => {
        // 既存のオプションをクリア (「選択してください」の最初のオプションは残す)
        while (select.options.length > 1) {
            select.remove(1);
        }
        // タグの配列からオプションを追加
        tags.forEach(tag => {
            const option = document.createElement('option');
            option.value = tag.id;
            option.textContent = tag.name;
            select.appendChild(option);
        });
    });
}

/**
 * 取得したタグ一覧を使って、
 * タグ管理セクションのリスト (ul#tag-list) の中身を生成する
 * @param {Array} tags - 表示するタグの配列
 * @param {Function} deleteCallback - 削除ボタンが押されたときに実行する関数 (tagId, tagNameを引数に取る)
 */
export function populateTagManagementList(tags, deleteCallback) {
    const tagListUl = document.getElementById('tag-list');
    if (!tagListUl) return; // タグ管理リストが存在しないページでは何もしない
    
    tagListUl.innerHTML = ''; // リストをクリア

    if (tags.length === 0) {
        tagListUl.innerHTML = '<li>利用可能なタグはありません。</li>';
        return;
    }

    // タグの配列からリスト項目を生成
    tags.forEach(tag => {
        const li = document.createElement('li');
        li.setAttribute('data-tag-id', tag.id);

        const tagNameSpan = document.createElement('span');
        tagNameSpan.className = 'tag-name';
        tagNameSpan.textContent = tag.name;

        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-tag-btn';
        deleteButton.textContent = '削除';
        
        // ★重要★ onclick属性の代わりに、コールバック関数を紐付ける
        deleteButton.onclick = () => deleteCallback(tag.id, tag.name); 

        li.appendChild(tagNameSpan);
        li.appendChild(deleteButton);
        tagListUl.appendChild(li);
    });
}
