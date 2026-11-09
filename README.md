# Django Portfolio & Blog

A portfolio and blog with a publishing workflow built into Django admin. Create or edit posts in the admin, store them in SQLite through the Django ORM, and render published content on the public site with Django templates and Tailwind CSS.

## Try the publishing workflow

1. Start the app using the setup below and sign in at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
2. Under **Blog posts**, add a post with a title, body, and image. Save it as a draft.
3. Set its status to **Published** and save. Open the [blog index](http://127.0.0.1:8000/blog/) and select the post.

The public index and detail routes both filter for published posts. The detail view returns a 404 for drafts. See the [admin configuration](myapp/admin.py), [models](myapp/models.py), and [public views](myapp/views.py).

## Run locally

```bash
git clone https://github.com/Kylin-Ace/Kylin-Portfolio.git
cd Kylin-Portfolio
python -m venv .venv
```

Activate with `source .venv/bin/activate` on macOS or Linux, or `.venv\Scripts\Activate.ps1` in Windows PowerShell. Then run:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). These settings are for local development.

## Tests

Run `python manage.py test` to check blog visibility for published posts and drafts.
