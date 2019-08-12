from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from products.models import Product, Category, ProductImage


def products(request):
    products = Product.objects.all()  
    featured_products = Product.objects.filter(featured='True').order_by('?')[:4]
    return render(
        request,
        'products.html',
        context={'products': products, 'featured_products': featured_products}
    )


def create_product(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        return render(request, 'create_product.html', context={'categories':categories}) 
    elif request.method == 'POST':
        fields = ['name', 'sku', 'price']
        errors = {}
        for field in fields:
            if not request.POST.get(field):
                errors[field] = 'This Field is Required'
        if errors:
            return render(request,
                          'create_product.html', 
                          context={'categories':categories, 'errors':errors, 'payload':request.POST})
        name = request.POST.get('name')
        if len(name) > 100:
            errors['name'] = "Name can't be longer than 100 characters."
        sku=request.POST.get('sku')
        if len(sku) != 8:
            errors['sku'] = "SKU must be 8 alphanumeric characters"
        price=request.POST.get('price')
        if float(price) > 9999.99 or float(price) < 0:
            errors['price']='TOO RICH FOR MY BLOOD'
        if errors:
            return render(request,
                          'create_product.html', 
                          context={'categories':categories, 'sku':sku, 'payload':request.POST})
        category = Category.objects.get(name=request.POST.get('category'))
        
        product = Product.objects.create(name=request.POST.get('name'),
            sku=request.POST.get('sku'),
            price=float(request.POST.get('price')),
            description=request.POST.get('description', ''),
            category=category
        )
        images = []
        for i in range(3):
            image=request.POST.get('image_{}'.format(i+1))
            if image:
                images.append(image)
        for image in images:
            ProductImage.objects.create(product=product,url=image)
        return redirect('products')


def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    if request.method == 'GET':
        return render(request, 'edit_product.html', context={'product':product, 'categories':categories, 'image':[image.url for image in product.productimage_set.all()]})
    elif request.method == 'POST':
        fields = ['name', 'sku', 'price']
        errors = {}
        for field in fields:
            if not request.POST.get(field):
                errors[field] = 'This Field is Required'
        if errors:
            return render(request,
                          'create_product.html', 
                          context={'categories':categories, 'errors':errors, 'payload':request.POST})
        name = request.POST.get('name')
        if len(name) > 100:
            errors['name'] = "Name can't be longer than 100 characters."
        sku=request.POST.get('sku')
        if len(sku) != 8:
            errors['sku'] = "SKU must be 8 alphanumeric characters"
        price=request.POST.get('price')
        if float(price) > 9999.99 or float(price) < 0:
            errors['price']='TOO RICH FOR MY BLOOD'
        if errors:
            return render(request,
                          'create_product.html', 
                          context={'categories':categories, 'sku':sku, 'payload':request.POST})
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.price= request.POST.get('price')
        product.decription = request.POST.get('description')
        category = Category.objects.get(name=request.POST.get('category'))
        product.category = category
        product.save()
        
        newimages = {}
        for i in range(3):
            image=request.POST.get('image_{}'.format(i+1))
            if image:
                newimages.append(image)
        oldimages = [image.url for image in productimage_set.all()]
        
        deleteimages = []
        for image in oldimages:
            if image not in newimages:
                deleteimages.append(image)
        ProductImage.objects.filter(url__in = deleteimages).delete()

        return redirect('products')


def delete_product(request, product_id):
    # Get product with given product_id
    product = Product.objects.get(id=product_id)
    if request.method == 'GET':
        # render 'delete_product.html' sending product as context
        return render(request, 'delete_product.html', context={'product':product})
                      
    elif request.method == "POST":
        product.delete()
        return redirect('products')


def toggle_featured(request, product_id):
    # Get product with given product_id
    product = Product.objects.get(id=product_id)

    # Toggle product featured flag
    product.features = not product.featured

    # Redirect to 'products' view
    return redirect('products')
