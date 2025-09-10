#  📘Freelancer Platform - API
The Freelancer Platform is a RESTful API built with Django REST Framework (DRF).
It provides a marketplace where sellers can offer freelance services and buyers can browse, order, and review those services.
The project uses JWT authentication with Djoser and includes interactive API documentation via Swagger & ReDoc.

## ✨ Features
- User authentication & role management (Buyer / Seller / Admin)
- Email verification for account activation
- Categories & service management
- Service images upload and management
- Reviews and ratings (1–10 scale)
- Order management with status tracking (Pending, In Progress, Completed, Canceled)
- Notifications for buyers and sellers
- API documentation with Swagger and ReDoc

## 🛠 Technologies Used
- Django – Backend framework
- Django REST Framework (DRF) – API development
- Djoser + JWT – Authentication
- drf-yasg – API documentation (Swagger & ReDoc)
- django-filter – Filtering support
- PostgreSQL / SQLite – Database
- Pillow – Image handling

## ⚙️ Installation
1. **Clone the repository:**
```bash
git clone https://github.com/abtahi2024
cd freelancer-platform
```
2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate 
Windows: venv\Scripts\activate
```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Documentation
Swagger documentation is available at:
```
http://127.0.0.1:8000/swagger/
```

ReDoc documentation is available at:
```
http://127.0.0.1:8000/redoc/
```

## Environment Variables
Create a `.env` file in the root directory and add the following:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
ALLOWED_HOSTS=*
EMAIL_HOST=your_email_host
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True
```

## Project Structure
```bash
freelancer-platform/
│── api/                # API root URLs
│── services/           # Services, categories, reviews, images
│── orders/             # Orders, order items, notifications
│── users/              # Custom user model & authentication
│── Freelancer_managents/   
│── requirements.txt
│── manage.py
│── README.md
````

## __📌 License__
This project is licensed under the MIT License.

### 🔐 Authentication (Djoser + JWT)
| Method | Endpoint                    | Description                      | Permission    |
| ------ | --------------------------- | -------------------------------- | ------------- |
| POST   | `/api/v1/auth/users/`       | Register new user (Buyer/Seller) | Public        |
| POST   | `/api/v1/auth/jwt/create/`  | Login and get JWT token          | Public        |
| POST   | `/api/v1/auth/jwt/refresh/` | Refresh JWT token                | Authenticated |
| POST   | `/api/v1/auth/jwt/verify/`  | Verify JWT token                 | Authenticated |
| GET    | `/api/v1/auth/users/me/`    | Get current user profile         | Authenticated |
| PATCH  | `/api/v1/auth/users/me/`    | Update own profile               | Authenticated |

## 👥 Users
| Method | Endpoint                   | Description                        | Permission |
| ------ | -------------------------- | ---------------------------------- | ---------- |
| GET    | `/api/v1/auth/users/`      | List all users                     | Admin      |
| GET    | `/api/v1/auth/users/{id}/` | Retrieve user details              | Admin      |
| PATCH  | `/api/v1/auth/users/{id}/` | Update user (role, verified, etc.) | Admin      |
| DELETE | `/api/v1/auth/users/{id}/` | Delete user                        | Admin      |

## 🗂 Categories
| Method | Endpoint                   | Description               | Permission |
| ------ | -------------------------- | ------------------------- | ---------- |
| GET    | `/api/v1/categories/`      | List all categories       | Public     |
| POST   | `/api/v1/categories/`      | Create a new category     | Admin      |
| GET    | `/api/v1/categories/{id}/` | Retrieve category details | Public     |
| PUT    | `/api/v1/categories/{id}/` | Update category           | Admin      |
| PATCH  | `/api/v1/categories/{id}/` | Partial update category   | Admin      |
| DELETE | `/api/v1/categories/{id}/` | Delete category           | Admin      |

## 💼 Services
| Method | Endpoint                 | Description                                                   | Permission   |
| ------ | ------------------------ | ------------------------------------------------------------- | ------------ |
| GET    | `/api/v1/services/`      | List all services (with search, filter, ordering, pagination) | Public       |
| POST   | `/api/v1/services/`      | Create a new service                                          | Seller/Admin |
| GET    | `/api/v1/services/{id}/` | Retrieve service details                                      | Public       |
| PUT    | `/api/v1/services/{id}/` | Update service                                                | Seller/Admin |
| PATCH  | `/api/v1/services/{id}/` | Partial update service                                        | Seller/Admin |
| DELETE | `/api/v1/services/{id}/` | Delete service                                                | Seller/Admin |

## 🖼 Service Images
| Method | Endpoint                                     | Description               | Permission   |
| ------ | -------------------------------------------- | ------------------------- | ------------ |
| GET    | `/api/v1/services/{service_id}/images/`      | List images for a service | Public       |
| POST   | `/api/v1/services/{service_id}/images/`      | Upload new image          | Seller/Admin |
| DELETE | `/api/v1/services/{service_id}/images/{id}/` | Delete image              | Seller/Admin |

## ⭐ Reviews
| Method | Endpoint                                      | Description                | Permission            |
| ------ | --------------------------------------------- | -------------------------- | --------------------- |
| GET    | `/api/v1/services/{service_id}/reviews/`      | List reviews for a service | Public                |
| POST   | `/api/v1/services/{service_id}/reviews/`      | Create a review            | Buyer (Authenticated) |
| PUT    | `/api/v1/services/{service_id}/reviews/{id}/` | Update review              | Review Author         |
| PATCH  | `/api/v1/services/{service_id}/reviews/{id}/` | Partial update review      | Review Author         |
| DELETE | `/api/v1/services/{service_id}/reviews/{id}/` | Delete review              | Review Author         |


## 📦 Orders
| Method | Endpoint                             | Description                                      | Permission    |
| ------ | ------------------------------------ | ------------------------------------------------ | ------------- |
| GET    | `/api/v1/orders/`                    | List all orders (Admin sees all, Buyer sees own) | Authenticated |
| POST   | `/api/v1/orders/`                    | Create new order with multiple services          | Buyer         |
| GET    | `/api/v1/orders/{id}/`               | Retrieve order details                           | Buyer/Admin   |
| PATCH  | `/api/v1/orders/{id}/`               | Update order (status, etc.)                      | Admin         |
| DELETE | `/api/v1/orders/{id}/`               | Delete order                                     | Admin         |
| POST   | `/api/v1/orders/{id}/cancel/`        | Cancel own order                                 | Buyer         |
| PATCH  | `/api/v1/orders/{id}/update_status/` | Update order status                              | Admin         |


## 👨‍💻 Author
[abtahi2024](https://github.com/abtahi2024)

