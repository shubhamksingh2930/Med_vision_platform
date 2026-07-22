# This file contains why each thing is used or what choices affect our decision in selecting something.
## What things we required?
 * System Design: We will use hybrid of both monolith(85%) and microservice(15%) structure.

   ### Hybrid Monolith-Microservices Architecture

 ```text  
                                               Users
                                                │
                                          Load Balancer
                                                │
                                           API Gateway
                                                │
                                  ┌─────────────┴─────────────┐
                                  │                           │
                                  ▼                           ▼
                            Monolith App                 Microservices
                           (Most Features)          ┌────────────────┬────────────────┬
                                                    │                │                │         
                                                AI Service       Notification       Search

```
### Why Hybrid
** We selected a hybrid Monolith-Microservices model to demonstrate a balanced engineering approach—combining the straightforward deployment of a monolith with the targeted scalability of microservices. 
### Strategic Considerations
* **Target Audience & Traffic Patterns:** The platform is primarily designed for interns and NEET-PG aspirants preparing for exams, rather than primary hospital administration. Traffic is expected to peak during exam preparation cycles rather than maintaining a constant heavy load.
* **Cost Efficiency:** Maintaining core features within a monolith minimizes initial cloud infrastructure costs during the early deployment phase.
* **Future Scalability:** Decoupling resource-intensive modules (such as AI evaluations and search) ensures that if user adoption spikes, critical components can scale independently without requiring an expensive, full-scale infrastructure overhaul.
