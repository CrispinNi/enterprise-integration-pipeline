package com.example.producer;

import org.springframework.stereotype.Service;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.scheduling.annotation.Scheduled;

import java.time.Instant;
import java.util.Map;
import java.util.UUID;
import java.util.HashMap;

@Service
public class CustomerProducer {

    private final RabbitTemplate rabbitTemplate;
    private final WebClient webClient;

    public CustomerProducer(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
        this.webClient = WebClient.create("http://crm-service:8000");
    }

    @Scheduled(fixedDelay = 60000)
    public void publishCustomers() {
        webClient.get()
            .uri("/customers")
            .retrieve()
            .bodyToFlux(Map.class)
            .retry(3)
            .doOnNext(customer -> {

                Map<String, Object> event = new HashMap<>(customer);

                event.put("eventId", UUID.randomUUID().toString());
                event.put("eventType", "customer.created");
                event.put("timestamp", Instant.now().toString());

                rabbitTemplate.convertAndSend(
                    "integration.exchange",
                    "customer.created",
                    event
                );
            })
            .subscribe();
    }
}
