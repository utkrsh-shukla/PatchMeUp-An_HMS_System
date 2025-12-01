# PatchMeUp Hospital Management System

A comprehensive Flask-based web application for hospital management with role-based access control for Admins, Doctors, and Patients. Features a professional beige and red themed interface with complete treatment management capabilities. Built with modularity in mind, featuring clear structure and organized code architecture.

## 🏥 Features Overview

### 👨‍💼 Admin Features
- **Dashboard Analytics**: Real-time statistics (doctors, patients, appointments)
- **Doctor Management**: Complete CRUD operations with department assignment
- **Patient Management**: View, edit, and manage patient records
- **User Administration**: Activate/deactivate accounts, role management
- **Advanced Search**: Search across doctors and patients with filters
- **Appointment Oversight**: Monitor all appointments and statuses
- **Data Security**: Permanent deletion vs. soft deactivation options

### 👨‍⚕️ Doctor Features
- **Smart Dashboard**: Upcoming appointments with treatment status indicators
- **Appointment Management**: Mark complete, cancel, reschedule appointments
- **Treatment Records**: 
  - Add comprehensive treatment records (diagnosis, prescription, notes)
  - Edit and update existing treatments
  - View complete treatment details
- **Patient History**: Access complete medical history for assigned patients
- **Availability Management**: Set weekly schedules with time slots
- **Treatment Timeline**: Track patient progress over multiple visits

### 👤 Patient Features
- **Doctor Discovery**: Browse doctors by department with active status filtering
- **Smart Booking**: 
  - View doctor availability for next 7 days
  - Conflict prevention system
  - Real-time availability checking
- **Appointment Management**: View upcoming and past appointments
- **Medical Records Access**:
  - View detailed treatment records
  - Complete medical history timeline
  - Print-friendly treatment summaries
- **Profile Management**: Update personal and medical information
- **Treatment Tracking**: Monitor diagnosis, prescriptions, and follow-ups

## 🛠️ Technology Stack

- **Backend Framework**: Flask 3.0 with Blueprint architecture
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Authentication**: Flask-Login with session management
- **Forms & Validation**: Flask-WTF, WTForms with custom validators
- **Frontend**: Bootstrap 5 with responsive design
- **Styling**: Custom CSS with professional beige/red theme
- **Icons**: Bootstrap Icons for consistent UI
- **Security**: CSRF protection, password hashing, role-based access

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or extract the project**
   ```bash
   cd hospital_management_system
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```
   
   This will create the SQLite database, all tables, a default admin user, and sample departments.

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## Default Credentials

### Admin Account
- **Email**: admin@hospital.com
- **Password**: admin123

⚠️ **IMPORTANT**: Change the admin password after first login!

## 📋 Usage Guide

### For Admins
1. **Initial Setup**: Login with admin credentials
2. **Doctor Management**: 
   - Add doctors with department assignments
   - Set default availability schedules
   - Manage doctor accounts (activate/deactivate/delete)
3. **Patient Oversight**: View and manage patient records
4. **System Monitoring**: 
   - Monitor appointment statistics
   - Search across all users
   - Handle user account issues

### For Doctors
1. **Account Setup**: Receive credentials from admin
2. **Schedule Management**: Set weekly availability schedules
3. **Appointment Handling**:
   - View today's and upcoming appointments
   - Mark appointments as completed or cancelled
4. **Treatment Management**:
   - Add detailed treatment records after consultations
   - Edit and update existing treatments
   - View complete patient medical history
5. **Patient Care**: Access comprehensive patient information and history

### For Patients
1. **Registration**: Create account with medical information
2. **Doctor Selection**:
   - Browse doctors by department/specialization
   - View doctor profiles and availability
3. **Appointment Booking**:
   - Check 7-day availability calendar
   - Book appointments with conflict prevention
4. **Medical Records**:
   - View detailed treatment records
   - Access complete medical history
   - Print treatment summaries
5. **Profile Management**: Update personal and medical information

## Project Structure

