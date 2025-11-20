from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
from django.utils.http import urlencode
import random
import string

from .models import User, Product, Category, Cart, Wishlist, Order, OrderItem, ProductImage, ProductVideo, Review
from .forms import UserRegistrationForm, ProductForm, UserSettingsForm, ReviewForm


def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(
        is_featured=True,
        stock_status='in_stock',
        approval_status='approved'
    ).order_by('-created_at')
    
    # If no featured products, show recent products
    if not featured_products.exists():
        featured_products = Product.objects.filter(
            stock_status='in_stock',
            approval_status='approved'
        ).order_by('-created_at')
    
    paginator = Paginator(featured_products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'featured_products': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'store/home.html', context)


def search_products(request):
    """Search products by name or description (optionally filtered by category)"""
    query = request.GET.get('q', '').strip()
    category_value = request.GET.get('category')
    category_param_present = 'category' in request.GET
    category_slug = (category_value or '').strip()
    
    products = Product.objects.filter(stock_status='in_stock', approval_status='approved')
    selected_category = None
    
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()
        if selected_category:
            products = products.filter(category=selected_category)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        total_results = products.count()
    elif selected_category or category_param_present:
        total_results = products.count()
    else:
        products = products.none()
        total_results = 0
    
    # Pagination - 12 products per page
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = {}
    if query:
        query_params['q'] = query
    if category_param_present:
        query_params['category'] = category_slug
    pagination_query = urlencode(query_params)
    
    context = {
        'query': query,
        'products': page_obj,
        'page_obj': page_obj,
        'total_results': total_results,
        'selected_category': selected_category,
        'category_slug': category_slug if category_param_present else '',
        'category_param_present': category_param_present,
        'has_filters': bool(query or selected_category or category_param_present),
        'pagination_query': pagination_query,
    }
    return render(request, 'store/search_results.html', context)


def signup(request):
    """User registration with role selection"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {username}!')
            
            # Redirect all users to home page
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            # Redirect all users to home page
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def logout_view(request):
    """User logout"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def category_products(request, category_slug):
    """Category-wise products page with pagination"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, stock_status='in_stock', approval_status='approved')
    
    # Pagination - 12 products per page
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj,
    }
    return render(request, 'store/category_products.html', context)


def product_detail(request, product_id):
    """Product detail page with image gallery"""
    # Only show approved products to non-sellers, or show to seller if it's their own product
    if request.user.is_authenticated and request.user.role == 'seller':
        # Sellers can view their own products regardless of approval status
        product = get_object_or_404(Product, id=product_id)
        if product.seller != request.user:
            # If viewing another seller's product, must be approved
            product = get_object_or_404(Product, id=product_id, approval_status='approved')
    else:
        # Non-sellers and anonymous users can only see approved products
        product = get_object_or_404(Product, id=product_id, approval_status='approved')
    images = product.images.all()
    primary_image = images.filter(is_primary=True).first() or images.first()
    if primary_image:
        other_images = images.exclude(id=primary_image.id)
    else:
        other_images = images
    
    # Get videos for the product
    videos = product.videos.all()
    
    # Calculate delivery date (7 days from now)
    delivery_date = timezone.now().date() + timedelta(days=7)
    reviews = product.reviews.select_related('user').order_by('-created_at')
    review_form = None
    user_review = None
    can_review = False
    has_purchased = False

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        eligible_statuses = ['confirmed', 'shipped', 'delivered']
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status__in=eligible_statuses
        ).exists()
        can_review = has_purchased and product.seller != request.user

        if request.method == 'POST':
            if can_review:
                review_form = ReviewForm(request.POST, instance=user_review)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.product = product
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Thank you for sharing your review!')
                    return redirect('product_detail', product_id=product_id)
                else:
                    messages.error(request, 'Please fix the errors in your review.')
            else:
                messages.error(request, 'You need to purchase this product before leaving a review.')
        elif can_review:
            review_form = ReviewForm(instance=user_review)

    context = {
        'product': product,
        'primary_image': primary_image,
        'other_images': other_images,
        'videos': videos,
        'delivery_date': delivery_date,
        'reviews': reviews,
        'review_form': review_form,
        'user_review': user_review,
        'can_review': can_review,
        'has_purchased': has_purchased,
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def admin_page(request):
    """Admin page for sellers only"""
    if request.user.role != 'seller':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    products = Product.objects.filter(seller=request.user)
    total_products = products.count()
    total_sales = sum(product.total_sells for product in products)
    
    context = {
        'products': products,
        'total_products': total_products,
        'total_sales': total_sales,
    }
    return render(request, 'store/admin_page.html', context)


@login_required
def add_category(request):
    """Add new category via AJAX"""
    if request.user.role != 'seller':
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Category name is required'}, status=400)
        
        # Generate slug from name
        from django.utils.text import slugify
        slug = slugify(name)
        
        # Check if category already exists
        if Category.objects.filter(slug=slug).exists():
            return JsonResponse({'success': False, 'error': 'Category with this name already exists'}, status=400)
        
        try:
            category = Category.objects.create(
                name=name,
                slug=slug,
                description=description
            )
            return JsonResponse({
                'success': True,
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'slug': category.slug
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def add_product(request):
    """Add new product page for sellers"""
    if request.user.role != 'seller':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if at least one image is uploaded
            images = request.FILES.getlist('images')
            if not images:
                messages.error(request, 'Please upload at least one product image.')
                categories = Category.objects.all()
                return render(request, 'store/add_product.html', {
                    'form': form,
                    'categories': categories,
                })
            
            product = form.save(commit=False)
            product.seller = request.user
            product.approval_status = 'pending'  # New products start as pending
            product.save()
            
            # Handle multiple images
            for i, image in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_primary=(i == 0)
                )
            
            # Handle video
            video = request.FILES.get('video')
            if video:
                ProductVideo.objects.create(product=product, video=video)
            
            messages.success(request, 'Product added successfully! It will be reviewed by admin before going live.')
            return redirect('admin_page')
    else:
        form = ProductForm()
    
    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'store/add_product.html', context)


@login_required
def edit_product(request, product_id):
    """Edit product page for sellers"""
    if request.user.role != 'seller':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            # Reset approval status to pending when product is edited
            product.approval_status = 'pending'
            product.save()
            
            # Handle new images
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product updated successfully! It will be reviewed by admin before going live.')
            return redirect('admin_page')
    else:
        form = ProductForm(instance=product)
    
    categories = Category.objects.all()
    context = {
        'form': form,
        'product': product,
        'categories': categories,
    }
    return render(request, 'store/edit_product.html', context)


@login_required
def delete_product(request, product_id):
    """Delete product"""
    if request.user.role != 'seller':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('admin_page')


@login_required
def settings(request):
    """Settings page for both buyers and sellers"""
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'store/settings.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    
    # Only approved products can be added to cart
    if product.approval_status != 'approved':
        messages.error(request, 'This product is not available for purchase yet.')
        return redirect('product_detail', product_id=product_id)
    
    # Prevent sellers from adding their own products to cart
    if product.seller == request.user:
        messages.error(request, 'You cannot add your own product to cart.')
        return redirect('product_detail', product_id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, 'Product added to cart!')
        return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)


@login_required
def cart(request):
    """Cart page - accessible to all authenticated users"""
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'store/cart.html', context)


@login_required
def update_cart(request, cart_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, 'Product added to wishlist!')
    else:
        messages.info(request, 'Product is already in your wishlist!')
    
    return redirect('product_detail', product_id=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    wishlist_item.delete()
    messages.success(request, 'Product removed from wishlist!')
    return redirect('product_detail', product_id=product_id)


@login_required
def wishlist(request):
    """Wishlist page - accessible to all authenticated users"""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def my_orders(request):
    """List of user's orders (for both buyers and sellers)"""
    # For buyers: show orders they placed
    # For sellers: show orders for their products (if needed in future)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'store/my_orders.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)


