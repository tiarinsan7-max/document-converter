# Web UI Documentation

Complete guide for using the Streamlit and React web interfaces.

---

## 🎨 Streamlit UI

### Starting Streamlit

```bash
# Using main.py
python main.py streamlit

# Using streamlit directly
streamlit run streamlit_app/app.py

# Custom port
streamlit run streamlit_app/app.py --server.port 8501
```

Access at: **http://localhost:8501**

---

### Features

#### 1. **Single File Conversion**
- Drag & drop file upload
- Select output format
- Choose quality level
- One-click conversion
- Instant download

#### 2. **Batch Conversion**
- Upload multiple files
- Convert all to same format
- Progress tracking
- Individual file downloads
- Error reporting

#### 3. **Workflows** (Multi-page)
- Create automated workflows
- Schedule conversions
- Manage workflows
- Run workflows on demand

#### 4. **About Page**
- Supported formats
- Conversion matrix
- Documentation links
- Version information

---

### Usage Guide

#### Single File Conversion

1. **Upload File:**
   - Click "Choose a file to convert"
   - Or drag & drop file into upload area

2. **Select Format:**
   - Choose output format from dropdown
   - Available formats shown based on input

3. **Set Quality:**
   - Use sidebar slider
   - Options: Low, Medium, High

4. **Convert:**
   - Click "🚀 Convert File"
   - Wait for progress bar
   - Download button appears

5. **Download:**
   - Click "⬇️ Download Converted File"
   - File saves to your downloads folder

#### Batch Conversion

1. **Upload Files:**
   - Click "Choose files to convert"
   - Select multiple files
   - Or drag & drop multiple files

2. **Select Format:**
   - Choose output format for all files

3. **Convert:**
   - Click "🚀 Convert All to [FORMAT]"
   - Progress bar shows overall progress

4. **Download:**
   - Individual download buttons for each file
   - Download successful conversions

#### Workflows

1. **Create Workflow:**
   - Go to "📋 Workflows" page
   - Fill in workflow details:
     - Name
     - Input directory
     - Output directory
     - Output format
     - Quality
     - Recursive option
   - Click "Create Workflow"

2. **Run Workflow:**
   - Go to "▶️ Run Workflows" tab
   - Click "▶️ Run [workflow name]"
   - View results

3. **Manage Workflows:**
   - Go to "📊 Manage Workflows" tab
   - Enable/Disable workflows
   - View details
   - Delete workflows

---

### Configuration

#### Sidebar Settings

- **Conversion Mode:** Single File / Batch / About
- **Quality:** Low / Medium / High
- **Supported Formats:** View all formats
- **Statistics:** Format count, conversion count

#### Custom Styling

Edit `streamlit_app/app.py` to customize:
- Colors
- Fonts
- Layout
- Components

---

## ⚛️ React UI

### Starting React App

```bash
# Install dependencies (first time only)
cd web
npm install

# Start development server
npm start

# Build for production
npm run build
```

Access at: **http://localhost:3000**

---

### Features

#### 1. **Modern Interface**
- Clean, responsive design
- Chakra UI components
- Smooth animations
- Mobile-friendly

#### 2. **Drag & Drop**
- Intuitive file upload
- Visual feedback
- Multiple file support
- File size display

#### 3. **Real-time Progress**
- Upload progress
- Conversion progress
- Status updates
- Error handling

#### 4. **Tabbed Interface**
- Convert tab
- Formats tab
- About tab

---

### Usage Guide

#### Convert Tab

1. **Upload Files:**
   - Drag files into upload area
   - Or click to browse
   - Multiple files supported

2. **Configure:**
   - Select output format
   - Choose quality level

3. **Convert:**
   - Click "🚀 Convert Files"
   - Watch progress bar

4. **Download:**
   - Click download button for each file
   - Files download automatically

#### Formats Tab

- View all supported formats
- See format descriptions
- Check file extensions
- View conversion statistics

#### About Tab

- Application information
- Feature list
- Technology stack
- Version details

---

### API Integration

React app connects to FastAPI backend:

