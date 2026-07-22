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
