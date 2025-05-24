# OpenParlement

**OpenParlement** is providing a public API to access data related to the French Parliament. 
It aims to improve transparency, facilitate civic tech initiatives, and support anybody in accessing structured parliamentary information.

## ⚠️ Disclaimer

> **Work In Progress (WIP):** This API is currently under active development and is subject to change at any time.  

## 🚀 Features

- RESTful API to access deputies, laws, votes, political parties, and sessions. (WIP)
- Regularly updated data from official French parliamentary sources (https://data.assemblee-nationale.fr/).

## 📦 Tech Stack

- **Python 3.10+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database interaction
- **SQlite/MariaDB** 
## 📚 API Overview

Base URL: `https://api.openparlement.fr/` (WIP)

Example endpoints:
- `GET /deputies` – List all deputies
- `GET /deputies/<id>` – Get details of a deputy
- `GET /laws` – List laws and propositions
- `GET /votes` – Retrieve voting records
- `GET /parties` – List political parties
- `GET /sessions` – Parliamentary sessions

Detailed documentation is available at: [API Docs](https://api.openparlement.fr/apidocs) (WIP)

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

### Run the App

```bash
flask db upgrade
flask run
```

### Seed Database (optional)

```bash
python scripts/seed_data.py
```

## 🧪 Running Tests

```bash
pytest
```

## 📖 Contributing

We welcome contributions! Please submit pull requests or open issues for bugs, features, or suggestions.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

## 📄 License

OpenParlement is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](LICENSE) file for details.

## 🌍 Acknowledgements

- Assemblée Nationale open data (https://data.assemblee-nationale.fr/)