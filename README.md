## Django Educa 🎓

![Django](https://img.shields.io/badge/Django-5-green)
![Python](https://img.shields.io/badge/Python|3.12-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Linters](https://github.com/macalistervadim/django-educa/actions/workflows/linters.yml/badge.svg)

**Django Educa** is an educational platform built with Django. It allows you to create courses, modules, and content for learning. The project includes models for managing courses, modules, text, video, and file content.

---

## Table of Contents 📚

- [Features](#features-)
- [Installation and Setup](#installation-and-setup-)
  - [Requirements](#requirements)
  - [Docker Setup](#docker-setup)
  - [Environment Configuration](#environment-configuration-)
  - [Database](#database-)
  - [Static Files](#static-files-)
- [ER Diagram](#er-diagram-)
- [License](#license-)
- [Contributing](#contributing-)

---

## Features ✨

- **Content Management System (CMS):** A powerful CMS for managing courses, modules, and content.
- **Admin Panel:** Built-in Django admin panel for easy content management.
- **Course Creation:** Create and manage courses with titles, descriptions, and overviews.
- **Module Management:** Organize courses into modules for structured learning.
- **Polymorphic Content:** Supports various content types, including text, video, and files.
- **User Authentication:** Secure user authentication and authorization system.
- **Docker Integration:** Easy setup and deployment using Docker.
- **Automated Workflow:** Uses Poetry for dependency management and automation.
- **Code Quality:** Integrated with Black, Flake8, and MyPy for clean and maintainable code.

---

## Technologies ⚙️

The project was developed using modern technologies:

- **Django 5** — a web application framework for Python, providing a quick start and flexibility.
- **Python 3.12** — the main programming language.
- **PostgreSQL** — a database management system used for storing information.
- **Docker** — for containerizing the application and simplifying the deployment process.
- **Poetry** — a tool for dependency management and packaging Python projects.
- **Gunicorn** — a high-performance WSGI server for running the Django application in a production environment.
- **Nginx** — a web server for handling requests, proxying them to Gunicorn, and ensuring security with SSL.

---

## Installation

To install the application and run it on your server, follow the [instructions](docs/START.md)

---

## ER Diagram 📊

Below is the ER diagram of the project's database:

![docs/ER.png](docs/ER.png)

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENCE.md) file for details.

---

## Screenshots 📸

**Home Page**

[Home Page]

**Course Page**

[Course Page]

---

## Acknowledgments 🙏

Thanks to everyone who supports this project!
