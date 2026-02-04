[![CI Pipeline](https://github.com/CrispinNi/enterprise-integration-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/CrispinNi/enterprise-integration-pipeline/actions/workflows/ci.yml)

# 🚀 System Integration Pipeline

## 🧩 Overview
This project demonstrates a production-grade, event-driven integration pipeline built with Spring Boot (Java) and Python, designed to synchronize data across multiple systems in a scalable and reliable way. It simulates real-world enterprise integration scenarios where independent services exchange data asynchronously using a message broker.
The system ingests customer and inventory data, publishes events via RabbitMQ, processes them through a Python analytics consumer, and exposes consolidated analytics via REST APIs. The architecture is containerized using Docker Compose, making it easy to run, extend, scale, and suitable for high-throughput data pipelines, microservice ecosystems, and enterprise system integrations.

## 🚀 Instructions to Run the System
### 1️⃣ Prerequisites

🐳Ensure you have the following installed:

 - Docker
 - Docker Compose

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/event-driven-analytics-pipeline.git
cd event-driven-analytics-pipeline
```

### 3️⃣ Start All Services

`docker-compose up --build`

*run it in the root* 


This will start:
 - RabbitMQ
 - CRM Service
 - Inventory Service
 - Analytics Consumer
 - Analytics API

### 4️⃣ Verify Services
##### Health Service	Endpoint:

 - CRM	http://localhost:8001/health

 - Inventory	http://localhost:8002/health

 - Analytics API	http://localhost:8003/health

 - RabbitMQ UI	http://localhost:15672

##### RabbitMQ credentials

 - username: guest
 - password: guest

##### Service Endpoint:

 - CRM	http://localhost:8001/customers

 - Inventory	http://localhost:8002/products

 - Analytics API	http://localhost:8003/analytics/data
 

### 5️⃣ Trigger Events

CRM automatically publishes customer.created

Inventory periodically publishes inventory.updated

Analytics Consumer merges data and posts to Analytics API

Check logs to observe real-time event flow.


## 🧠 Architectural Decisions

The system was designed using an event-driven, asynchronous architecture to address the challenges of integrating multiple independent systems while maintaining scalability and fault tolerance. Rather than relying on synchronous API-to-API communication, RabbitMQ was introduced as a message broker to decouple producers from consumers. This choice ensures that services can operate independently without blocking or cascading failures when one system is slow or unavailable.

This architecture scales naturally by allowing producers and consumers to be horizontally scaled without code changes. As message volume increases, additional consumer instances can be added to process events in parallel. Failure scenarios are handled safely through message buffering, retries, idempotent processing, and explicit acknowledgements ensuring that messages are not lost or processed multiple times even during crashes or restarts.

### 🏗️ Architecture Diagram

![ARCH](/images/Arch.png)


### ⚙️ Technologies Used

| Layer            | Technology                |
| ---------------- | ------------------------- |
| Messaging        | RabbitMQ (Topic Exchange) |
| Producers        | Spring Boot (Java)        |
| Consumer         | Python (Pika)             |
| Analytics API    | FastAPI                   |
| HTTP Client      | Spring WebClient          |
| Containerization | Docker & Docker Compose   |
| Communication    | JSON over AMQP & REST     |


## 📈 Scalability & Reliability Strategies

Scalability is achieved through asynchronous messaging, allowing producers to send events quickly without waiting for downstream processing. Consumers can be scaled horizontally to handle higher loads, enabling the system to process 10,000+ records per hour reliably. Reliability is ensured through retries, timeouts, and idempotency mechanisms that prevent duplicate processing. RabbitMQ provides buffering and back-pressure handling, ensuring the system remains stable even when downstream services are temporarily unavailable.


## 🔁 Spring Boot + Python Integration

The integration between Java and Python components is achieved exclusively through JSON messages transmitted via RabbitMQ. This language-agnostic communication model allows each component to be implemented using the most appropriate technology without introducing tight coupling. The same architecture could be implemented entirely in Java if required; however, the current design demonstrates how polyglot systems can coexist cleanly using standardized messaging protocols.
Asynchronous processing was intentionally selected to improve throughput, resilience, and operational flexibility, particularly in environments with diversified technologies.

## 🏆 Sample output

Successful integration is demonstrated through runtime logs, API responses, and message payloads. Spring Boot producers publish inventory and customer events to the message broker, which are consumed by a Python analytics service. The consumer aggregates the data and successfully posts it to the analytics API, confirmed by HTTP 200 responses in the service logs. Additionally, the analytics endpoint can be invoked directly via Postman to verify availability and correct request handling. 

Here is some Output:

### </> Terminal / Docker Logs 

The is the the Image show the output in my terminal, it show a positive answer:
![refernce](/images/terminal.png)
If you already clone this project and you run 
`docker-compose up --build`
you will get the same also in your terminal 

### Post 

Here is the image of the output comes from after testing the endpoint of analytics API in Postman.
Endpoint:http://localhost:8003/analytics/data

![Postman](/images/postman1.png)

Remember this is POST Methos. So you have to provide JSON data, for example:
```JSON
{
  "customer": {
    "id": "c1",
    "name": "Mohamed",
    "email": "Mohamed@test.com"
  },
  "products": [
    { "id": "P132", "name": "Keyboard", "stock": 01 },
    { "id": "p23", "name": "Ipad", "stock": 52 }
  ]
}

``` 

## 🧩 Message Flow & Integration Pipeline

The system follows an event-driven pipeline where Java-based producers fetch data
from upstream services and publish domain events to RabbitMQ. A Python consumer
subscribes to these events, performs idempotent processing, and forwards enriched
data to the Analytics service.

### Message Processing Flow Diagram
![Reference](/images/Message-flow-pipeline.png)

### Failure, Retry & Idempotency Flow
![Reference](/images/Failure,%20Retry-Idempotency-Flow.png)

#### Conclusion The implemented integration pipeline demonstrates a robust and scalable approach to enterprise systems integration. By combining Spring Boot producers, RabbitMQ messaging, and Python consumers, the system achieves high throughput, fault tolerance, and extensibility.


