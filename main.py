from fastapi import FastAPI
from product_controller import router as product_router

app = app = FastAPI(
    title="Consulta Produtos Embalagem Jatai API",
    description="API para gerenciamento das informações entre o banco de dados e o sistema.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Olá, FastAPI!"}

app.include_router(product_router)