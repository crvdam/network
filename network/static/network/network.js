document.addEventListener('DOMContentLoaded', () => { 
    // Edit button
    document.querySelectorAll('.edit-button').forEach(function(button) {
        button.onclick = () => {
            // Before showing edit form, hide all other edit forms/display all posts. To prevent editing multiple posts.
            document.querySelectorAll(".edit-form-div").forEach(function(form) {
                form.style.display = 'none';
            })
            document.querySelectorAll(".post-content").forEach(function(post){
                post.style.display = 'block';
            })
            
            // Hide post content
            post = document.querySelector(`#post-${button.id}-content`);
            post.style.display = 'none';

            // Display edit form
            edit_form = document.querySelector(`#edit-form-div-${button.id}`);
            edit_form.style.display = 'block';

            // Update post content
            document.querySelector(`#edit-submit-${button.id}`).onclick = () => {
                const content = document.querySelector(`#edit-content-${button.id}`).value;
                const post_id = button.id;
                
                fetch('/edit_post', {
                    method: 'POST',
                    body: JSON.stringify({
                        content: content,
                        post_id: post_id
                    })
                })
                .then(response => response.json())
                .then(result => {
                })

                // Hide edit form and display post with new content
                post.innerHTML = content;
                post.style.display = 'block';
                edit_form.style.display = 'none';
            }
        }
    });

    // Like button
    document.querySelectorAll('.like-button').forEach(function(button) {
        button.onclick = () => {
            // Update like count
            post_id = button.id.substring(12)
            fetch('/like', {
                    method: 'POST',
                    body:JSON.stringify({
                    post_id: post_id
                })
            })
            .then(response => response.json())
            // Update html for total likes
            .then(result => {
                document.querySelector(`#total-likes-${post_id}`).innerHTML = result["total_likes"]
            })

            // Change like/unlike button
            like_button = document.querySelector(`#like-button-${post_id}`);
            if (like_button.alt === "Like") {
                like_button.src = "https://cdn-icons-png.flaticon.com/128/833/833472.png"
                like_button.alt = "Unlike"
            } else {
                like_button.src = "https://cdn-icons-png.flaticon.com/128/1077/1077035.png"
                like_button.alt = "Like"
            }
        }
    })
});

