# ShirtVerse

ShirtVerse is a Django-based e-commerce platform for curated apparel. It includes product browsing, cart and checkout flows, user profiles, and order management, all backed by Django models and the Django admin.

## Features
- Product catalog with categories, galleries, and detailed pages
- Shopping cart with persistent session data and reusable context processors
- Checkout flow with address management and order confirmation emails
- User accounts for authentication, password resets, and profile dashboards
- Admin dashboards for managing products, orders, and user-generated data

## Tech Stack
- Python 3.x, Django 4.x
- PostgreSQL or MySQL (configurable via `settings.py`)
- Bootstrap-based frontend located in `static/` and `templates/`

## Getting Started
1. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   - Copy `shirtverse/settings.py` and update database credentials, email backend, and secret key.
   - Set `DEBUG`, `ALLOWED_HOSTS`, and any provider-specific keys.
4. **Apply migrations and load initial data**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Running Tests
```
python manage.py test
```

## Project Structure
- `accounts/`, `profiles/` – Authentication, registration, and user settings
- `products/` – Catalog models, views, and templates
- `cart/` – Cart models, utilities, and views for session-based carts
- `orders/` – Checkout, addresses, and order lifecycle
- `core/` – Site-wide configuration and base pages
- `templates/` – Shared HTML templates organized by app
- `static/` – Compiled CSS, JS, and assets including Bootstrap overrides
- `media/` – Uploaded product imagery

## Contributing
1. Fork the repository and create a feature branch.
2. Add tests and keep existing ones green.
3. Submit a pull request that describes the change and screenshots when UI is involved.

## License
This project is distributed under the MIT License. See `LICENSE` for details.
# brovid
