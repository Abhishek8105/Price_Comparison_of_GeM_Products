document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const resultsDiv = document.getElementById('results');

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    function performSearch() {
        const query = searchInput.value.trim();
        if (query) {
            resultsDiv.innerHTML = '<p class="text-center">Searching...</p>';
            axios.post('/search', { product: query })
                .then(response => {
                    displayResults(response.data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    resultsDiv.innerHTML = '<p class="text-center text-red-500">An error occurred. Please try again.</p>';
                });
        }
    }

    function displayResults(data) {
        resultsDiv.innerHTML = '';
        for (const [platform, products] of Object.entries(data)) {
            products.forEach(product => {
                const productCard = `
                    <div class="bg-white shadow-md rounded-lg overflow-hidden">
                        <img src="${product.image_url}" alt="${product.name}" class="w-full h-48 object-cover">
                        <div class="p-4">
                            <h3 class="font-bold text-xl mb-2">${product.name}</h3>
                            <p class="text-gray-700 text-base mb-2">Price: ₹${product.price}</p>
                            <p class="text-gray-600 text-sm">Platform: ${platform}</p>
                            <a href="${product.product_url}" target="_blank" class="mt-4 inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                                View Product
                            </a>
                        </div>
                    </div>
                `;
                resultsDiv.innerHTML += productCard;
            });
        }
    }
});