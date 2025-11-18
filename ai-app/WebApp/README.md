# Grant Search Web Application

A modern, responsive web application for searching grants using AI-powered semantic search.

## Features

- 🔍 Real-time grant search functionality
- 🎨 Modern UI with Tailwind CSS
- 📱 Fully responsive design
- ⚡ Fast and intuitive user experience
- 🎯 Similarity scoring for search results
- ⌨️ Keyboard shortcuts (Enter to search)
- 🔄 Loading states and error handling

## Technology Stack

- **HTML5** - Semantic markup
- **JavaScript** - Application logic
- **jQuery** - AJAX requests and DOM manipulation
- **Tailwind CSS** - Modern styling framework
- **Font Awesome** - Icons

## Prerequisites

- A running REST API endpoint at `http://localhost:5000/api/GrantSearch`
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

1. Navigate to the WebApp folder
2. Open `index.html` in your web browser

Alternatively, you can serve the application using a local web server:

```bash
# Using Python
python -m http.server 8080

# Using Node.js (http-server)
npx http-server -p 8080
```

Then visit `http://localhost:8080` in your browser.

## Usage

1. Enter search keywords in the search box
2. Click the "Search" button or press Enter
3. View the results with similarity scores
4. Results are ranked by relevance (distance score)

## API Integration

The application expects a REST endpoint that returns JSON in the following format:

```json
{
  "value": [
    {
      "GrantID": "8073818",
      "Title": "Co-location visual pattern mining for near-duplicate image retrieval",
      "Distance": 0.35605764389038086
    }
  ]
}
```

### API Parameters

- **SearchText**: The search query string (URL encoded)

## Configuration

To change the API endpoint, edit the `API_ENDPOINT` constant in `app.js`:

```javascript
const API_ENDPOINT = 'http://localhost:5000/api/GrantSearch';
```

## Features Breakdown

### Search Functionality
- Input validation
- URL encoding for special characters
- Keyboard support (Enter key)
- Loading states with spinner

### Results Display
- Card-based layout with hover effects
- Similarity percentage calculation
- Result count badge
- Smooth scroll to results
- Numbered results for easy reference

### Error Handling
- Connection errors
- Timeout handling
- API errors
- Empty result sets
- User-friendly error messages

## Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Customization

### Colors
The application uses a purple gradient theme. To customize colors, modify the Tailwind classes in `index.html` or the CSS gradients in the `<style>` section.

### Timeout
The default AJAX timeout is 30 seconds. Modify it in `app.js`:

```javascript
timeout: 30000, // milliseconds
```

## License

See LICENSE.txt in the parent directory.
