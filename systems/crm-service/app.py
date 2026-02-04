from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List
#from lxml import etree

app = FastAPI(title="CRM Service")

class Customer(BaseModel):
    id: str
    name: str
    email: str

CUSTOMERS = [
    Customer(id="c1", name="crispin", email="crispin@test.com"),
    Customer(id="c2", name="luck", email="luck@test.com"),
    Customer(id="c3", name="frank", email="frank@test.com"),
    Customer(id="c4", name="james", email="james@test.com"),
    Customer(id="c5", name="david", email="david@test.com"),
    Customer(id="c5", name="Rugaju", email="Rugaju@test.com"),
]

@app.get("/customers", response_model=List[Customer])
def get_customers():
    return CUSTOMERS

@app.post("/customers")
def post_customers(customer: Customer):
    CUSTOMERS.append(customer)
    return {"message": "Customer added successfully"}

"""@app.post("/soap/customers")
async def add_customer_soap(request: Request):
    body = await request.body()

    # Parse SOAP XML
    root = etree.fromstring(body)
    ns = {
        "soap": "http://schemas.xmlsoap.org/soap/envelope/"
    }

    name = root.xpath("//name/text()")
    email = root.xpath("//email/text()")

    name = name[0] if name else "Unknown"
    email = email[0] if email else "unknown@test.com"

    new_customer = {
        "id": len(Customer) + 1,
        "name": name,
        "email": email
    }
    Customer.append(new_customer)

    # SOAP Response
    response_xml = f"
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <AddCustomerResponse>
          <status>SUCCESS</status>
          <customerId>{new_customer['id']}</customerId>
        </AddCustomerResponse>
      </soap:Body>
    </soap:Envelope>
    

    return Response(content=response_xml, media_type="text/xml")"""


@app.get("/health")
def health():
    return {"status": "ok",
            "service": "crm-service"
            }