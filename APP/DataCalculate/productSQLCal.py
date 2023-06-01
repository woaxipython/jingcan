from models.product import AtomModel


def DataSale(sales):
    sales_list = []
    for sale in sales:
        sale_dict = {}
        sale_dict["id"] = sale.id
        sale_dict["search_id"] = sale.search_id if sale.search_id else ""
        sale_dict["name"] = sale.name if sale.name else ""
        sale_dict["sale_name"] = sale.sale_name if sale.sale_name else ""
        sale_dict["code"] = sale.code if sale.code else ""
        sale_dict['cost'] = sale.cost if sale.cost else 0
        sale_dict["price"] = sale.price if sale.price else 0
        sale_dict["createtime"] = sale.createtime.strftime("%Y-%m-%d ")
        sale_dict['store'] = [{"id": store.id, "name": store.name} for store in sale.store if store]
        sale_dict["brand"] = sale.brand.name if sale.brand else ""
        sale_dict['atoms'] = [
            {"id": atom.id,
             "name": atom.name,
             "code": atom.code,
             "cost": atom.cost,
             "weight": atom.weight,
             "unit": atom.unit.name,
             "quantity": atom.quantity,
             }
            for atom in sale.atoms if atom.name]
        sale_dict["min_quantity"] = min([atom.quantity for atom in sale.atoms if atom]) if sale.atoms else 0

        sale_dict['weight'] = sum([atom.weight for atom in sale.atoms if atom])

        sales_list.append(sale_dict)
    return sales_list
