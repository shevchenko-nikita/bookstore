document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');

    searchInput.addEventListener('input', function () {
        const query = this.value;
        if (query.length > 0) {
            fetch(`/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = '';
                    data.results.forEach(item => {
                        const link = document.createElement('a');
                        link.href = item.url;
                        link.textContent = `${item.name} — ${item.price} грн`;
                        resultsContainer.appendChild(link);
                    });
                });
        } else {
            resultsContainer.innerHTML = '';
        }
    });

    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.innerHTML = '';
        }
    });
});