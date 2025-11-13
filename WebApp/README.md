# Grant Search Portal

A modern, responsive web application for searching research grants using a REST API backend.

## Features

- **Modern UI**: Built with Tailwind CSS for a clean, professional look
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Search**: Instant search results with loading indicators
- **Relevance Scoring**: Visual relevance indicators based on search distance
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Interactive Elements**: Hover effects and smooth animations

## Technologies Used

- **HTML5**: Semantic markup and modern web standards
- **CSS3**: Tailwind CSS framework for styling
- **JavaScript**: ES6+ features for modern functionality
- **jQuery**: DOM manipulation and AJAX requests
- **Font Awesome**: Professional icons

## API Integration

The application connects to a REST API endpoint at:
```
GET http://localhost:5000/api/GrantSearch?SearchText='<search_term>'
```

Expected response format:
```json
{
  "value": [
    {
      "GrantID": "8073818",
      "Title": "Grant title here",
      "Distance": 0.35605764389038086
    }
  ]
}
```

## Getting Started

### Prerequisites

- A web server (for local development)
- The grants database API running on localhost:5000

### Running the Application

1. **Using a simple HTTP server:**
   ```bash
   # Using Node.js http-server (if installed globally)
   npx http-server
   
   # Using Python 3
   python -m http.server 8000
   
   # Using Python 2
   python -m SimpleHTTPServer 8000
   ```

2. **Using VS Code Live Server:**
   - Install the "Live Server" extension
   - Right-click on `index.html` and select "Open with Live Server"

3. **Open in browser:**
   - Navigate to `http://localhost:8080` (or the port shown by your server)

### API Setup

Make sure your grants database API is running on `http://localhost:5000` with the endpoint `/api/GrantSearch`.

## File Structure

```
WebApp/
├── index.html          # Main HTML file
├── app.js             # JavaScript application logic
└── README.md          # This file
```

## Features in Detail

### Search Functionality
- Type keywords and press Enter or click Search
- Real-time validation and error handling
- Loading states with visual feedback

### Results Display
- Cards with grant information
- Relevance scoring (calculated as 1 - Distance)
- Color-coded relevance indicators
- Responsive grid layout

### Error Handling
- Network connection issues
- API timeout handling
- Empty results messaging
- User-friendly error descriptions

## Customization

### Styling
The application uses Tailwind CSS. To customize:
- Modify classes in `index.html`
- Add custom CSS in the `<style>` section
- Adjust the color scheme by changing Tailwind color classes

### API Configuration
Change the API endpoint in `app.js`:
```javascript
const API_BASE_URL = 'your-api-endpoint-here';
```

## Browser Support

- Modern browsers (Chrome 60+, Firefox 60+, Safari 12+, Edge 79+)
- Responsive design for mobile devices
- Progressive enhancement for older browsers

## License

This project is part of the pass-2025 repository.