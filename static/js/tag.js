/**
 * Tag関連のAPI通信を担当するモジュール
 */

/**
 * [API] 全てのタグを取得する
 * API: GET /v1/tag/
 */
export async function fetchTags() {
    try {
        const response = await fetch('/v1/tag/');
        if (!response.ok) {
            throw new Error(`Failed to fetch tags: ${response.statusText}`);
        }
        return await response.json(); // タグの配列を返す
    } catch (error) {
        console.error('Error loading tags:', error);
        throw error;
    }
}

/**
 * [API] 新しいタグを作成する
 * API: POST /v1/tag/
 */
export async function createTag(tagName) {
    console.log(`Creating new tag: ${tagName}`);
    try {
        const response = await fetch('/v1/tag/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: tagName }),
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try {
                const errorData = await response.json();
                if (errorData.detail) {
                    if (response.status === 409) { // 409 Conflict (重複)
                         errorDetail = `タグ名「${tagName}」は既に使用されています。`;
                    } else {
                         errorDetail = errorData.detail;
                    }
                }
            } catch (e) { console.warn("Could not parse error response as JSON"); }
            throw new Error(errorDetail);
        }
        return await response.json(); // 作成されたタグオブジェクトを返す
    } catch (error) {
        console.error('Error creating tag:', error);
        throw error;
    }
}

/**
 * [API] データベースからタグ自体を削除する
 * API: DELETE /v1/tag/{tagId}
 */
export async function deleteTag(tagId) {
    console.log(`Attempting to delete tag (ID: ${tagId})`);
    try {
        const response = await fetch(`/v1/tag/${tagId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            let errorDetail = response.statusText;
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) { console.warn("Could not parse error response as JSON"); }
            throw new Error(`${errorDetail}\n（他のToDoで使用されている可能性があります）`);
        }
        return true; // 成功したことを示す
    } catch (error) {
        console.error('Network or other error during tag deletion:', error);
        throw error;
    }
}
