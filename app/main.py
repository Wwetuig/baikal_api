from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1 import users, satellite_data_files, ground_data_files
from api.v1 import external_resources
from api.v1 import publications
from api.v1 import about_project

# Создание FastAPI приложения
app = FastAPI()

#CORS Configuring
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Access-Control-Allow-Origin", "Authorization"],
)

# Подключаем роутеры
app.include_router(users.user_router, prefix="/api/v1/users", tags=["Users"])

app.include_router(satellite_data_files.satellite_data_firstSD_router,
                   prefix="/api/v1/files/satellite_data", tags=["Satellite data (Landsat)"])
app.include_router(satellite_data_files.satellite_data_secondSD_router,
                   prefix="/api/v1/files/satellite_data", tags=["Satellite data (Monthly Avg)"])
app.include_router(satellite_data_files.satellite_data_thirdSD_router,
                   prefix="/api/v1/files/satellite_data", tags=["Satellite data (Monthly Avg Many Years)"])
app.include_router(satellite_data_files.satellite_data_router,
                   prefix="/api/v1/files/satellite_data", tags=["Satellite data (general)"])

app.include_router(ground_data_files.ground_data_router,
                   prefix="/api/v1/files/ground_data", tags=["Ground data"])

app.include_router(publications.publications_router,
                   prefix="/api/v1/publications", tags=["Publications"])

app.include_router(external_resources.external_resources_router,
                   prefix="/api/v1/external_resources", tags=["External Resources"])

app.include_router(about_project.about_project_router,
                   prefix="/api/v1/about", tags=["About Project"])


@app.get("/")
async def read_root():
    return {"framework": "FastAPI",
            "message": "The API for BAIKAL Information System"
            }


