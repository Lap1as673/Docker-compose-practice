document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('shorten-form');
    const urlInput = document.getElementById('url-input');
    const resultDiv = document.getElementById('result');
    const shortUrlLink = document.getElementById('short-url');
    const statsUrlLink = document.getElementById('stats-url');
    const errorDiv = document.getElementById('error');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Сброс предыдущих состояний
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');

        const longUrl = urlInput.value.trim();
        
        if (!longUrl) {
            showError('Please enter a URL');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/shorten/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    original_url: longUrl
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Показываем результат
            shortUrlLink.href = `http://localhost:8000/${data.short_code}`;
            shortUrlLink.textContent = shortUrlLink.href;
            
            statsUrlLink.href = data.admin_url;
            statsUrlLink.textContent = 'View statistics';
            
            resultDiv.classList.remove('hidden');
            urlInput.value = '';

        } catch (error) {
            showError('Error shortening URL: ' + error.message);
        }
    });

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }
});