from product_repository import ProductRepository


class ProductService:
    def __init__(self,repository:ProductRepository):
        self.repository=repository


    def get_product_id(self,product_id:int):
        product=self.repository.get_by_id(product_id)
        if product is None:
            raise ValueError("Produto não encontrado")
        return product


    def get_product_active(self):
        product_active=self.repository.get_product_active()
        if product_active is None: 
            raise ValueError("Produto ativo não encontrado.")
        return product_active
    

    def get_description_product(self,description:str):
        product_found= self.repository.description_product(description)
        return product_found