# Gym Management System

A comprehensive gym management system built with Django and React, designed to streamline gym operations with specific roles for admins, experts, trainers, and users.

## Features

### Admin Features
- Expert management
- Trainer management
- Event management
- Batch management
- View users
- Allocate batch to user
- Allocate batch to trainer
- View fee
- Send payment alert
- View payment reports
- Change password

### Trainer Features
- View profile
- View allocated batch
- View members
- Attendance management
- Update health details
- Chat with user
- Change password

### Expert Features
- View and edit profile
- Video management
- Tips management
- Chat with user
- Change password

### User Features
- Register
- Login
- View profile
- View trainer
- View attendance
- Chat with trainer
- View health details
- View expert
- View videos
- View tips
- View event
- View payment alert
- Make payment
- Change password

## Installation

### Prerequisites
- Python 3.8+
- MySQL
- Node.js and npm

### Backend Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/gym-management-system.git
cd gym-management-system
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create MySQL database:
```
mysql -u root -p
CREATE DATABASE gym_management_system;
exit;
```

5. Update database settings in `gym_management_system/settings.py` if needed.

6. Run migrations:
```
cd gym_management_system
python manage.py migrate
```

7. Create a superuser:
```
python manage.py createsuperuser
```

8. Run the server:
```
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install dependencies:
```
npm install
```

3. Start the development server:
```
npm run dev
```

## API Documentation

The API documentation is available at `/api/docs/` when the server is running.

## License

This project is licensed under the MIT License - see the LICENSE file for details.