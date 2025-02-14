# Sealy Chat 🦭

## Overview
Sealy is a encrypted real-time chat application built using Flask and Vue.js with a focus on security and privacy.

## Installation

## Prerequisites
- docker-compose

**Copy and rename `.env.example` to `.env`**
```bash
cp .env.example .env
```

**Insert a Flask & JWT secret key in `.env`**
```bash
FLASK_SECRET_KEY=your-flask-secret-key
JWT_SECRET_KEY=your-ywt-secret-key
```

**Build the application**
```bash
./build
```

**Run the Docker image**
```bash
docker-compose up -d
```
By default it runs on port 5000

## License
This project is licensed under the GNU Affero General Public License - see the [LICENSE](LICENSE) file for details.
