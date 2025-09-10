# Product Management UI

A modern, responsive user interface for managing products, built with Vue 3, TypeScript, and Vite. This UI connects to a FastAPI backend and implements a pixel-perfect design from Figma.

## Features

- 📱 Responsive layout that works on desktop, tablet, and mobile
- 🎨 Pixel-perfect implementation of Figma design
- 🔍 Real-time product search functionality
- ✨ Modern, clean UI with smooth interactions
- 📊 Product management with CRUD operations
- 🚀 Fast and optimized performance

## Tech Stack

- **Framework**: Vue 3 with TypeScript
- **Build Tool**: Vite
- **Routing**: Vue Router
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Backend**: FastAPI (running on `http://localhost:8000`)

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

   The development server will start at `http://localhost:5173`

3. **Build for Production**
   ```bash
   npm run build
   # or
   yarn build
   ```

## Project Structure

```
src/
├── api/            # API client and endpoints
├── assets/         # Static assets and icons
├── components/     # Reusable Vue components
├── router/        # Vue Router configuration
├── views/         # Page components
└── App.vue        # Root component
```

## Features and Pages

### Product List
- Grid layout displaying all products
- Real-time search functionality
- Quick actions: View, Edit, Delete
- Product information including name, description, stock, and price

### Product Details
- Detailed view of individual products
- Complete product information
- Edit and delete capabilities

### Create/Edit Product
- Form for adding new products
- Validation and error handling
- Real-time feedback

## Design System

The UI implements a custom design system with the following key elements:

### Colors
- Primary Text: `#0A0A0A`
- Secondary Text: `#717182`
- Background: `#F3F3F5`
- Accent: `#D4183D`
- Border: `rgba(0, 0, 0, 0.1)`

### Typography
- Primary Font: Inter
- Font Sizes: 10.7px - 13.2px
- Various weights for different contexts

### Components
- Cards with `12.75px` border radius
- Buttons with `6.75px` border radius
- Custom form inputs
- Specialized action buttons with icons

## Development

### Prerequisites
- Node.js 16+
- npm or yarn
- Running FastAPI backend (see `03_python_fastapi_project`)

### Backend Connection
The UI expects the backend to be running at `http://localhost:8000`. Make sure the FastAPI server is running before starting the UI.

### Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build
- `npm run test`: Run tests
- `npm run lint`: Lint code

## Contributing

1. Ensure you have the latest changes
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes.
