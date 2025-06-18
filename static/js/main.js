document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('optimizeForm');
    const fileInput = document.getElementById('fileInput');
    const textInput = document.getElementById('textInput');
    const keywordsInput = document.getElementById('keywordsInput');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const results = document.getElementById('results');
    const contentAnalysis = document.getElementById('contentAnalysis');
    const seoOptimization = document.getElementById('seoOptimization');
    const geoOptimization = document.getElementById('geoOptimization');

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Validate input
        if (!fileInput.files[0] && !textInput.value.trim()) {
            alert('Please provide either a file or text content');
            return;
        }

        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        results.classList.add('opacity-50');

        try {
            // Prepare form data
            const formData = new FormData();
            
            if (fileInput.files[0]) {
                formData.append('file', fileInput.files[0]);
            }
            
            if (textInput.value.trim()) {
                formData.append('text', textInput.value.trim());
            }

            // Add keywords
            const keywords = keywordsInput.value
                .split(',')
                .map(k => k.trim())
                .filter(k => k);
            if (keywords.length > 0) {
                formData.append('target_keywords', JSON.stringify(keywords));
            }

            // Add target platforms
            const platforms = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                .map(cb => cb.value);
            if (platforms.length > 0) {
                formData.append('target_platforms', JSON.stringify(platforms));
            }

            // Send request to API
            const response = await fetch('/api/optimize', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Display results
            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your content. Please try again.');
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
            results.classList.remove('opacity-50');
        }
    });

    // Display optimization results
    function displayResults(data) {
        // Content Analysis
        contentAnalysis.innerHTML = formatContentAnalysis(data.content_analysis);

        // SEO Optimization
        seoOptimization.innerHTML = formatSEOOptimization(data.seo_optimization);

        // GEO Optimization
        geoOptimization.innerHTML = formatGEOOptimization(data.geo_optimization);
    }

    // Format content analysis results
    function formatContentAnalysis(analysis) {
        return `
            <div class="space-y-2">
                <p><strong>Word Count:</strong> ${analysis.metadata.word_count}</p>
                <p><strong>Sentence Count:</strong> ${analysis.metadata.sentence_count}</p>
                <p><strong>Paragraph Count:</strong> ${analysis.metadata.paragraph_count}</p>
                ${analysis.metadata.is_html ? '<p><strong>Content Type:</strong> HTML</p>' : ''}
            </div>
        `;
    }

    // Format SEO optimization results
    function formatSEOOptimization(seo) {
        return `
            <div class="space-y-2">
                <p><strong>Overall Score:</strong> ${seo.score}/100</p>
                <div class="mt-2">
                    <p class="font-semibold">Suggestions:</p>
                    <ul class="list-disc pl-5 mt-1">
                        ${seo.suggestions.map(s => `<li>${s}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    // Format GEO optimization results
    function formatGEOOptimization(geo) {
        return `
            <div class="space-y-2">
                <p><strong>Overall Score:</strong> ${geo.score}/100</p>
                <div class="mt-2">
                    <p class="font-semibold">Platform-specific Optimizations:</p>
                    <ul class="list-disc pl-5 mt-1">
                        ${Object.entries(geo.platform_metrics)
                            .map(([platform, metrics]) => `
                                <li>
                                    <strong>${platform}:</strong>
                                    <ul class="list-disc pl-5">
                                        ${Object.entries(metrics)
                                            .map(([key, value]) => `<li>${key}: ${value}</li>`)
                                            .join('')}
                                    </ul>
                                </li>
                            `)
                            .join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    // Handle file input change
    fileInput.addEventListener('change', () => {
        if (fileInput.files[0]) {
            textInput.value = '';
        }
    });

    // Handle text input change
    textInput.addEventListener('input', () => {
        if (textInput.value.trim()) {
            fileInput.value = '';
        }
    });
}); 