# DataForge - Data Annotation Platform

![DataForge](https://img.shields.io/badge/DataForge-Data%20Annotation-blue)
![Python](https://img.shields.io/badge/Python-38.5%25-brightgreen)
![HTML](https://img.shields.io/badge/HTML-38.1%25-orange)
![CSS](https://img.shields.io/badge/CSS-17.7%25-red)
![JavaScript](https://img.shields.io/badge/JavaScript-5.7%25-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Overview

**DataForge** is a comprehensive AI/ML Data Annotation Platform designed to streamline the data preparation pipeline for machine learning projects. It empowers development teams to efficiently prepare, organize, and label datasets for training modern AI algorithms.

The platform provides an intuitive web interface for annotators to label raw data (images, text, etc.) while giving project managers powerful tools to manage datasets, track progress, and export annotated data in multiple formats.

### Key Highlights
- 🚀 **Fast & Efficient**: Streamline your data labeling workflow
- 🔐 **Secure**: Role-based access control with user authentication
- 📊 **Real-Time Tracking**: Monitor labeling progress on an interactive dashboard
- 🔄 **Concurrency Control**: Prevent duplicate labeling with intelligent task assignment
- 📤 **Flexible Export**: Export labeled data as CSV or JSON
- 🎯 **Quality Assurance**: Built-in label verification and data filtering

---

## 🎯 Features

### 1. **Dataset Upload and Management**
   - Upload raw datasets (images, text files, etc.)
   - Organize data into projects and batches
   - Preview and validate data before labeling
   - Filter and remove corrupted data

### 2. **Dynamic Data Labeling Interface**
   - Intuitive, responsive web interface for annotators
   - Support for multiple annotation types (classification, tagging, etc.)
   - Keyboard shortcuts and quick actions for faster labeling
   - Automatic data progression after labeling

### 3. **Role-Based Access Control (RBAC)**
   - **Admin**: Full control over datasets, users, and projects
   - **Annotator**: Access to assigned labeling tasks
   - Granular permission management
   - Secure user authentication and profiles

### 4. **Automated Task Assignment Logic**
   - Intelligent work distribution among annotators
   - Prevent duplicate labeling of same data points
   - Load balancing across team members
   - Optional redundancy for quality assurance

### 5. **Real-Time Progress Dashboard**
   - Visual progress tracking for each project
   - Statistics on labeling completion rates
   - Annotator performance metrics
   - Real-time notifications and alerts

### 6. **Annotated Data Export**
   - Export labeled data in multiple formats (CSV, JSON)
   - Customizable export fields
   - Batch export capabilities
   - Metadata preservation

### 7. **Label Verification and Editing**
   - Review and edit labels before export
   - Comparison tools for quality assurance
   - Undo/redo functionality
   - Change history and audit logs

### 8. **Corrupted Data Filtering**
   - Automatic detection of invalid or corrupted files
   - Manual marking for data removal
   - Validation rules and constraints
   - Data integrity reports

### 9. **User Authentication and Profiles**
   - Secure login with password hashing
   - User profile management
   - Password reset and account recovery
   - Session management and logout

### 10. **Concurrency Control**
   - Lock mechanism to prevent simultaneous labeling
   - Database transaction management
   - Conflict resolution
   - Activity logging

---

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup and structure
- **CSS3**: Responsive design and styling
- **JavaScript**: Dynamic interactivity and client-side logic

### Backend
- **Django**: Python web framework for robust server-side logic
- **Django REST Framework**: RESTful API development

### Database
- **MySQL**: Relational database for persistent data storage

### Additional Technologies
- **REST API**: Standard HTTP-based communication protocol
- **AJAX**: Asynchronous data loading for seamless UX

---

## 📦 Project Structure

```
DataForge-Data-Annotation-Platform/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/
│   │   ├── projects/
│   │   ├── datasets/
│   │   ├── annotations/
│   │   └── tasks/
│   └── static/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── app.js
│   │   ├── auth.js
│   │   ├── dashboard.js
│   │   └── labeling.js
│   └── assets/
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── INSTALLATION.md
│   └── USER_GUIDE.md
├── tests/
│   ├── unit/
│   └── integration/
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL 5.7+
- Node.js 14+ (for frontend development)
- Git

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/imtiaz-techie/DataForge-Data-Annotation-Platform.git
cd DataForge-Data-Annotation-Platform
```

#### 2. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with database configuration
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### 3. Set Up Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Open in your preferred code editor and ensure all paths are correct
# No build step required for vanilla HTML/CSS/JS setup
```

#### 4. Configure Database

Update the `backend/config/settings.py` file with your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dataforge_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 5. Access the Application

- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api

---

## 🔐 User Roles and Permissions

### Admin (Project Manager)
- ✅ Upload and manage datasets
- ✅ Create and configure annotation projects
- ✅ Assign tasks to annotators
- ✅ Monitor progress in real-time
- ✅ Review and verify labels
- ✅ Export annotated data
- ✅ Manage user accounts
- ✅ View analytics and reports

### Annotator
- ✅ View assigned labeling tasks
- ✅ Label data points with provided tags
- ✅ Submit completed annotations
- ✅ View personal progress
- ✅ Access user profile and settings

---

## 📚 API Documentation

The platform uses a RESTful API for all backend operations. Comprehensive API documentation is available at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **Detailed Documentation**: See [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

### Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| GET | `/api/projects/` | List all projects |
| POST | `/api/projects/` | Create new project |
| GET | `/api/datasets/` | List datasets |
| POST | `/api/datasets/upload` | Upload dataset |
| GET | `/api/tasks/` | Get assigned tasks |
| POST | `/api/annotations/` | Submit annotation |
| GET | `/api/export/` | Export labeled data |

---

## 💡 Usage Examples

### For Administrators

1. **Create a New Project**
   - Log in to the admin dashboard
   - Click "New Project"
   - Enter project details and annotation guidelines
   - Upload dataset CSV/JSON file

2. **Monitor Labeling Progress**
   - Access the real-time dashboard
   - View completion percentage per annotator
   - Identify bottlenecks and reassign tasks

3. **Export Labeled Data**
   - Navigate to project settings
   - Click "Export Data"
   - Select format (CSV/JSON)
   - Download the annotated dataset

### For Annotators

1. **Label Data**
   - Log in to your account
   - View assigned tasks on dashboard
   - Click on a task to open the labeling interface
   - Apply appropriate tags/labels to data
   - Submit your work

2. **Track Progress**
   - View personal progress bar
   - See completed vs. pending tasks
   - Check performance metrics

---

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
# Backend tests
cd backend
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🤝 Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

---

## 📋 Requirements

### Backend Dependencies

See `backend/requirements.txt`:
```
Django>=4.0
djangorestframework>=3.13
django-cors-headers>=3.11
mysql-connector-python>=8.0
python-dotenv>=0.19
Pillow>=9.0
```

### System Requirements

- **Disk Space**: Minimum 2GB (depends on dataset size)
- **RAM**: Minimum 2GB for development, 4GB+ for production
- **CPU**: Multi-core processor recommended for concurrent operations

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Database connection refused
- **Solution**: Verify MySQL is running and credentials in `.env` are correct

**Issue**: Static files not loading
- **Solution**: Run `python manage.py collectstatic` in backend directory

**Issue**: CORS errors in API calls
- **Solution**: Ensure `CORS_ALLOWED_ORIGINS` is configured in Django settings

**Issue**: Port already in use
- **Solution**: Run server on different port: `python manage.py runserver 8001`

For more troubleshooting, see [INSTALLATION.md](docs/INSTALLATION.md)

---

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [User Guide](docs/USER_GUIDE.md)
- [Architecture Overview](docs/ARCHITECTURE.md)

---

## 🔒 Security

- Password hashing using Django's built-in authentication
- CSRF protection on all forms
- SQL injection prevention through ORM
- XSS protection via template escaping
- Secure session management
- Role-based access control enforcement

**Note**: Always run in production mode with `DEBUG=False` and use environment variables for sensitive data.

---

## 📊 Project Statistics

- **Language Composition**:
  - Python: 38.5%
  - HTML: 38.1%
  - CSS: 17.7%
  - JavaScript: 5.7%
- **Repository**: https://github.com/imtiaz-techie/DataForge-Data-Annotation-Platform
- **License**: MIT

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Core annotation features
- ✅ User authentication and RBAC
- ✅ Basic data export

### Version 1.1 (Planned)
- 🔄 Collaborative labeling with inter-annotator agreement metrics
- 🔄 Advanced filtering and search
- 🔄 Batch operations

### Version 2.0 (Future)
- 🔄 Machine learning model integration for active learning
- 🔄 Multi-language support
- 🔄 Mobile app
- 🔄 Cloud storage integration (S3, GCS)
- 🔄 Advanced analytics and reporting

---

## 📞 Support and Contact

For issues, questions, or suggestions:

- **GitHub Issues**: [Open an issue](https://github.com/imtiaz-techie/DataForge-Data-Annotation-Platform/issues)
- **Email**: imtiaz-techie@example.com
- **Documentation**: Check the [docs](docs/) folder

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- API development using [Django REST Framework](https://www.django-rest-framework.org/)
- Database management with [MySQL](https://www.mysql.com/)
- Community feedback and contributions

---

## 📈 Performance

Optimized for:
- **Concurrent Users**: Up to 100 simultaneous annotators
- **Dataset Size**: Supports datasets with 100K+ data points
- **Label Submission**: Sub-second response times
- **Data Export**: Batch processing for large exports

---

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Guide](https://www.django-rest-framework.org/)
- [MySQL Best Practices](https://dev.mysql.com/)
- [Modern JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

---

**Last Updated**: 2026-05-02

Made with ❤️ by the DataForge Team