```
hospital_management_system/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   ├── models/                  # Database models
│   ├── routes/                  # Route handlers (blueprints)
│   ├── forms/                   # WTForms
│   ├── decorators/              # Custom decorators
│   ├── utils/                   # Utility functions
│   ├── templates/               # Jinja2 templates
│   └── static/                  # CSS, JS files
├── instance/
│   └── hospital.db              # SQLite database (created automatically)
├── init_db.py                   # Database initialization script
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🗄️ Database Schema

- **User**: Base authentication model with role-based access
- **Doctor**: Doctor profiles with department association and specializations
- **Patient**: Patient profiles with comprehensive medical information
- **Department**: Medical departments/specializations with active doctor counts
- **Appointment**: Appointment bookings with conflict prevention and status tracking
- **Treatment**: Detailed medical treatment records (diagnosis, prescription, notes)
- **Availability**: Doctor availability schedules with time slot management

### Key Relationships
- User → Doctor/Patient (One-to-One with cascade delete)
- Doctor → Department (Many-to-One)
- Doctor → Appointments (One-to-Many)
- Doctor → Availability (One-to-Many)
- Patient → Appointments (One-to-Many)
- Appointment → Treatment (One-to-One)

## 🔑 Key Features

### Advanced Appointment System
- **Conflict Prevention**: Automatic double-booking prevention with database constraints
- **Real-time Availability**: 7-day availability calendar with time slot management
- **Status Tracking**: Complete appointment lifecycle (booked → completed/cancelled)
- **Smart Validation**: Custom validators for appointment conflicts and doctor availability

### Comprehensive Treatment Management
- **CRUD Operations**: Full create, read, update capabilities for treatments
- **Detailed Records**: Diagnosis, prescription, and clinical notes
- **Patient Access**: Patients can view their complete treatment history
- **Print Functionality**: Print-friendly treatment records and medical history

### Role-Based Security
- **Custom Decorators**: `@admin_required`, `@doctor_required`, `@patient_required`
- **Data Protection**: Users can only access their authorized data
- **Active Status Filtering**: Inactive doctors hidden from patient booking
- **Secure Authentication**: Password hashing and session management

### User Experience Features
- **Responsive Design**: Mobile-friendly interface
- **Professional Theme**: Consistent beige/red hospital branding
- **Intuitive Navigation**: Role-specific menus and dashboards
- **Real-time Feedback**: Flash messages and form validation
- **Print Support**: Medical records optimized for printing

## 🔒 Security Features

- **Password Security**: Werkzeug password hashing with salt
- **CSRF Protection**: All forms protected against cross-site request forgery
- **Session Management**: Secure session handling with Flask-Login
- **Role-Based Access**: Multi-layer authorization system
- **Data Isolation**: Users can only access their authorized data
- **Account Management**: Both soft delete (deactivation) and permanent deletion
- **Input Validation**: Comprehensive form validation and sanitization
- **Active Status Filtering**: Inactive users automatically filtered from patient-facing features

## 🔧 Troubleshooting

### Database Issues
If you encounter database errors, reinitialize the database:
```bash
python init_db.py
```
**Note**: This will reset all data and recreate the default admin account.

### Port Already in Use
If port 5000 is in use, edit `run.py` and change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change port here
```

### Missing Dependencies
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### SQLAlchemy Errors
If you encounter relationship or query errors:
1. Check that all models are properly imported
2. Ensure foreign key relationships are correctly defined
3. Reinitialize the database if schema changes were made

### Template Not Found Errors
Ensure all template files are in the correct directory structure under `app/templates/`

## 🚀 Development

### Running in Development Mode
```bash
python run.py
```

Development mode provides:
- **Auto-reload**: Automatic restart on code changes
- **Debug Pages**: Detailed error information
- **Interactive Debugger**: In-browser debugging tools
- **SQL Query Logging**: Database query monitoring

### Code Structure Guidelines
- **Modular Design**: Separate blueprints for different modules
- **Clean Architecture**: Models, routes, forms, and templates separated
- **Consistent Naming**: Clear, descriptive function and variable names
- **Documentation**: Comprehensive docstrings and comments

### Adding New Features
1. Create models in `app/models/`
2. Add routes in `app/routes/` using blueprints
3. Create forms in `app/forms/`
4. Design templates in `app/templates/`
5. Update navigation in `base.html`

## 📊 System Statistics

- **Total Files**: 50+ organized files
- **Database Tables**: 7 interconnected tables
- **User Roles**: 3 distinct role types
- **Templates**: 20+ responsive HTML templates
- **Routes**: 30+ protected endpoints
- **Security Layers**: Multiple validation and authorization levels

## 🎯 Future Enhancements

- **Appointment Reminders**: Email/SMS notifications
- **Payment Integration**: Billing and payment processing
- **Reporting System**: Advanced analytics and reports
- **Mobile App**: React Native or Flutter mobile application
- **Telemedicine**: Video consultation integration
- **Inventory Management**: Medical supplies tracking

## 📄 License

This project is free to use for educational and personal purposes. 
⭐ **Please give it a star if you find it helpful!**

## 🤝 Contributing

Contributions are welcome! Whether it's:
- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- 🔧 Code optimization

Feel free to open issues or submit pull requests.

## 📞 Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact for collaboration opportunities

---

**PatchMeUp Hospital Management System** - Revolutionizing healthcare delivery through technology 🏥✨
