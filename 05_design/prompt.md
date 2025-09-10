Create Vue.js UI for FastAPI Backend

## Objective
You are an AI agent tasked with creating a modern, responsive user interface for a FastAPI backend application. The UI should be built using Vue.js and Vite, following the provided Figma design specifications.

## Project Structure Requirements
- **UI Location**: Create all UI files in the `05_design` folder
- **Backend Reference**: Available API endpoints are documented in `03_python_fastapi_project/readme.md`
- **Technology Stack**: Vite + Vue.js (latest stable versions)

## Technical Specifications

### 1. Setup Instructions
- Initialize a new Vite + Vue.js project in the `05_design` folder
- Configure the project with:
  - TypeScript support (if applicable)
  - Vue Router for navigation
  - Axios or Fetch API for HTTP requests
  - Tailwind CSS or your preferred styling framework
  - Any necessary UI component libraries (e.g., Vuetify, Quasar, Element Plus)

### 2. API Integration Requirements
- **Endpoint Discovery**: Read and analyze all available endpoints from `03_python_fastapi_project/readme.md`
- **HTTP Client Setup**: Create a centralized API service/client
- **Error Handling**: Implement comprehensive error handling for API calls
- **Loading States**: Add loading indicators for all async operations
- **Data Validation**: Ensure proper request/response data validation

### 3. Figma Design Integration
- **Access Method**: Use MCP (Model Context Protocol) via FrameLink.ai
- **Documentation Reference**: Follow the quickstart guide at https://www.framelink.ai/docs/quickstart
- **Design Fidelity**: Maintain high fidelity to the Figma designs
- **Responsive Design**: Ensure the UI works across desktop, tablet, and mobile devices
- **Figma design**: https://figma.com/design/Cep7R0EjWIdbO4GEzcAkti/Product-Management-Mockup---Codespring-LLM-Training

## Implementation Steps

### Step 1: Project Initialization
1. Set up Vite + Vue.js project in `05_design` folder
2. Install necessary dependencies
3. Configure build tools and development environment
4. Set up project structure with proper folder organization

### Step 2: Figma Design Analysis
1. Connect to Figma using MCP and FrameLink.ai
2. Extract design specifications including:
   - Color palette and typography
   - Component layouts and spacing
   - Interactive states and animations
   - Responsive breakpoints
3. Create a design system/style guide based on Figma specs

### Step 3: API Documentation Analysis
1. Read `03_python_fastapi_project/readme.md` thoroughly
2. Document all available endpoints with:
   - HTTP methods (GET, POST, PUT, DELETE, etc.)
   - Request/response schemas
   - There is no Authentication
   - Query parameters and path variables
3. Create TypeScript interfaces/types for API data models

### Step 4: Core Development
1. **Router Setup**: Configure Vue Router with all necessary routes
2. **API Service Layer**: Create reusable API service functions
3. **Component Development**: Build Vue components matching Figma designs
4. **State Management**: Implement Pinia or Vuex if complex state is needed
5. **Form Handling**: Create forms for data input with proper validation

### Step 5: UI/UX Implementation
1. **Styling**: Implement the design system from Figma
2. **Animations**: Add smooth transitions and micro-interactions
3. **Accessibility**: Ensure WCAG compliance
4. **Performance**: Optimize for fast loading and smooth interactions

### Step 6: Testing & Optimization
1. Test all API integrations
2. Verify responsive design across devices
3. Test user flows and edge cases
4. Optimize bundle size and performance

## Required Features

### Core Functionality
- [ ] CRUD operations for all relevant entities
- [ ] Data visualization (charts, tables, lists)
- [ ] Search and filtering capabilities
- [ ] Pagination for large datasets

### UI/UX Features
- [ ] Responsive design (mobile-first approach)
- [ ] Dark/light theme toggle (if in Figma design)
- [ ] Loading states and skeleton screens
- [ ] Error states and user feedback
- [ ] Form validation with clear error messages
- [ ] Confirmation dialogs for destructive actions

### Technical Features
- [ ] Environment configuration (dev/staging/prod)
- [ ] API base URL configuration
- [ ] Request/response interceptors
- [ ] Caching strategy for API responses
- [ ] Offline support (if applicable)

## Deliverables

### 1. Complete Vue.js Application
- Fully functional UI in `05_design` folder
- All components matching Figma designs
- Complete API integration with FastAPI backend

### 2. Documentation
- README.md with setup and development instructions
- API integration documentation
- Component documentation
- Deployment guide

### 3. Configuration Files
- Proper Vite configuration
- Environment variables setup
- Package.json with all dependencies
- ESLint/Prettier configuration (if applicable)

## Quality Standards

### Code Quality
- Follow Vue.js best practices and composition API patterns
- Use TypeScript for type safety (recommended)
- Implement proper error boundaries
- Write clean, maintainable, and well-documented code
- Follow consistent naming conventions

### Performance
- Optimize images and assets
- Implement code splitting and lazy loading
- Minimize bundle size
- Ensure fast initial load times
- Use efficient rendering patterns

### Security
- Sanitize user inputs
- Implement proper authentication flows
- Secure API communication
- Handle sensitive data appropriately

## Getting Started Command Sequence

```bash
# Navigate to project root
cd 05_design

# Initialize Vite + Vue project
npm create vue@latest . 
# or
yarn create vue .

# Install dependencies
npm install
# or
yarn install

# Start development server
npm run dev
# or
yarn dev
```

## Additional Considerations

1. **MCP Setup**: Ensure you have proper access to the Figma design via FrameLink.ai MCP
2. **API Testing**: Test all API endpoints manually before integration
3. **Version Control**: Use Git with meaningful commit messages
4. **Cross-browser Testing**: Ensure compatibility across major browsers
5. **Accessibility**: Test with screen readers and keyboard navigation

## Success Criteria

The project will be considered successful when:
- All API endpoints are properly integrated
- UI matches Figma designs with pixel-perfect accuracy
- Application is fully responsive and accessible
- All user flows work seamlessly
- Code is well-structured and maintainable
- Documentation is complete and clear

---
