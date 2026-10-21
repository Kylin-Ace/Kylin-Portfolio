# Kylin Ace — Developer Portfolio

A server-rendered Django portfolio with a Tailwind CSS frontend, editable project and blog content, and a contact inbox in Django admin.

## Run locally

Requirements: Python 3.11+ and Node.js 20+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
npm ci
npm run build
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Use `/admin/` to manage projects, published posts, profile content, and contact messages. The local development setup uses SQLite and stores uploads in `media/`.

For frontend development, run `npm run watch` in a second terminal.

## Deploy to Vercel

Vercel runs Django as a Python Function, serves collected and content-hashed static assets through its CDN, and uses the build script in `pyproject.toml` to compile Tailwind. A production deployment also needs a persistent PostgreSQL database and S3-compatible object storage for uploaded images; a Vercel Function's local disk is not persistent.

1. Push this project to a Git repository and import it into Vercel. Keep the repository root as the project root.
2. Create a managed PostgreSQL database and an S3-compatible media bucket. Neon (using its pooled connection URL) and Cloudflare R2 are reasonable starting options; configure the bucket for public read access or attach a public custom domain so portfolio images can be displayed.
3. Add these environment variables in the Vercel project settings for **Production, Preview, and Development** as appropriate:

   | Variable | Value |
   | --- | --- |
   | `DJANGO_SECRET_KEY` | A unique, random production secret. Generate one with `python -c "import secrets; print(secrets.token_urlsafe(50))"`. |
   | `DATABASE_URL` | The PostgreSQL connection URL from your database provider. |
   | `DJANGO_ALLOWED_HOSTS` | Optional comma-separated custom domains. Vercel's `VERCEL_URL` and `VERCEL_PROJECT_PRODUCTION_URL` hostnames are allowed automatically. |
   | `CSRF_TRUSTED_ORIGINS` | Comma-separated full origins for custom domains, including `https://`, for example `https://example.com,https://www.example.com`. |
   | `AWS_STORAGE_BUCKET_NAME` | The bucket name used for uploaded media. |
   | `AWS_ACCESS_KEY_ID` | Storage access key. |
   | `AWS_SECRET_ACCESS_KEY` | Storage secret key. |
   | `AWS_S3_ENDPOINT_URL` | S3-compatible endpoint; for R2, use `https://<account-id>.r2.cloudflarestorage.com`. |
   | `AWS_S3_REGION_NAME` | Provider region; use `auto` for R2. |
   | `AWS_S3_CUSTOM_DOMAIN` | Optional public media hostname, without `https://`. |

   Leave `DJANGO_DEBUG` unset in Vercel. Production mode is selected automatically there.
4. Deploy. Vercel detects `manage.py` and `config.wsgi.application`; its Django integration runs `collectstatic` and serves files under `/static/`. The configured build script runs `npm run build` first to create the Tailwind stylesheet.
5. Apply migrations against the production database before relying on the site. Run `python manage.py migrate` from an environment configured with the production `DATABASE_URL`, `DJANGO_SECRET_KEY`, and media-storage variables.
6. If you imported existing users as described below, sign in with the imported admin account. Otherwise, create the production admin account with `python manage.py createsuperuser` from that same configured environment.

Contact form submissions are saved in the database and reviewed under **Contact messages** in `/admin/`. Email notifications are not configured; add an email provider later if you want new messages forwarded to your inbox.

Never commit `.env` files, database credentials, or production secret keys. `.env.example` is a reference; Django does not load `.env` files automatically, so set local variables in your shell or your development environment.

### Preserve existing content and uploads

The local SQLite database and `media/` directory are excluded from Git. Back them up before deployment. First export records while the app is still pointed at the existing SQLite database; then set the production environment variables and import them:

```powershell
# Keep DATABASE_URL unset while exporting from the local SQLite database.
python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --indent 2 > data.json

# Set DATABASE_URL, DJANGO_SECRET_KEY, and the media-storage variables to their
# production values before running these commands:
python manage.py migrate
python manage.py loaddata data.json
```

Move files from the local `media/` directory to the corresponding object-storage bucket before switching traffic. Preserve the relative paths (for example `projects/`, `blog/`, and `about/`) so existing image fields continue to resolve. Do not delete the local database or upload files until you have verified the production site and backups.

## Project structure

- `config/` — Django settings, URL configuration, and WSGI entry point.
- `myapp/` — portfolio pages, models, admin, templates, and tests.
- `theme/` — shared templates and Tailwind source CSS.
- `static/` — project static assets and the generated Tailwind output.
