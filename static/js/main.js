  let availableTags = [];

        const tagListUl = document.getElementById('tag-list');

        function populateTagManagementList() {
            if (!tagListUl) return;
            tagListUl.innerHTML = '';

            if (availableTags.length === 0) {
                tagListUl.innerHTML = '<li>利用可能なタグはありません。</li>';
                return;
            }

            availableTags.forEach(tag => {
                const li = document.createElement('li');
                li.setAttribute('data-tag-id', tag.id);

                const tagNameSpan = document.createElement('span');
                tagNameSpan.className = 'tag-name';
                tagNameSpan.textContent = tag.name;

                const deleteButton = document.createElement('button');
                deleteButton.className = 'delete-tag-btn';
                deleteButton.textContent = '削除';
                deleteButton.onclick = () => deleteTag(tag.id, tag.name);

                li.appendChild(tagNameSpan);
                li.appendChild(deleteButton);
                tagListUl.appendChild(li);
            });
        }

        async function loadTags() {
            try {
                const response = await fetch('/v1/tag/');
                if (!response.ok) {
                    throw new Error(`Failed to fetch tags: ${response.statusText}`);
                }
                availableTags = await response.json();
                console.log('Available tags loaded:', availableTags);
                populateTagDropdowns();
                populateTagManagementList();
            } catch (error) {
                console.error('Error loading tags:', error);
                alert('タグ一覧の読み込みに失敗しました。');
                if (tagListUl) tagListUl.innerHTML = '<li>タグ一覧の読み込みに失敗しました。</li>'; // ★★★ エラー表示 ★★★
            }
        }

        function populateTagDropdowns() {
            const selects = document.querySelectorAll('select[name="tag_id"]');

            selects.forEach(select => {
                while (select.options.length > 1) {
                    select.remove(1);
                }

                availableTags.forEach(tag => {
                    const option = document.createElement('option');
                    option.value = tag.id;
                    option.textContent = tag.name;
                    select.appendChild(option);
                });
            });
        }

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
                    alert(`タグの追加に失敗しました: ${errorData.detail || response.statusText}`);
                } else {
                    const updatedTodo = await response.json();
                    console.log('Tag added:', updatedTodo);
                    alert('タグが追加されました！');

                    window.location.reload();
                }
            } catch (error) {
                console.error('Network or other error:', error);
                alert('タグの追加中にエラーが発生しました。');
            }
        }

        async function deleteTodo(event, todoId) {
            event.preventDefault();

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
                    } catch (e) {
                         console.warn("Could not parse error response as JSON");
                    }
                    console.error('Error deleting todo:', errorDetail);
                    alert(`ToDoの削除に失敗しました: ${errorDetail}`);
                } else {
                    console.log('Todo deleted successfully');
                    alert('ToDoが削除されました!');

                    window.location.reload();
                }
            } catch (error) {
                console.error('Network or other error:', error);
                alert('ToDoの削除中にエラーが発生しました。');
            }
        }

        async function createTag(event) {
            event.preventDefault();
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
                    alert(`タグの作成に失敗しました: ${errorDetail}`);
                } else {
                    const newTag = await response.json();
                    console.log('Tag created:', newTag);
                    alert(`タグ「${newTag.name}」が作成されました！`);

                    tagNameInput.value = '';
                    availableTags.push(newTag);
                    availableTags.sort((a, b) => a.name.localeCompare(b.name));
                    populateTagDropdowns();
                    populateTagManagementList(); 
                }
            } catch (error) {
                console.error('Network or other error:', error);
                alert('タグの作成中にエラーが発生しました。');
            }
        }


         async function removeTag(event, todoId, tagId) {
            event.preventDefault();

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

                    window.location.reload();
                }
            } catch (error) {
                console.error('Network or other error:', error);
                alert('タグの削除中にエラーが発生しました。');
            }
        }


        async function deleteTag(tagId, tagName) {
            console.log(`Attempting to delete tag: ${tagName} (ID: ${tagId})`);

            if (!confirm(`タグ「${tagName}」をデータベースから完全に削除しますか？\nこのタグが紐付いているすべてのToDoからも解除されます。（注意：元に戻せません）`)) {
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
                        console.warn("Could not parse error response as JSON (maybe empty on success)");

                    }
                    console.error('Error deleting tag:', errorDetail);
                    alert(`タグ「${tagName}」の削除に失敗しました: ${errorDetail}\n（他のToDoで使用されている可能性があります）`);
                } else {
                    console.log(`Tag ${tagId} (${tagName}) deleted successfully`);
                    alert(`タグ「${tagName}」が削除されました！`);

                    
                    availableTags = availableTags.filter(tag => tag.id !== tagId); // グローバルリストから削除
                    populateTagDropdowns();
                    populateTagManagementList();
                }
            } catch (error) {
                console.error('Network or other error during tag deletion:', error);
                alert(`タグ「${tagName}」の削除中にエラーが発生しました。`);
            }
        }

        document.addEventListener('DOMContentLoaded', loadTags);