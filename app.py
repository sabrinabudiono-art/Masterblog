import json
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


def load_posts():
    try:
        with open("storage.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    with open("storage.json", "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    blog_posts = load_posts()
    print(blog_posts)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Add the code that handles adding a new blog
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_posts = load_posts()
        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1
        else:
            new_id = 1
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()

    # Remove post with matching ID
    deleted_post = [post for post in blog_posts if post['id'] != post_id]

    save_posts(deleted_post)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = load_posts()
    updated_post = next((post for post in blog_posts if post['id'] == post_id), None)
    print(updated_post)
    if updated_post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        updated_post['author'] = request.form.get('author')
        updated_post['title'] = request.form.get('title')
        updated_post['content'] = request.form.get('content')

        for i, post in enumerate(blog_posts):
            if post["id"] == post_id:
                blog_posts[i] = updated_post
                break

        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=updated_post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
