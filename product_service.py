from product_repository import ProductRepository


class ProductService:
    def __init__(self,repository:ProductRepository):
        self.repository=repository


    def get_product_id(self,product_id:int):
        product=self.repository.get_by_id(product_id)
        if product is None:
            raise ValueError("Produto não encontrado")
        return product
