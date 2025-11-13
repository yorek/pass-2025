$(document).ready(function() {
    const API_ENDPOINT = 'http://localhost:5000/api/GrantSearch';
    
    // Event listeners
    $('#searchButton').click(performSearch);
    $('#searchInput').keypress(function(e) {
        if (e.which === 13) { // Enter key
            performSearch();
        }
    });

    // Main search function
    function performSearch() {
        const searchText = $('#searchInput').val().trim();
        
        if (!searchText) {
            showError('Please enter search keywords');
            return;
        }

        // Reset UI
        hideAllMessages();
        $('#resultsContainer').empty();
        showLoading(true);

        // Build API URL
        const apiUrl = `${API_ENDPOINT}?SearchText=${encodeURIComponent(searchText)}`;

        // Make AJAX request
        $.ajax({
            url: apiUrl,
            method: 'GET',
            dataType: 'json',
            timeout: 30000, // 30 seconds timeout
            success: function(data) {
                showLoading(false);
                handleSearchResults(data);
            },
            error: function(xhr, status, error) {
                showLoading(false);
                handleSearchError(xhr, status, error);
            }
        });
    }

    // Handle successful search results
    function handleSearchResults(data) {
        if (!data || !data.value || data.value.length === 0) {
            $('#noResults').removeClass('hidden').addClass('fade-in');
            return;
        }

        const results = data.value;
        displayResults(results);
        updateSearchStats(results.length);
    }

    // Display results in the grid
    function displayResults(results) {
        const container = $('#resultsContainer');
        
        results.forEach((grant, index) => {
            const similarityScore = calculateSimilarityPercentage(grant.Distance);
            const scoreColor = getScoreColor(similarityScore);
            
            const card = `
                <div class="search-result bg-white rounded-xl shadow-lg p-6 fade-in hover:shadow-2xl" 
                     style="animation-delay: ${index * 0.1}s">
                    <div class="flex justify-between items-start mb-4">
                        <div class="bg-gradient-to-r from-purple-100 to-indigo-100 rounded-lg px-4 py-2">
                            <span class="text-xs text-gray-600 font-semibold uppercase tracking-wide">Grant ID</span>
                            <p class="text-lg font-bold text-purple-700">${escapeHtml(grant.GrantID)}</p>
                        </div>
                        <div class="text-right">
                            <span class="text-xs text-gray-500 block mb-1">Relevance</span>
                            <div class="flex items-center gap-2">
                                <div class="w-12 h-12 rounded-full ${scoreColor} flex items-center justify-center">
                                    <span class="text-white font-bold text-sm">${similarityScore}%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <h3 class="text-xl font-semibold text-gray-800 mb-3 line-clamp-3">
                        ${escapeHtml(grant.Title)}
                    </h3>
                    
                    <div class="mt-4 pt-4 border-t border-gray-200">
                        <div class="flex items-center justify-between text-sm text-gray-500">
                            <span class="flex items-center gap-2">
                                <i class="fas fa-ruler-horizontal"></i>
                                Distance: ${grant.Distance.toFixed(4)}
                            </span>
                            <button class="text-purple-600 hover:text-purple-800 font-semibold transition-colors flex items-center gap-1"
                                    onclick="viewGrantDetails('${escapeHtml(grant.GrantID)}')">
                                View Details
                                <i class="fas fa-arrow-right"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            container.append(card);
        });
    }

    // Calculate similarity percentage from distance
    function calculateSimilarityPercentage(distance) {
        // Lower distance = higher similarity
        // Assuming distance ranges from 0 to 1, convert to percentage
        const similarity = (1 - distance) * 100;
        return Math.max(0, Math.min(100, Math.round(similarity)));
    }

    // Get color based on similarity score
    function getScoreColor(score) {
        if (score >= 80) return 'bg-green-500';
        if (score >= 60) return 'bg-blue-500';
        if (score >= 40) return 'bg-yellow-500';
        return 'bg-orange-500';
    }

    // Update search statistics
    function updateSearchStats(count) {
        $('#resultCount').text(`Found ${count} grant${count !== 1 ? 's' : ''} matching your search`);
        $('#searchStats').removeClass('hidden').addClass('fade-in');
    }

    // Handle search errors
    function handleSearchError(xhr, status, error) {
        let errorMsg = 'An error occurred while searching. Please try again.';
        
        if (status === 'timeout') {
            errorMsg = 'The request timed out. Please check your connection and try again.';
        } else if (xhr.status === 404) {
            errorMsg = 'API endpoint not found. Please ensure the server is running on http://localhost:5000';
        } else if (xhr.status === 0) {
            errorMsg = 'Cannot connect to the server. Please ensure the API is running on http://localhost:5000';
        } else if (xhr.responseJSON && xhr.responseJSON.message) {
            errorMsg = xhr.responseJSON.message;
        }
        
        showError(errorMsg);
    }

    // Show error message
    function showError(message) {
        $('#errorText').text(message);
        $('#errorMessage').removeClass('hidden').addClass('fade-in');
    }

    // Show/hide loading indicator
    function showLoading(show) {
        if (show) {
            $('#loadingIndicator').removeClass('hidden').addClass('fade-in');
        } else {
            $('#loadingIndicator').addClass('hidden');
        }
    }

    // Hide all messages
    function hideAllMessages() {
        $('#errorMessage').addClass('hidden');
        $('#noResults').addClass('hidden');
        $('#searchStats').addClass('hidden');
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Global function for view details button
    window.viewGrantDetails = function(grantId) {
        alert(`Viewing details for Grant ID: ${grantId}\n\nThis would typically open a detailed view or navigate to a grant details page.`);
        // You can replace this with actual navigation or modal display
    };
});
