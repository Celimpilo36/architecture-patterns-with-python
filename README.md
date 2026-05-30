# Architecture Patterns with Python 🏗️🐍

This repository contains implementations and explorations of architectural design patterns in Python, heavily inspired by Domain-Driven Design (DDD) and clean architecture principles. 

The goal of this project is to demonstrate how to build low-coupling, high-cohesion software components that remain highly testable and independent of external infrastructure frameworks.

---

## 🧩 Core Patterns Explored

This codebase moves away from traditional database-centric designs ("Active Record") and implements an architecture centered around a pure domain model:

* **Domain Model Pattern:** Capturing business rules in pure, framework-agnostic Python objects (Entities, Value Objects, and Aggregates).
* **Repository Pattern:** An abstraction over data storage that hides the complexities of SQLAlchemy/ORM mapping, treating the database like an in-memory collection.
* **Service Layer Pattern (Use Cases):** Defines the application's entry points and orchestrates the execution of business logic without leaking API or database implementation details.
* **Unit of Work (UoW) Pattern:** Maintains an atomic transaction boundary across multiple repositories, ensuring that data modifications either completely succeed or fail together.
* **Event-Driven Architecture:** Utilizing a Message Bus to handle domain events, decoupling side-effects (like sending emails or updating logs) from the main use case execution.

---

## 📁 Repository Structure

The layout follows a clean, layered architectural boundary:

```text
├── src/
│   ├── domain/             # Pure entities, aggregates, and business logic
│   ├── adapters/           # Database repositories, ORM maps, API clients (Infrastructure)
│   ├── service_layer/      # Handlers, services, and Unit of Work orchestrators
│   └── entrypoints/        # FastAPI / Flask controllers, CLI routes, or event consumers
└── tests/
    ├── unit/               # Testing domain logic and services with fake adapters
    ├── integration/        # Testing adapters against real databases (SQLite/Postgres)
    └── e2e/                # Testing full application entrypoints (HTTP requests)
