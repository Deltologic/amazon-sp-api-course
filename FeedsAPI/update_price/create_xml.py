class ProductToReprice:
    def __init__(self, sku: str, price: str, currency: str):
        self.sku = sku
        self.price = price
        self.currency = currency


feed_base_content = """<?xml version = "1.0" encoding = "utf-8"?>
<AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
 <Header>
    <DocumentVersion>1.01</DocumentVersion>
    <MerchantIdentifier>{{seller_id}}</MerchantIdentifier>
  </Header>
  <MessageType>Price</MessageType>
  {{products_to_reprice}}
</AmazonEnvelope>
"""


def create_xml_product_to_reprice(id: str, price_feed: ProductToReprice):
    return f"""
    <Message>
      <MessageID>{id}</MessageID>
      <OperationType>Update</OperationType>
      <Price>
        <SKU>{price_feed.sku}</SKU>
        <StandardPrice currency="{price_feed.currency}">{float(price_feed.price):.2f}</StandardPrice>
      </Price>
    </Message>"""


def create_xml(seller_id: str, products_to_reprice: list[ProductToReprice]):
    products_to_reprice_xml = [
        create_xml_product_to_reprice(
            str(index + 1), product)
        for index, product in enumerate(products_to_reprice)
    ]
    products_to_reprice = '\n'.join(products_to_reprice_xml)
    return feed_base_content.replace('{{seller_id}}', seller_id).replace('{{products_to_reprice}}', products_to_reprice)
