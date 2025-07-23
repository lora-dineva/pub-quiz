# Pub Quiz Frontend

A simple web-based UI for adding quiz questions to the Pub Quiz backend system.

## Features

- ✅ **Clean Form Interface**: Modern, responsive design with TailwindCSS
- ✅ **Dynamic Categories**: Automatically loads categories from the backend API
- ✅ **Smart Subcategories**: Dynamically updates subcategory options based on selected category
- ✅ **Question Type Support**: Dropdown for open, true/false, image, video, and audio questions
- ✅ **File Upload**: Support for media files with type-specific validation
- ✅ **Real-time Validation**: Client-side and server-side validation with helpful error messages
- ✅ **API Status Indicator**: Shows connection status to the backend
- ✅ **Auto-save**: Automatically saves form data locally to prevent data loss

## Technology Stack

- **HTML5** - Semantic markup
- **TailwindCSS** - Utility-first CSS framework (via CDN)
- **Vanilla JavaScript** - No build step required
- **Nginx** - Web server for serving static files
- **Docker** - Containerized deployment

## File Structure

```
frontend/
├── index.html      # Main form interface
├── app.js          # JavaScript application logic
├── nginx.conf      # Nginx server configuration
└── README.md       # This file
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- **GET /categories** - Fetches available categories and subcategories
- **POST /questions/** - Submits new quiz questions
- **GET /health** - Checks API connection status

## Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Question Text | Textarea | Yes | The quiz question text |
| Answer Text | Input | Yes | The correct answer |
| Question Type | Select | Yes | open, true_false, image, video, audio |
| Category | Select | Yes | Main category (loaded from API) |
| Subcategory | Select | Yes | Subcategory (filtered by category) |
| Media File | File | No | Optional media file for image/video/audio questions |

## Features

### Dynamic Subcategories
When a category is selected, the subcategory dropdown automatically updates with relevant options.

### Media Upload
- Shows/hides based on question type selection
- File type validation (images for image questions, etc.)
- File size limit (10MB)
- Preview of selected file

### Auto-save
- Automatically saves form data to localStorage
- Restores data on page reload
- Clears saved data after successful submission

### Error Handling
- Network connection errors
- API validation errors
- File upload errors
- Form validation errors

## Usage

1. **Access the form**: Open http://localhost:3000
2. **Fill in question details**: Enter question and answer text
3. **Select question type**: Choose from dropdown options
4. **Pick category**: Select from available categories
5. **Choose subcategory**: Pick from filtered subcategories
6. **Upload media** (optional): Add image/video/audio for media question types
7. **Submit**: Click "Add Question" to save to database

## Development

The frontend is served via Docker using nginx. No build step is required - all dependencies are loaded via CDN.

### Local Development
```bash
# Start all services
docker-compose up --build

# Access frontend
open http://localhost:3000
```

### File watching
Since the frontend files are mounted as volumes, changes to HTML/CSS/JS files are immediately reflected without rebuilding the container.

## Browser Support

- Chrome/Chromium 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Security Features

- CORS protection
- XSS protection headers
- Content type validation
- File size limits
- Input sanitization 