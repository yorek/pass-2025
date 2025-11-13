$(document).ready(function() {
    // API configuration
    const API_BASE_URL = 'http://localhost:5000/api/GrantSearch';
    
    // DOM elements
    const $searchInput = $('#searchInput');
    const $searchBtn = $('#searchBtn');
    const $searchStatus = $('#searchStatus');
    const $errorMessage = $('#errorMessage');
    const $resultsContainer = $('#resultsContainer');
    const $resultsGrid = $('#resultsGrid');
    const $resultCount = $('#resultCount');
    const $welcomeMessage = $('#welcomeMessage');
    const $errorText = $('#errorText');
    
    // Search functionality
    function performSearch() {
        const searchText = $searchInput.val().trim();
        
        if (!searchText) {
            showError('Please enter search keywords');
            return;
        }
        
        // Show loading state
        hideAllMessages();
        $searchStatus.removeClass('hidden');
        $searchBtn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin mr-2"></i>Searching...');
        
        // Make API call
        const apiUrl = `${API_BASE_URL}?SearchText=${encodeURIComponent(searchText)}`;
        
        $.ajax({
            url: apiUrl,
            method: 'GET',
            dataType: 'json',
            timeout: 10000,
            success: function(data) {
                hideAllMessages();
                displayResults(data.value || [], searchText);
            },
            error: function(xhr, status, error) {
                hideAllMessages();
                let errorMessage = 'An error occurred while searching';
                
                if (status === 'timeout') {
                    errorMessage = 'Search request timed out. Please try again.';
                } else if (xhr.status === 404) {
                    errorMessage = 'Search service not available. Please ensure the API is running.';
                } else if (xhr.status === 0) {
                    errorMessage = 'Unable to connect to search service. Please check your connection.';
                } else {
                    errorMessage = `Search failed: ${error}`;
                }
                
                showError(errorMessage);
            },
            complete: function() {
                $searchBtn.prop('disabled', false).html('<i class="fas fa-search mr-2"></i>Search');
            }
        });
    }
    
    // Display search results
    function displayResults(results, searchText) {
        $welcomeMessage.addClass('hidden');
        
        if (results.length === 0) {
            $resultsContainer.removeClass('hidden');
            $resultCount.text('No results found');
            $resultsGrid.html(`
                <div class="col-span-full text-center py-12">
                    <i class="fas fa-search-minus text-4xl text-gray-300 mb-4"></i>
                    <h3 class="text-xl font-semibold text-gray-700 mb-2">No grants found</h3>
                    <p class="text-gray-500">Try different keywords or broaden your search terms</p>
                </div>
            `);
            return;
        }
        
        $resultCount.text(`${results.length} result${results.length !== 1 ? 's' : ''} found`);
        
        // Sort results by distance (most relevant first)
        results.sort((a, b) => a.Distance - b.Distance);
        
        const resultsHtml = results.map(grant => createGrantCard(grant)).join('');
        $resultsGrid.html(resultsHtml);
        $resultsContainer.removeClass('hidden');
        
        // Animate results appearance
        $('.result-card').each(function(index) {
            $(this).css('opacity', '0').delay(index * 100).animate({opacity: 1}, 300);
        });
    }
    
    // Create grant card HTML
    function createGrantCard(grant) {
        const relevanceScore = Math.round((1 - grant.Distance) * 100);
        const relevanceClass = getRelevanceClass(relevanceScore);
        const relevanceLabel = getRelevanceLabel(relevanceScore);
        
        return `
            <div class="result-card bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <div class="flex items-start justify-between mb-4">
                    <div class="flex-1">
                        <span class="inline-block px-2 py-1 text-xs font-semibold ${relevanceClass} rounded-full mb-2">
                            ${relevanceLabel}
                        </span>
                        <h4 class="text-lg font-semibold text-gray-900 mb-2 leading-tight">
                            ${escapeHtml(grant.Title)}
                        </h4>
                    </div>
                </div>
                
                <div class="space-y-3">
                    <div class="flex items-center text-sm text-gray-600">
                        <i class="fas fa-hashtag mr-2 text-gray-400"></i>
                        <span class="font-medium">Grant ID:</span>
                        <span class="ml-1 font-mono">${grant.GrantID}</span>
                    </div>
                    
                    <div class="flex items-center text-sm text-gray-600">
                        <i class="fas fa-chart-bar mr-2 text-gray-400"></i>
                        <span class="font-medium">Relevance:</span>
                        <span class="ml-1">${relevanceScore}%</span>
                    </div>
                    
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="distance-bar bg-gradient-to-r from-green-400 to-blue-500 h-2 rounded-full" 
                             style="width: ${relevanceScore}%"></div>
                    </div>
                </div>
                
                <div class="mt-4 pt-4 border-t border-gray-100">
                    <button class="w-full bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-medium py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center">
                        <i class="fas fa-external-link-alt mr-2"></i>
                        View Grant Details
                    </button>
                </div>
            </div>
        `;
    }
    
    // Get relevance class based on score
    function getRelevanceClass(score) {
        if (score >= 80) return 'bg-green-100 text-green-800';
        if (score >= 60) return 'bg-yellow-100 text-yellow-800';
        if (score >= 40) return 'bg-orange-100 text-orange-800';
        return 'bg-red-100 text-red-800';
    }
    
    // Get relevance label based on score
    function getRelevanceLabel(score) {
        if (score >= 80) return 'Highly Relevant';
        if (score >= 60) return 'Relevant';
        if (score >= 40) return 'Moderately Relevant';
        return 'Low Relevance';
    }
    
    // Utility functions
    function hideAllMessages() {
        $searchStatus.addClass('hidden');
        $errorMessage.addClass('hidden');
    }
    
    function showError(message) {
        $errorText.text(message);
        $errorMessage.removeClass('hidden');
    }
    
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    // Event listeners
    $searchBtn.on('click', performSearch);
    
    $searchInput.on('keypress', function(e) {
        if (e.which === 13) { // Enter key
            performSearch();
        }
    });
    
    // Auto-focus search input
    $searchInput.focus();
    
    // Example searches for demo
    const exampleSearches = [
        'image processing',
        'machine learning',
        'data mining',
        'computer vision',
        'artificial intelligence'
    ];
    
    // Add placeholder cycling effect
    let placeholderIndex = 0;
    setInterval(function() {
        placeholderIndex = (placeholderIndex + 1) % exampleSearches.length;
        $searchInput.attr('placeholder', `Try searching: "${exampleSearches[placeholderIndex]}"`);
    }, 3000);
});