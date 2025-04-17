# API for IS-BAIKAL
The API of a web application for analyzing the Baikal natural area using satellite data.

## Stack
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [postgreSQL](https://www.postgresql.org/)
- [uvicorn](https://www.uvicorn.org/) - for development
- [gunicorn](https://gunicorn.org/) + uvicorn workers - for production

## Start Development Server:
- uvicorn main:app
## Start Production Server:
- gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 