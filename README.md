# Introduction

## Why Do Our Designs Go Wrong

1. **Chaos in software systems**  
   * Chaotic software often suffers from duplicated functionality and lack of clear structure.  

2. **API handlers with domain knowledge or business logic**  

3. **Tight coupling**  
   * When everything is coupled to everything else, modifying any part of the system becomes risky and error‑prone.  
   * This is known as the **Big Ball of Mud** anti‑pattern.  
   * Fortunately, there are straightforward techniques we can use to avoid this.  

---

# Encapsulation and Abstraction

## Encapsulation

Encapsulation is the mechanism of bundling data and the methods/functions that operate on that data into a single unit (such as a class) and controlling access to it to ensure security and data integrity.  

It simplifies system behavior by hiding internal details and exposing only what’s necessary. We encapsulate behavior by identifying a task that should be handled by a well‑defined object.  

## Abstraction

Abstraction is the process of showing only the essential features of an object while hiding its internal implementation details.  

Using abstraction to encapsulate behavior is a powerful tool for making code more **reusable**, easier to test, and simpler to maintain.  

---

# Layering

* Encapsulation and abstraction help us by hiding details and protecting the consistency of our data.  
* We must pay attention to how our objects and functions interact with one another.  
* When a function, module, or object uses another, we say it **depends** on that module, function, or object.  
* These dependencies form a kind of network or map.  
* We can avoid the “Big Ball of Mud” by using layered architecture, such as the **Three‑Layered Architecture**.  
* There are rules that need to be followed to achieve a proper layered design.  
* In this repository, we are going to use the **Dependency Inversion Principle (DIP)**.  

---

# The Dependency Inversion Principle (DIP)

The Dependency Inversion Principle states that our business code should not depend on technical details; instead, both should depend on abstractions.  

1. Higher‑level modules should not depend on low‑level modules. Both should depend on **abstractions**.  
2. Abstractions should not depend on details; instead, details should depend on abstractions.  

## Higher‑Level Modules

These are the high‑priority parts of the code that an organization really cares about. They include the functions, classes, and packages that deal with real‑world concepts.  

## Low‑Level Modules

These are less critical parts of the code that typically handle technical details rather than core business logic.  

**Note:** “Depends on” does not necessarily mean imports or calls. It refers more generally to the idea that one module knows about or requires another module.  
