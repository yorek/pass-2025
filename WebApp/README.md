# Grant Search Web Application

A modern, responsive web application for searching grants using semantic search technology.

## Features

- 🔍 **Semantic Search**: Search grants using natural language queries
- 🎨 **Modern UI**: Built with Tailwind CSS for a clean, professional look
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- ⚡ **Real-time Search**: Instant results as you search
- 📊 **Relevance Scoring**: Visual indicators showing match relevance
- 🎯 **Clean Interface**: Intuitive and easy to use

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Tailwind CSS for styling
- **JavaScript**: jQuery for DOM manipulation and AJAX
- **Font Awesome**: Icons
- **REST API**: Connects to backend grant search service

## Setup and Usage

### Prerequisites

- A web browser (Chrome, Firefox, Safari, Edge)
- Backend API running on `http://localhost:5000`

### Running the Application

1. Open `index.html` in your web browser
2. Enter search keywords in the search box
3. Click "Search" or press Enter
4. View the results with relevance scores

### API Endpoint

The application connects to:
```
GET http://localhost:5000/api/GrantSearch?SearchText=<search_text>
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

## Project Structure

```
WebApp/
├── index.html       # Main HTML file
├── app.js          # JavaScript application logic
└── README.md       # This file
```

## Features Explained

### Relevance Scoring

- The app converts distance values to similarity percentages
- Lower distance = higher relevance
- Color-coded badges:
  - 🟢 Green (80-100%): Highly relevant
  - 🔵 Blue (60-79%): Very relevant
  - 🟡 Yellow (40-59%): Moderately relevant
  - 🟠 Orange (0-39%): Less relevant

### Error Handling

- Connection errors
- Timeout handling (30 seconds)
- API not found (404)
- No results found
- Invalid input validation

## Customization

### Changing the API Endpoint

Edit the `API_ENDPOINT` constant in `app.js`:
```javascript
const API_ENDPOINT = 'http://your-api-url/api/GrantSearch';
```

### Styling

The application uses Tailwind CSS. You can customize colors and styles by:
- Modifying the gradient colors in the header
- Changing the color scheme in the CSS classes
- Adjusting the custom CSS in the `<style>` section of `index.html`

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

## License

See LICENSE.txt in the project root.
