# 1337 Pizza 🍕
> **A Highly Customizable, API-First Pizza Delivery Platform.**

## 📖 Project Overview
1337 Pizza is a conceptual delivery platform designed to handle highly customized and complex orders. This repository contains the development artifacts for the core backend service along with a custom-built Preact frontend. Developed as a comprehensive university software engineering project, this application applies agile methodologies and modern full-stack development practices to create a robust, scalable ordering system.

**Core Product Features (USPs):**
* **24/7 Availability:** System architecture designed for continuous, round-the-clock order processing.
* **Maximum Customizability:** The data model supports highly exotic pizza compositions and infinite ingredient combinations.
* **Flexible Order Parameters:** Capable of handling unconventional order variables (e.g., specifying delivery temperature).
* **API-First Approach:** A fully functional REST API allowing seamless integration with various frontend clients or third-party services.

## ✨ Features
* **Comprehensive Order Management:** Full lifecycle management of pizza orders via REST APIs, including a reactive frontend visualization (`OrderListComponent`).
* **Advanced Order Tracking:** Fine-grained status updates (`open`, `transmitted`, `preparing`, `in delivery`, `completed`) to streamline kitchen operations and improve order visibility.
* **Dynamic Sauce & Ingredient Configuration:** Expanding the menu by allowing custom bases (e.g., different sauces). New options can be added seamlessly via the API and are instantly reflected in the order details for both customers and chefs.
* **Inventory Management:** Real-time tracking and updating of toppings stock (`ToppingsListComponent`).
* **Component-Based UI:** A responsive Preact frontend featuring interactive dialogs, asynchronous loading states, and convenient "click-to-copy" UI elements.

## 🛠 Technologies
**Frontend:**
* **Preact:** A lightweight alternative to React for building the user interface.
* **TypeScript:** Ensuring static typing and enhanced code maintainability.
* **Custom State Management:** Context-API based state management with an asynchronous action queue.

**Backend & Database:**
* **Python:** Core backend logic.
* **SQLAlchemy & Alembic:** ORM and database schema migrations.
* **Mypy:** Static type checking to enforce code quality.

**DevOps & Tooling:**
* **Docker & Docker Compose:** Containerization for consistent development, testing, and deployment environments.
* **GitLab CI/CD:** Automated pipelines for building and testing the application.
* **SonarQube & Pytest:** Continuous code quality analysis, security checks, and automated backend testing.

## 📁 Project Structure
The repository follows a clean, separated monorepo architecture:
* `/app` - The backend service's source code (Python API, business logic).
* `/doc` - Comprehensive project documentation and architecture overview.
* `/infra` - Infrastructure artifacts and deployment configurations.
* `/tests` - Automated test suites for backend validation.
* `/pizza_1337_preact` - The Preact frontend source code (components, hooks, state).

## 🔄 Agile Development Process
This project was developed by a team of four using agile methodologies, heavily emphasizing structured Requirements Engineering:
* **Customer-Centric User Stories:** Unstructured feedback (e.g., chefs losing track of orders during peak hours) was systematically analyzed and translated into clean backend requirements.
* **INVEST Criteria:** All requirements were scoped as User Stories that are Independent, Negotiable, Valuable, Estimable, Small, and Testable.
* **Continuous Integration:** Every commit triggered CI pipelines with SonarQube quality gates to maintain a high standard of maintainability and security.
