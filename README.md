# OpenParlement

**OpenParlement** is an open-source Flask application that provides a public API to access data related to the French Parliament. It aims to improve transparency, facilitate civic tech initiatives, and support developers, researchers, and journalists in accessing structured parliamentary information.

## 🚀 Features

- RESTful API to access deputies, laws, votes, political parties, and sessions.
- Real-time or regularly updated data from official French parliamentary sources.
- Filter, sort, and paginate results easily.
- Built with Flask, making it lightweight and easy to deploy.

## 📦 Tech Stack

- **Python 3.10+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database interaction
- **SQlite/MariaDB/PostgreSQL** 
## 📚 API Overview

Base URL: `https://api.openparlement.fr/` (WIP)

Example endpoints:
- `GET /deputies` – List all deputies
- `GET /deputies/<id>` – Get details of a deputy
- `GET /laws` – List laws and propositions
- `GET /votes` – Retrieve voting records
- `GET /parties` – List political parties
- `GET /sessions` – Parliamentary sessions

Detailed documentation is available at: [API Docs](https://api.openparlement.fr/docs) (WIP)

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (or another compatible database)

### Installation

```bash
git clone https://github.com/yourusername/openparlement.git
cd openparlement
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Configuration

Edit `.env` file to set database credentials and environment variables.

```dotenv
FLASK_DATABASE_URL=postgresql://user:password@localhost:543_
```