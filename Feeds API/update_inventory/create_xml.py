class ProductInventoryChange:
    def __init__(self, sku: str, quantity: str):
        self.sku = sku
        self.quantity = quantity


feed_base_content = """<?xml version = "1.0" encoding = "utf-8"?>
<AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
 <Header>
    <DocumentVersion>1.01</DocumentVersion>
    <MerchantIdentifier>{{seller_id}}</MerchantIdentifier>
  </Header>
  <MessageType>Inventory</MessageType>
  {{product_inventory_changes}}
</AmazonEnvelope >
"""


def create_xml_product_to_reprice(id: str, inventory_feed: ProductInventoryChange):
    return f"""
<Message>
      <MessageID>{id}</MessageID>
      <OperationType>Update</OperationType>
      <Inventory>
        <SKU>{inventory_feed.sku}</SKU>
        <Quantity>{inventory_feed.quantity}</Quantity>
      </Inventory>
    </Message>"""


def create_xml(seller_id: str, inventory_changes: list[ProductInventoryChange]):
    inventory_changes_xml = [
        create_xml_product_to_reprice(
            str(index + 1), inventory_change)
        for index, inventory_change in enumerate(inventory_changes)
    ]
    inventory_changes = '\n'.join(inventory_changes_xml)
    return feed_base_content.replace('{{seller_id}}', seller_id).replace('{{product_inventory_changes}}', inventory_changes)
