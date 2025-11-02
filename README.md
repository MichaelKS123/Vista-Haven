# 📚 BookFlow - Library Management System

**Created by Michael Semera**

BookFlow is a comprehensive library management system built with Java, JavaFX, and MySQL. Features complete book inventory management, user registration, lending/return operations, and advanced reporting capabilities. Demonstrates professional relational database integration using JDBC.

---

## ✨ Features

### Core Functionality
- 📚 **Book Management** - Add, edit, delete, search books
- 👥 **User Management** - Register and manage library members
- 📤 **Lending System** - Issue books with due dates
- 📥 **Return System** - Process returns with fine calculation
- 🔍 **Advanced Search** - Search by title, author, ISBN
- 📊 **Dashboard** - Real-time statistics and analytics
- 📋 **Reservation System** - Reserve books when unavailable
- 💰 **Fine Calculation** - Automatic overdue fine calculation

### Technical Features
- ✅ **MySQL Database** - Relational database with proper schema
- ✅ **JDBC Integration** - PreparedStatements for SQL injection prevention
- ✅ **Transaction Management** - ACID properties maintained
- ✅ **JavaFX UI** - Modern graphical interface
- ✅ **CRUD Operations** - Complete Create, Read, Update, Delete
- ✅ **Foreign Key Constraints** - Data integrity enforcement
- ✅ **Connection Pooling Ready** - Scalable architecture
- ✅ **Error Handling** - Robust exception management

---

## 🏗️ System Architecture

### Three-Tier Architecture

```
┌─────────────────────────────────────┐
│   Presentation Layer (JavaFX UI)   │
│   - Dashboard, Forms, Tables        │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│   Business Logic Layer (Java)       │
│   - DatabaseManager                 │
│   - Model Classes                   │
│   - Business Rules                  │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│   Data Layer (MySQL Database)       │
│   - books, users, loans, etc.       │
└─────────────────────────────────────┘
```

---

## 📋 Prerequisites

### Software Requirements
- **Java Development Kit (JDK)** - Version 11 or higher
- **MySQL Server** - Version 5.7 or higher
- **JavaFX SDK** - Version 11 or higher
- **MySQL Connector/J** - JDBC Driver (8.0.x)
- **IDE** - IntelliJ IDEA, Eclipse, or NetBeans

### MySQL Setup

```sql
-- Create database user (optional)
CREATE USER 'bookflow'@'localhost' IDENTIFIED BY 'bookflow123';
GRANT ALL PRIVILEGES ON bookflow.* TO 'bookflow'@'localhost';
FLUSH PRIVILEGES;
```

---

## 🚀 Installation

### Step 1: MySQL Installation

**Windows:**
```
1. Download MySQL Installer from mysql.com
2. Run installer and select "Developer Default"
3. Set root password during installation
4. Complete installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### Step 2: Configure Database Connection

Edit `DatabaseManager.java`:
```java
private static final String DB_URL = "jdbc:mysql://localhost:3306/";
private static final String DB_NAME = "bookflow";
private static final String DB_USER = "root";  // Your MySQL username
private static final String DB_PASSWORD = "your_password";  // Your MySQL password
```

### Step 3: Download MySQL Connector/J

```
1. Visit: https://dev.mysql.com/downloads/connector/j/
2. Download Platform Independent ZIP
3. Extract mysql-connector-j-X.X.XX.jar
4. Note the location for Step 4
```

### Step 4: Project Setup (IntelliJ IDEA)

```
1. File > New > Project
2. Select: Java
3. JDK: 11 or higher
4. Create project

5. Add MySQL Connector:
   File > Project Structure > Libraries
   Click '+' > Java
   Navigate to mysql-connector-j-X.X.XX.jar
   Click OK

6. Add JavaFX:
   File > Project Structure > Libraries
   Click '+' > Java
   Navigate to javafx-sdk/lib folder
   Add all JAR files

7. Configure VM Options:
   Run > Edit Configurations
   VM options:
   --module-path /path/to/javafx-sdk/lib
   --add-modules javafx.controls
