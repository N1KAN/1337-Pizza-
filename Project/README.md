# **1337 Pizza** - Pizza Delivery for Your *Nerdy* Needs

**1337 Pizza** is a pizza delivery company, that has specialized on the needs of nerds.
The unique selling propositions of **1337 Pizza** compared with their competitors are: 
- 24/7 pizza delivery; ***you need it; we deliver it***
- Any exotic pizza composition is possible; ***anything goes***
- Pizza can be ordered hot or cold; ***we don't judge***
- Orders can be placed through an API; ***talk API to us, baby***


## Project Overview
This repository contains all development artifacts related to the backend service of the **1337 Pizza**-delivery. It exposes an API endpoints that can be used by front-end applications. For this repository, however, front-end applications are out of scope. They may be developed by other teams.


## Folder Structure of this Repository
The following is a brief description of the folder structure of this project:
- **app** - service's source code
- **doc** - all documentation of the project - [entrypoint](doc/README.md)
- **infra** - all infrastructure artifacts
- **test** - all tests 


## Lab. 7: Preparation

### INVEST Criteria for User Stories

- **I** – *Independent*: Can be developed and delivered separately.
- **N** – *Negotiable*: Not a contract; flexible for discussion.
- **V** – *Valuable*: Delivers value to the user or customer.
- **E** – *Estimable*: Can be estimated for effort and time.
- **S** – *Small*: Sized appropriately for implementation in a sprint.
- **T** – *Testable*: Has clear acceptance criteria to verify completion.

### Userstories:
Customer Feedback:
Fortunately, our store is doing great. More and more pizzas are ordered. Therefore, we use your backend very intensively by now. Because so many orders come in at the same time, we often loose track of which orders are currently being prepared. We can only display all orders and cannot distinguish which orders are currently being processed or being still open. Somehow we should be able to define what status an order currently has. You can see the problem also in the web-application frontend: if there are many orders, we need to scroll and it gets pretty inconvenient.

==> Problem: **Web-application not our project**

==> Diffenenciate between  currently processed or still open 

==> Definie the Status of the order 

### Userstory 1:
#### Card
**As** a chef, **I want** to see a diffrence between processed and still open **so that** I can see which orders are still open and which are being processed.
#### Conversation:
- Better diffenciation between transmitted, preparing, in delivery and completed by adding open (not already transmitted ?)

#### Confirmation:
- [ ] new order status added
- [ ] can be set or changed 
### Userstory 2:
#### Card
**As** a chef **I want** to update the status of the orders **so that** I can track the progess of the Orders.
#### Conversation:
- Make the new status acessable via API (frontend)
#### Confirmation:
- [ ] Added API endpoint


## Lab. 8 Preparation
### Userstory

#### Card  
**As** a shop owner **I want** to configure pizzas with different sauces **so that** I can expand my pizza offerings.

#### Conversation:
- Tomato sauce is the default  
- Additional sauces can be added via API  
- Sauce should be visible in the order details

#### Confirmation:
- [ ] Sauce can be selected for each pizza  
- [ ] Tomato sauce is selected by default  
- [ ] New sauces can be added via API  
- [ ] Selected sauce is shown in order and kitchen views