```javascript
// API base URL (configured in package.json proxy)
const API_URL = '/api/v1';

// Convert file
const formData = new FormData();
formData.append('file', file);
formData.append('output_format', 'pdf');
formData.append('quality', 'high');

const response = await axios.post(`${API_URL}/convert`, formData);
```

---

### Customization

#### Theme

Edit `web/src/App.js`:

```javascript
<ChakraProvider theme={customTheme}>
  {/* App content */}
</ChakraProvider>
```

#### Colors

Modify Chakra UI color scheme:
- `colorScheme="blue"` → Change to any Chakra color
- Custom colors in theme configuration

#### Components

Add new components in `web/src/components/`:
```
web/src/components/
├── FileUploader.js
├── ConversionSettings.js
├── ResultsList.js
└── ...
```

---

## 📊 Comparison

| Feature | Streamlit | React |
|---------|-----------|-------|
| **Setup** | Simple (Python only) | Requires Node.js |
| **Development** | Fast prototyping | More control |
| **Customization** | Limited | Highly customizable |
| **Performance** | Good | Excellent |
| **Mobile** | Responsive | Fully responsive |
| **Workflows** | Built-in | Requires implementation |
| **Best For** | Quick deployment | Production apps |

---

## 🚀 Deployment

### Streamlit

#### Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy from repository

#### Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "streamlit_app/app.py"]
```

### React

#### Build for Production

```bash
cd web
npm run build
```

#### Serve with Nginx

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    root /path/to/web/build;
    index index.html;
    
    location / {
        try_files $uri /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

#### Deploy to Vercel/Netlify

1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Deploy

---

## 🔧 Troubleshooting

### Streamlit Issues

**Issue:** Port already in use
```bash
streamlit run streamlit_app/app.py --server.port 8502
```

**Issue:** Module not found
```bash
# Make sure you're in project root
cd /path/to/Cline
streamlit run streamlit_app/app.py
```

**Issue:** File upload fails
- Check file size limits in config
- Verify file format is supported

### React Issues

**Issue:** npm install fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue:** API calls fail
- Ensure backend is running on port 8000
- Check proxy configuration in package.json

**Issue:** Build fails
```bash
# Clear build cache
rm -rf build
npm run build
```

---

## 📱 Mobile Support

### Streamlit
- Automatically responsive
- Touch-friendly controls
- Mobile-optimized layout

### React
- Chakra UI responsive breakpoints
- Mobile-first design
- Touch gestures supported

---

## 🎨 Screenshots

### Streamlit UI

**Main Page:**
- Clean header
- File upload area
- Format selection
- Quality slider
- Convert button

**Batch Mode:**
- Multiple file upload
- Progress tracking
- Individual downloads

**Workflows:**
- Workflow creation form
- Workflow list
- Run controls

### React UI

**Convert Tab:**
- Drag & drop zone
- Settings panel
- Progress bar
- Results list

**Formats Tab:**
- Format cards
- Statistics
- Conversion matrix

---

## 🔐 Security

### File Upload
- Size limits enforced
- Type validation
- Secure file handling

### API Communication
- CORS configured
- Request validation
- Error handling

### Data Privacy
- Files deleted after conversion
- No data stored
- Secure transmission

---

## 📈 Performance

### Optimization Tips

1. **File Size:**
   - Compress large files before upload
   - Use appropriate quality settings

2. **Batch Processing:**
   - Limit concurrent conversions
   - Process in chunks

3. **Caching:**
   - Enable browser caching
   - Cache API responses

4. **Network:**
   - Use CDN for static assets
   - Optimize images

---

## 🆘 Support

### Getting Help

- Check logs in `logs/` directory
- Review browser console for errors
- Test API endpoints directly
- Verify backend is running

### Common Solutions

1. **Conversion fails:**
   - Check file format
   - Verify file isn't corrupted
   - Try different quality setting

2. **Upload fails:**
   - Check file size
   - Verify internet connection
   - Clear browser cache

3. **Download fails:**
   - Check browser download settings
   - Verify file was created
   - Try different browser

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [React Documentation](https://react.dev)
- [Chakra UI Documentation](https://chakra-ui.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

---

**Version:** 1.0.0  
**Last Updated:** 2024