```

### Step 5: Project Structure

```
BookFlow/
├── src/
│   └── com/
│       └── michaelsemera/
│           └── bookflow/
│               ├── Main.java
│               ├── DatabaseManager.java
│               ├── Book.java
│               ├── User.java
│               └── Loan.java
└── lib/
    ├── mysql-connector-j-8.0.xx.jar
    └── javafx-sdk/
```

### Step 6: Run the Application

```
1. Right-click Main.java
2. Select "Run Main.main()"
3. Database will be created automatically
4. Sample data will be inserted
5. Application window opens
```

---

## 💾 Database Schema

### Entity-Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    BOOKS     │       │    LOANS     │       │    USERS     │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │◄──────┤ book_id (FK) │       │ id (PK)      │
│ title        │       │ user_id (FK) ├──────►│ name         │
│ author       │       │ issue_date   │       │ email (UQ)   │
│ isbn (UQ)    │       │ due_date     │       │ phone        │
│ publisher    │       │ return_date  │       │ address      │
│ pub_year     │       │ status       │       │ membership   │
│ category     │       │ fine         │       │ reg_date     │
│ total_copies │       └──────────────┘       │ status       │
│ avail_copies │                              └──────────────┘
│ created_at   │
└──────────────┘
```

### Table Definitions

**books**
```sql
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publisher VARCHAR(255),
    publication_year INT,
    category VARCHAR(100),
    total_copies INT DEFAULT 1,
    available_copies INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**users**
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    membership_type ENUM('Basic', 'Premium', 'Student') DEFAULT 'Basic',
    registration_date DATE,
    status ENUM('Active', 'Suspended', 'Inactive') DEFAULT 'Active'
);
```

**loans**
```sql
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status ENUM('Active', 'Returned', 'Overdue') DEFAULT 'Active',
    fine DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**reservations**
```sql
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    status ENUM('Active', 'Fulfilled', 'Cancelled') DEFAULT 'Active',
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🎮 User Guide

### Dashboard

The dashboard provides an overview:

**Statistics Cards:**
- 📚 **Total Books** - Complete inventory count
- ✅ **Available** - Books ready to lend
- 👥 **Users** - Registered members
- 📤 **Active Loans** - Currently borrowed books

**Recent Activity:**
- Latest loan transactions
- Quick access to common operations

### Book Management

**Adding a Book:**
1. Navigate to "Books"
2. Click "➕ Add Book"
3. Fill in details:
   - Title (required)
   - Author (required)
   - ISBN (unique)
   - Publisher
   - Publication Year
   - Category
   - Number of Copies
4. Click OK to save

**Editing a Book:**
1. Select book from table
2. Click "✏️ Edit Book"
3. Modify details
4. Click OK to save changes

**Deleting a Book:**
1. Select book from table
2. Click "🗑️ Delete Book"
3. Confirm deletion
4. Book is permanently removed

**Searching Books:**
- Use search field to find by:
  - Title
  - Author
  - ISBN
- Results update in real-time

### User Management

**Registering a User:**
1. Navigate to "Users"
2. Click "➕ Add User"
3. Enter details:
   - Name
   - Email (must be unique)
   - Phone
   - Address
   - Membership Type
4. Registration date set automatically

**Membership Types:**
- **Basic**: 3 books, 14-day loan period
- **Premium**: 10 books, 30-day loan period
- **Student**: 5 books, 21-day loan period

### Loan Operations

**Issuing a Book:**
1. Navigate to "Loans"
2. Click "📤 Issue Book"
3. Select:
   - Book (from available inventory)
   - User (active members only)
4. System sets:
   - Issue date (today)
   - Due date (based on membership)
5. Book's available copies decreased

**Returning a Book:**
1. Navigate to "Loans"
2. Select active loan from table
3. Click "📥 Return Book"
4. System:
   - Updates loan status to "Returned"
   - Sets return date
   - Calculates fine if overdue
   - Increases available copies

**Fine Calculation:**
```
Fine = Days Overdue × $0.50
Example: 5 days late = $2.50
```

---

## 🔌 JDBC Operations

### Connection Management

```java
// Establish connection
Connection connection = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/bookflow",
    "root",
    "password"
);

// Always close connections
connection.close();
```

### CRUD Examples

