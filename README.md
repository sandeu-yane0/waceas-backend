# WACEAS Backend — FastAPI + PostgreSQL + Cloudinary

## Stack
- FastAPI (Python)
- PostgreSQL (Railway)
- Cloudinary (stockage images permanent)

## Installation locale

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

pip install -r requirements.txt
copy .env.example .env      # puis éditez .env
uvicorn app.main:app --reload
```

→ API sur http://localhost:8000
→ Docs sur http://localhost:8000/api/docs

## Variables d'environnement (.env)

| Variable | Description |
|----------|-------------|
| DATABASE_URL | URL PostgreSQL Railway |
| SECRET_KEY | Clé JWT secrète (min 32 chars) |
| FIRST_ADMIN_EMAIL | Email du premier admin |
| FIRST_ADMIN_PASSWORD | Mot de passe du premier admin |
| CLOUDINARY_CLOUD_NAME | Depuis dashboard Cloudinary |
| CLOUDINARY_API_KEY | Depuis dashboard Cloudinary |
| CLOUDINARY_API_SECRET | Depuis dashboard Cloudinary |
| ALLOWED_ORIGINS | URLs autorisées (CORS) |

## Déploiement Railway (étapes)

1. Créez un compte sur https://railway.app
2. New Project → Deploy from GitHub
3. Ajoutez un service PostgreSQL → copiez DATABASE_URL
4. Ajoutez toutes les variables d'environnement
5. Le déploiement est automatique

## Identifiants admin par défaut
Email    : admin@waceas.com
Password : WaceasAdmin2026!
⚠️ Changez-les dès le premier login !
