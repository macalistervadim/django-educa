# Welcome to the Django Educa Project Documentation 🎓

![Django](https://img.shields.io/badge/Django-5-green)
![Python](https://img.shields.io/badge/Python|3.12-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Linters](https://github.com/macalistervadim/django-educa/actions/workflows/linters.yml/badge.svg)

**Django Educa** is an educational platform built with Django. It allows you to create courses, modules, and learning content. The project includes models for managing courses, modules, text, video, and file-based content.

---

## Features ✨

- **Content Management System (CMS):** A powerful CMS for managing courses, modules, and content.
- **Admin Panel:** Built-in Django admin panel for convenient content management.
- **Course Creation:** Create and manage courses with titles, descriptions, and overviews.
- **Module Management:** Organize courses into modules for structured learning.
- **Polymorphic Content:** Support for various content types, including text, video, and files.
- **User Authentication:** Secure user authentication and authorization system.
- **Docker Integration:** Easy setup and deployment using Docker.
- **Workflow Automation:** Use Poetry for dependency management and automation.
- **Code Quality:** Integration with Black, Flake8, and MyPy for clean and maintainable code.

---

## Technologies ⚙️

The project is developed using modern technologies:

- **Django 5** — a web framework for Python that ensures a fast start and flexibility.
- **Python 3.12** — the primary programming language.
- **PostgreSQL** — a database management system for storing information.
- **Docker** — for containerizing the application and simplifying the deployment process.
- **Poetry** — a tool for dependency management and packaging Python projects.
- **Gunicorn** — a high-performance WSGI server for running Django applications in production.
- **Nginx** — a web server for handling requests, proxying them to Gunicorn, and ensuring security with SSL.

---

## Installation and Setup

To install and run the application on your server, follow the [instructions](installation.md).

---

## ER Diagram 📊

Below is the ER diagram of the project's database:

![docs/ER.png](../ER.png)

---

## License 📜

This project is distributed under the MIT license. For more details, see the [LICENSE](../../LICENCE.md) file.

---

## Screenshots 📸

**Homepage**

![docs/images/main_page.png](../images/main_page.png)

**Chat**

![docs/images/chat.png](../images/chat.png)

**Course View**

![docs/images/view_course.png](../images/view_course.png)

**Course Management**

![docs/images/manage_course.png](../images/manage_course.png)

**Sign In**

![docs/images/sign_in.png](../images/sign_in.png)

---

## Acknowledgments 🙏

Thank you to everyone who supports this project!