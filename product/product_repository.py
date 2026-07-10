from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.orm import Session
from product.product_model import Products
from sqlalchemy import func, select
from sqlalchemy import text
class ProductRepository:
    def __init__(self, db:Session):
        self.db=db


    def get_by_id(self, product_id: int):
        return self.db.query(Products).filter(
            Products.id == product_id
        ).first()
    
    def get_product_active(self):
        return self.db.query(Products).filter(Products.ativo == True).first()
    

    def description_product(self, description: str):
        sql = text("""
                WITH parametros AS (
                        SELECT :busca AS busca
                    ),
                    termos_busca AS (
                        SELECT trim(unnest(string_to_array(lower(par.busca), ' '))) AS termo
                        FROM parametros par
                        WHERE par.busca IS NOT NULL 
                        AND par.busca != ''
                    ),
                    produtos_rankeados AS (
                        SELECT 
                            p.*,

                    embjatai.similarity(
                        lower(p.descricao)::text, 
                        lower(par.busca)::text
                    ) AS similaridade_frase,

                    embjatai.word_similarity(
                        lower(par.busca)::text, 
                        lower(p.descricao)::text
                    ) AS similaridade_palavra,

                    (
                        SELECT MAX(
                            embjatai.similarity(
                                lower(p.descricao)::text, 
                                ts.termo::text
                            )
                        )
                        FROM termos_busca ts
                    ) AS similaridade_termos

                FROM embjatai.produto p
                CROSS JOIN parametros par
                WHERE par.busca IS NOT NULL
                AND par.busca != ''

                AND (
                    embjatai.similarity(
                        lower(p.descricao)::text, 
                        lower(par.busca)::text
                    ) > 0.15

                    OR embjatai.word_similarity(
                        lower(par.busca)::text, 
                        lower(p.descricao)::text
                    ) > 0.25

                    OR EXISTS (
                        SELECT 1
                        FROM termos_busca ts
                        WHERE embjatai.similarity(
                            lower(p.descricao)::text, 
                            ts.termo::text
                        ) > 0.15
                        OR lower(p.descricao) ILIKE '%' || ts.termo || '%'
                    )
                )
                )
                SELECT *
                FROM produtos_rankeados
                ORDER BY
                (
                    COALESCE(similaridade_frase, 0) * 0.60 +
                    COALESCE(similaridade_termos, 0) * 0.30 +
                    COALESCE(similaridade_palavra, 0) * 0.10
                ) DESC,
                descricao ASC
                LIMIT 50;
            """)

        try:
            result = self.db.execute(
                sql,
                {"busca": description}
            ).mappings().all()
            print(len(result))
            if not result:
                raise ValueError("Não encontrei produtos com esse nome.")

            return [
                {
                    "id": product["id"],
                    "codigo": product["codigo"],
                    "descricao": product["descricao"],
                    "valor": float(product["valor"]),
                    "unidade": product["unidade"],
                }
                for product in result
            ]                 
            
        except DBAPIError as e:
            print("Erro PostgreSQL:")
            print(e.orig)
            raise
        except Exception as e:
            print(type(e))
            print(e)
            raise
                
           

            # for product in result:
            #     resultado.append({
            #         "id": product.id,
            #         "codigo": product.codigo,
            #         "descricao": product.descricao,
            #         "valor":product.valor, 
            #         "unidade":product.unidade
                    
            #     })



        
      


   