**Create (INSERT):**
```java
String sql = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)";
PreparedStatement pstmt = connection.prepareStatement(sql);
pstmt.setString(1, "1984");
pstmt.setString(2, "George Orwell");
pstmt.setString(3, "9780451524935");
pstmt.executeUpdate();
```

**Read (SELECT):**
```java
String sql = "SELECT * FROM books WHERE author = ?";
PreparedStatement pstmt = connection.prepareStatement(sql);
pstmt.setString(1, "George Orwell");
ResultSet rs = pstmt.executeQuery();

while (rs.next()) {
    String title = rs.getString("title");
    System.out.println(title);
}
```

**Update:**
```java
String sql = "UPDATE books SET available_copies = ? WHERE id = ?";
PreparedStatement pstmt = connection.prepareStatement(sql);
pstmt.setInt(1, 5);
pstmt.setInt(2, 1);
pstmt.executeUpdate();
```

**Delete:**
```java
String sql = "DELETE FROM books WHERE id = ?";
PreparedStatement pstmt = connection.prepareStatement(sql);
pstmt.setInt(1, 1);
pstmt.executeUpdate();
```

### Transaction Management

```java
connection.setAutoCommit(false);

try {
    // Multiple operations
    stmt1.executeUpdate();
    stmt2.executeUpdate();
    
    connection.commit();
} catch (SQLException e) {
    connection.rollback();
    throw e;
} finally {
    connection.setAutoCommit(true);
}
```

---

## 🐛 Troubleshooting

### Database Connection Issues

**Error:** `Communications link failure`

**Solutions:**
```bash
# Check MySQL is running
sudo systemctl status mysql  # Linux
brew services list  # macOS
Get-Service MySQL  # Windows PowerShell

# Start MySQL if stopped
sudo systemctl start mysql  # Linux
brew services start mysql  # macOS
net start MySQL  # Windows
```

**Error:** `Access denied for user`

**Solution:**
```sql
-- Reset MySQL root password
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### JDBC Driver Not Found

**Error:** `ClassNotFoundException: com.mysql.cj.jdbc.Driver`

**Solution:**
1. Download MySQL Connector/J
2. Add JAR to project classpath
3. Verify in Project Structure > Libraries

### JavaFX Not Found

**Error:** `Error: JavaFX runtime components are missing`

**Solution:**
```bash
# Add VM options
--module-path /path/to/javafx-sdk/lib
--add-modules javafx.controls
```

### Database Already Exists Error

**Solution:**
```sql
-- Drop and recreate database
DROP DATABASE IF EXISTS bookflow;
CREATE DATABASE bookflow;
```

### Port 3306 Already in Use

**Solution:**
```bash
# Find process using port
lsof -i :3306  # macOS/Linux
netstat -ano | findstr :3306  # Windows

# Change port in my.cnf or use different port
jdbc:mysql://localhost:3307/bookflow
```

---

## 📚 Advanced Features

### Implementing Search with JOIN

```java
public List<Loan> getOverdueLoans() throws SQLException {
    String sql = "SELECT l.*, b.title, u.name FROM loans l " +
                "JOIN books b ON l.book_id = b.id " +
                "JOIN users u ON l.user_id = u.id " +
                "WHERE l.status = 'Active' AND l.due_date < CURDATE()";
    
    PreparedStatement pstmt = connection.prepareStatement(sql);
    ResultSet rs = pstmt.executeQuery();
    
    // Process results...
}
```

### Implementing Aggregation Queries

```java
public Map<String, Integer> getBooksByCategory() throws SQLException {
    Map<String, Integer> stats = new HashMap<>();
    
    String sql = "SELECT category, COUNT(*) as count " +
                "FROM books GROUP BY category";
    
    Statement stmt = connection.createStatement();
    ResultSet rs = stmt.executeQuery(sql);
    
    while (rs.next()) {
        stats.put(rs.getString("category"), rs.getInt("count"));
    }
    
    return stats;
}
```

### Connection Pooling (Production)

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/bookflow");
config.setUsername("root");
config.setPassword("password");
config.setMaximumPoolSize(10);

HikariDataSource dataSource = new HikariDataSource(config);
Connection connection = dataSource.getConnection();
```

