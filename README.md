# Gujarat Crafts - E-commerce Website

A Django-based e-commerce platform for Gujarat's handcrafted items, where artists can sell their products and buyers can purchase them.

## Features

### For Buyers:
- Browse products by category or use the Amazon-style search bar with category filter
- Discover featured products on the homepage (paginated list, 8 per page)
- View product details with image gallery, video support, and full review section
- Read/write product reviews (1–5 stars) after purchasing an item
- Add products to cart or wishlist, then place orders with cash on delivery
- Manage personal profile and account settings

### For Sellers:
- Seller dashboard (“Sells Management”) to track inventory and sales
- Add, edit, delete, and feature products with multiple media uploads
- Monitor stock levels, quantities sold, and approval status
- Product approval workflow: new/edited products stay hidden until staff approves them
- View inline status badges showing stock + approval state

### For Staff / Admin:
- Dedicated “Pending Products” page to approve/reject seller submissions
- Full review moderation via Django admin (all reviews stored centrally)

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML, CSS, JavaScript (custom responsive theme inspired by Gujarati crafts)
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
- Sticky header with logo, account shortcuts, and search bar (category dropdown + keyword)
- Hero section with artisan-focused imagery and CTA
- Featured products grid with pagination (8 per page) and graceful fallbacks when empty

### Product Pages
- Category listing pages with pagination (8 per page) and stock/approval filtering
- Product detail page featuring image gallery, video embeds, delivery estimate, and sales stats
- Review system: buyers who completed an order can submit/edit a 1–5 star review plus text
- Live average rating recalculations and review list with avatars + timestamps
- Add-to-cart, wishlist, and quantity controls (prevents sellers buying own products)

### Admin Panel (Seller)
- Dashboard cards summarizing product count and total sales
- Product table with preview image, category, price, quantity, sales, and approval badge
- Quick actions to edit/delete entries and link to add-product form
- All new/edited products automatically revert to “Pending” until approved

### Cart & Checkout
- Shopping cart with quantity management and validation
- Checkout page collects address, PIN, and payment method (COD) with stock double-check
- Order confirmation page showing order number and summary

### Reviews & Ratings
- `Review` model links each buyer/product pair (one review per purchase)
- Review form rendered inline on the product page when the buyer qualifies (delivered order, not seller)
- Product rating field auto-updates using average of all approved reviews

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
- Order tracking & shipment updates
- Advanced search filters (price range, rating, etc.)
- Email/SMS notifications
- Rich CMS pages (About, Contact, FAQ)
- Product comparison feature
- Seller analytics dashboard and export tools

## License

This project is open source and available for educational purposes.

## Contact

For questions or support, please contact: info@gujaratcrafts.com

