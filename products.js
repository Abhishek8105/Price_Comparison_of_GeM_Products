document.addEventListener('DOMContentLoaded', function() {
    fetch('gem_products_frontend.json')
        .then(response => response.json())
        .then(data => {
            const categoriesDiv = document.getElementById('categories');
            Object.keys(data).forEach(category => {
                const button = document.createElement('button');
                button.textContent = category;
                button.className = 'category-card bg-blue-500 p-4 rounded-lg shadow-md text-center hover:bg-blue-100 transition duration-300';
                button.onclick = (event) => {
                    document.querySelectorAll('.category-card').forEach(btn => {
                        btn.classList.remove('bg-white-500', 'text-white');
                    });
                    event.target.classList.add('bg-white-600', 'text-white');
                    displayProducts(category, data[category]);
                };
                categoriesDiv.appendChild(button);
            });
            // Display featured products
            displayFeaturedProducts(data);
        })
        .catch(error => console.error('Error loading product data:', error));
});
function createProductCard(product, isFeatured = false) {
    const productCard = document.createElement('div');
    productCard.className = 'bg-gray product-card  rounded-lg shadow-md overflow-hidden cursor-pointer';
    productCard.innerHTML = `
        <img src="${product.image_url}" alt="${product.name}" class="w-full h-48 object-cover">
        <div class="p-4">
            <h4 class="text-xl font-semibold mb-2">${product.name.length > 50 ? product.name.substring(0, 50) + '...' : product.name}</h4>
            <div class="flex justify-between items-center">
                <span class="text-xl font-bold text-green-600">₹${product.price}</span>
                <a href="${product.product_url}" target="_blank" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">View</a>
            </div>
        </div>
    `;
    // Add click event to the whole card except the "View" button
    productCard.addEventListener('click', (event) => {
        if (!event.target.closest('a')) {
            window.location.href = product.product_url;
        }
    });
    return productCard;
}
function displayProducts(category, products) {
    const productSection = document.getElementById('productSection');
    const productList = document.getElementById('productList');
    productList.innerHTML = '';
    products.forEach(product => {
        const productCard = createProductCard(product);
        productList.appendChild(productCard);
    });
    productSection.classList.remove('hidden');
}
function displayFeaturedProducts(data) {
    const featuredProductList = document.getElementById('featuredProductList');
    featuredProductList.innerHTML = '';
    
    // Select a few random products from each category
    Object.values(data).forEach(categoryProducts => {
        const randomProduct = categoryProducts[Math.floor(Math.random() * categoryProducts.length)];
        const productCard = createProductCard(randomProduct, true);
        featuredProductList.appendChild(productCard);
    });
}