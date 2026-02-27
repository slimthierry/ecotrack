# EcoTrack

Application de suivi d'empreinte carbone avec gamification. Enregistrez vos activites quotidiennes, suivez vos emissions CO2, participez a des challenges et debloquez des achievements.

## Stack technique

- **Backend**: FastAPI + PostgreSQL + Redis + Celery
- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **Infrastructure**: Docker Compose

## Demarrage rapide

### Prerequis

- Docker & Docker Compose
- Node.js >= 20
- pnpm >= 9

### Backend

```bash
docker compose up -d
```

Services disponibles :
- API: http://localhost:38000
- Adminer (DB): http://localhost:38080

### Frontend

```bash
pnpm install
pnpm dev:web
```

Application web: http://localhost:3100

## Architecture

```
ecotrack/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/v1/         # Endpoints REST
│   │   ├── models/         # Modeles SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Logique metier
│   │   ├── tasks/          # Taches Celery
│   │   ├── config/         # Configuration
│   │   ├── core/           # Securite, exceptions
│   │   └── utils/          # Utilitaires
│   └── tests/              # Tests pytest
├── apps/
│   └── web/                # Application React (Vite)
├── packages/
│   ├── api-client/         # Client Axios + hooks React Query
│   ├── types/              # Types TypeScript partages
│   ├── ui/                 # Composants React reutilisables
│   └── utils/              # Fonctions utilitaires
└── docker-compose.yml
```

## API Endpoints

| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/auth/register | Inscription |
| POST | /api/v1/auth/login | Connexion |
| GET | /api/v1/auth/me | Profil utilisateur |
| POST | /api/v1/activities | Creer une activite |
| GET | /api/v1/activities | Lister les activites |
| GET | /api/v1/activities/summary | Resume des activites |
| DELETE | /api/v1/activities/{id} | Supprimer une activite |
| GET | /api/v1/challenges | Challenges actifs |
| POST | /api/v1/challenges/join | Rejoindre un challenge |
| GET | /api/v1/challenges/my-challenges | Mes challenges |
| GET | /api/v1/challenges/leaderboard/{id} | Classement |
| GET | /api/v1/achievements | Tous les achievements |
| GET | /api/v1/achievements/my-achievements | Mes achievements |
| GET | /api/v1/dashboard/overview | Vue d'ensemble |
| GET | /api/v1/dashboard/trends | Tendances |
| GET | /api/v1/dashboard/breakdown | Repartition |
| GET | /api/v1/dashboard/tips | Eco-conseils |
| GET | /api/v1/reports/weekly | Rapport hebdomadaire |
| GET | /api/v1/reports/monthly | Rapport mensuel |

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest
```