@login_required
def buy_now(request):
    """Buy/Payment page"""
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Check if user is trying to buy their own products
    own_products = [item for item in cart_items if item.product.seller == request.user]
    if own_products:
        messages.error(request, 'You cannot buy your own products. Please remove them from cart.')
        return redirect('cart')
    
    total_amount = sum(item.get_total_price() for item in cart_items)
    delivery_date = timezone.now().date() + timedelta(days=7)
    
    if request.method == 'POST':
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')
        
        if not address or not pin_code:
            messages.error(request, 'Please fill all required fields.')
            return render(request, 'store/buy.html', {
                'cart_items': cart_items,
                'total_amount': total_amount,
                'delivery_date': delivery_date,
            })
        
        # Double-check: prevent buying own products
        own_products_check = [item for item in cart_items if item.product.seller == request.user]
        if own_products_check:
            messages.error(request, 'You cannot buy your own products. Please remove them from cart.')
            return redirect('cart')
        
        # Verify stock availability
        insufficient_items = []
        for cart_item in cart_items:
            available_quantity = cart_item.product.quantity
            if available_quantity < cart_item.quantity or cart_item.product.stock_status == 'out_of_stock':
                insufficient_items.append(f"{cart_item.product.name} (available: {available_quantity})")
        
        if insufficient_items:
            messages.error(
                request,
                'Insufficient stock for: ' + ', '.join(insufficient_items)
            )
            return redirect('cart')
        
        # Generate order number
        order_number = 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            address=address,
            pin_code=pin_code,
            payment_method=payment_method,
            total_amount=total_amount,
            delivery_date=delivery_date,
            status='confirmed'
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product sales and quantity
            cart_item.product.total_sells += cart_item.quantity
            cart_item.product.quantity -= cart_item.quantity
            if cart_item.product.quantity <= 0:
                cart_item.product.stock_status = 'out_of_stock'
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order placed successfully! Order Number: {order_number}')
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'delivery_date': delivery_date,
    }
    return render(request, 'store/buy.html', context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'store/order_confirmation.html', context)


@login_required
def pending_products(request):
    """Admin page to view pending products for approval"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    pending_products_list = Product.objects.filter(approval_status='pending').order_by('-created_at')
    
    context = {
        'pending_products': pending_products_list,
    }
    return render(request, 'store/pending_products.html', context)


@login_required
def approve_product(request, product_id):
    """Approve a product - Admin only"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id)
    product.approval_status = 'approved'
    product.save()
    
    messages.success(request, f'Product "{product.name}" has been approved and is now live!')
    return redirect('pending_products')


@login_required
def reject_product(request, product_id):
    """Reject a product - Admin only"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id)
    product.approval_status = 'rejected'
    product.save()
    
    messages.success(request, f'Product "{product.name}" has been rejected.')
    return redirect('pending_products')

