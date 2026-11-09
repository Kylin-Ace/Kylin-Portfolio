# Django Portfolio, Blog & Listings API

A portfolio and blog with a publishing workflow built into Django admin. Create or edit posts in the admin, store them in SQLite through the Django ORM, and render published content on the public site with Django templates and Tailwind CSS. The project also includes a sample marketplace API built with Django REST Framework.

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

To build the site’s Tailwind styles, run `npm ci` and then `npm run build` from the repository root. The API and Python tests run without Node.js.

## Marketplace listings API

A small API for managing your own marketplace listings. It uses sample data you create locally and runs on the same SQLite database as the blog.

| Method | Path | Action |
| --- | --- | --- |
| GET, POST | `/api/v1/listings/` | List your listings or create one |
| GET, PUT, PATCH, DELETE | `/api/v1/listings/<id>/` | Read, replace, update, or delete one of your listings |

After local setup, create a token for the user you made with `createsuperuser`. Run this from a second terminal with your virtual environment active while the server runs.

```bash
python manage.py drf_create_token YOUR_USERNAME
```

Replace `YOUR_LOCAL_TOKEN` with the token printed by that command.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/listings/ \
  -H "Authorization: Token YOUR_LOCAL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Desk lamp","price":"12.50"}'

curl http://127.0.0.1:8000/api/v1/listings/ \
  -H "Authorization: Token YOUR_LOCAL_TOKEN"
```

The [viewset](listings/views.py) assigns the owner from the authenticated request and scopes every lookup to that user. Another user's listing returns 404. The [serializer](listings/serializers.py) validates the title, price, and optional status. New listings default to `draft`; valid statuses are `draft`, `active`, and `archived`.

## Tests

Run `python manage.py test` to check blog publishing and API behavior, including unauthenticated requests, cross-account reads and writes, and invalid input.
