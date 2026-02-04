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
public class InventoryProducer {

    private final RabbitTemplate rabbitTemplate;
    private final WebClient webClient;

    public InventoryProducer(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
        this.webClient = WebClient.create("http://inventory-service:8000");
    }

    @Scheduled(fixedDelay = 60000)
    public void publishInventory() {
        webClient.get()
            .uri("/products")
            .retrieve()
            .bodyToFlux(Map.class)
            .retry(3)
            .doOnNext(product -> {

                Map<String, Object> event = new HashMap<>();
                event.put("eventId", UUID.randomUUID().toString());
                event.put("eventType", "inventory.updated");
                event.put("timestamp", Instant.now().toString());
                event.putAll(product);

                rabbitTemplate.convertAndSend(
                    "integration.exchange",
                    "inventory.updated",
                    event
                );
            })
            .subscribe();
    }
}
