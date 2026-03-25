# Restaurant-ChatGPT

 **Restaurant Menu & Ordering System (RMOS)** that replaces paper menus and coordinates ordering + kitchen + billing across multiple device types. It defines four primary actors: **Customer, Waiter, Chef, Supervisor** (Supervisor inherits waiter+chef capabilities)

## Sprint 1:

Deliver a working “happy path” where:

1. a waiter logs in and activates a table,
2. a customer browses the menu and places an order,
3. the waiter accepts it and sends items to the kitchen,
4. the chef accepts/rejects items and marks them ready,
5. the waiter is alerted and marks items delivered.


## How to run

1. **Docker installed** (Docker Desktop or Docker Engine) and working:

   * Run: `docker --version`
   * Run: `docker compose version` (or `docker-compose --version`)


2. Build and start everything:

   ```bash
   docker compose up --build
   ```

   (or `docker-compose up --build`)

3. Open the prototype UI:

   * Frontend:  http://172.18.0.1/
   