---

## 🚀 Future Enhancements

### Planned Features
- [ ] **Barcode Scanner** - Scan ISBN barcodes
- [ ] **Email Notifications** - Overdue reminders
- [ ] **Reports Module** - PDF report generation
- [ ] **Multi-Branch Support** - Multiple library locations
- [ ] **Online Catalog** - Web-based book search
- [ ] **Mobile App** - Android/iOS companion
- [ ] **Fine Payment** - Integrated payment system
- [ ] **Book Reviews** - User ratings and reviews
- [ ] **E-Book Support** - Digital book lending
- [ ] **API Integration** - Google Books API

### Technical Improvements
- [ ] Connection pooling (HikariCP)
- [ ] Prepared statement caching
- [ ] Database indexing optimization
- [ ] Audit logging
- [ ] Backup automation
- [ ] User authentication (Spring Security)
- [ ] REST API (Spring Boot)
- [ ] Unit testing (JUnit)
- [ ] Integration testing
- [ ] CI/CD pipeline

---

## 📊 Sample Queries

### Most Borrowed Books
```sql
SELECT b.title, b.author, COUNT(l.id) as loan_count
FROM books b
JOIN loans l ON b.id = l.book_id
GROUP BY b.id
ORDER BY loan_count DESC
LIMIT 10;
```

### Active Users
```sql
SELECT u.name, u.email, COUNT(l.id) as active_loans
FROM users u
JOIN loans l ON u.id = l.user_id
WHERE l.status = 'Active'
GROUP BY u.id;
```

### Overdue Report
```sql
SELECT u.name, b.title, l.due_date,
    DATEDIFF(CURDATE(), l.due_date) as days_overdue,
    DATEDIFF(CURDATE(), l.due_date) * 0.50 as fine
FROM loans l
JOIN users u ON l.user_id = u.id
JOIN books b ON l.book_id = b.id
WHERE l.status = 'Active' AND l.due_date < CURDATE();
```

### Category Statistics
```sql
SELECT category,
    COUNT(*) as total_books,
    SUM(total_copies) as total_copies,
    SUM(available_copies) as available_copies
FROM books
GROUP BY category
ORDER BY total_books DESC;
```

---

## 🎓 Learning Outcomes

### Database Concepts
✅ Relational database design  
✅ Primary and foreign keys  
✅ Normalization (3NF)  
✅ SQL queries (SELECT, INSERT, UPDATE, DELETE)  
✅ JOINs (INNER, LEFT, RIGHT)  
✅ Aggregate functions (COUNT, SUM, GROUP BY)  
✅ Transactions and ACID properties  

### JDBC Programming
✅ DriverManager and Connection  
✅ Statement vs PreparedStatement  
✅ ResultSet navigation  
✅ SQL injection prevention  
✅ Exception handling  
✅ Resource management (try-with-resources)  
✅ Batch operations  

### Java Skills
✅ Object-oriented design  
✅ Model-View-Controller pattern  
✅ Collections framework  
✅ Date/Time API  
✅ Exception handling  
✅ File I/O  

### JavaFX
✅ Scene and Stage  
✅ Layout managers  
✅ TableView and data binding  
✅ Event handling  
✅ Dialog boxes  
✅ CSS styling  

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewFeature`
3. Commit changes: `git commit -m 'Add NewFeature'`
4. Push to branch: `git push origin feature/NewFeature`
5. Open Pull Request

---

## 📄 License

MIT License - Copyright (c) 2025 Michael Semera

---

## 👤 Author

**Michael Semera**

- 💼 LinkedIn: [Michael Semera](https://www.linkedin.com/in/michael-semera-586737295/)
- 🐙 GitHub: [@MichaelKS123](https://github.com/MichaelKS123)
- 📧 Email: michaelsemera15@gmail.com

---

**Made with 📚 by Michael Semera**

*Manage your library efficiently and effectively!*

---

**Version**: 1.0.0  
**Last Updated**: November 1, 2025  
**Status**: Production Ready ✅  
**Database**: MySQL 8.0+  
**Language**: Java 11+  
**License**: MIT