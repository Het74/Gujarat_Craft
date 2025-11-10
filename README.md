# Gujarat Crafts - E-commerce Website

A Django-based e-commerce platform for Gujarat's handcrafted items, where artists can sell their products and buyers can purchase them.

## Features

### For Buyers:
- Browse products by category
- View product details with image gallery
- Add products to cart
- Add products to wishlist
- Place orders with cash on delivery
- Manage profile and settings

### For Sellers:
- Admin panel to manage products
- Add, edit, and delete products
- View stock status and sales statistics
- Upload multiple product images and videos
- Feature products on homepage

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default)
- **Image Handling**: Pillow

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser** (optional, for Django admin):
```bash
python manage.py createsuperuser
```

7. **Run the development server**:
```bash
python manage.py runserver
```

8. **Access the website**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Setup Instructions

### 1. Create Categories

Before adding products, you need to create product categories. You can do this through:
- Django admin panel (after creating superuser)
- Or create them programmatically in Django shell

To create categories via Django shell:
```bash
python manage.py shell
```

Then:
```python
from store.models import Category

Category.objects.create(name="Pottery", slug="pottery")
Category.objects.create(name="Textiles", slug="textiles")
Category.objects.create(name="Jewelry", slug="jewelry")
Category.objects.create(name="Woodwork", slug="woodwork")
Category.objects.create(name="Metalwork", slug="metalwork")
Category.objects.create(name="Paintings", slug="paintings")
```

### 2. Create User Accounts

- **Buyer Account**: Sign up and select "Buyer" role
- **Seller Account**: Sign up and select "Seller" role

Sellers will be redirected to the admin page after signup where they can add products.

### 3. Add Products (Seller Only)

1. Login as a seller
2. Navigate to "Admin Panel"
3. Click "Add New Product"
4. Fill in product details:
   - Name, Description, Price, Quantity
   - Select Category
   - Upload images (first image will be primary)
   - Optionally upload video or add video URL
   - Set stock status
   - Check "Feature this product" to show on homepage

## Project Structure

```
gujarat_Crafts/
├── gujarat_crafts/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                   # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL patterns
│   ├── forms.py            # Form definitions
│   ├── admin.py            # Admin configuration
│   └── templates/          # HTML templates
│       └── store/
├── static/                 # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── media/                  # User uploaded files (created automatically)
├── manage.py
└── requirements.txt
```

## Key Models

- **User**: Custom user model with role (Seller/Buyer)
- **Category**: Product categories
- **Product**: Product information
- **ProductImage**: Product images
- **ProductVideo**: Product videos
- **Cart**: Shopping cart items
- **Wishlist**: Wishlist items
- **Order**: Order information
- **OrderItem**: Order line items

## Features Implementation

### Home Page
- Header with navigation and logo
- Category navigation bar
- Hero section with engaging visuals
- Featured products grid (6 products)

### Product Pages
- Category-wise product listing with pagination (12 per page)
- Product detail page with image gallery
- Product rating and sales information
- Add to cart and wishlist functionality

### Admin Panel (Seller)
- Dashboard with statistics
- Product management (add, edit, delete)
- Stock and sales tracking
- Product listing table

### Cart & Checkout
- Shopping cart with quantity management
- Checkout page with delivery address
- Order confirmation with order number
- Cash on delivery payment method

### Settings
- Profile management
- Update personal information
- Available for both buyers and sellers

## Development Notes

- The project uses SQLite database by default (suitable for development)
- For production, consider using PostgreSQL or MySQL
- Media files are stored in the `media/` directory
- Static files are served from the `static/` directory
- Secret key should be changed for production deployment

## Future Enhancements

- Payment gateway integration
- Order tracking
- Product reviews and ratings system
- Advanced search and filters
- Email notifications
- About and Contact pages
- Product comparison feature
- Seller dashboard analytics

## License

This project is open source and available for educational purposes.

## Contact

For questions or support, please contact: info@gujaratcrafts.com

