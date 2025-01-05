# Database Documentation

## Overview
* SQLite database system
* Located at root as `database.db`
* Supports core hardware store operations
* Focus on data integrity and efficiency

## Tables Overview

### Admin Table
* Purpose: Manage system users with privileges
* Key Fields:
  - Username (unique)
  - Password (encrypted)
  - Email
  - Role
  - Creation timestamp

### Category Table
* Purpose: Organize product classifications
* Key Fields:
  - Name (unique)
  - Description
  - Creator reference
  - Creation date

### Products Table
* Purpose: Track inventory items
* Key Fields:
  - SKU (unique)
  - Name
  - Description
  - Price
  - Stock quantity
  - Minimum quantity
  - Category link
  - Creation date

### Stock Movements Table
* Purpose: Record inventory changes
* Key Fields:
  - Product reference
  - Quantity change
  - Movement type
  - Date
  - Notes

### Sales Table
* Purpose: Track transactions
* Key Fields:
  - Admin reference
  - Date
  - Total amount

### Sale Items Table
* Purpose: Detail individual sales
* Key Fields:
  - Sale reference
  - Product reference
  - Quantity
  - Sale price

## Key Relationships

### Product Organization
* Products → Categories (one-to-one)
* Categories → Products (one-to-many)
* Categories → Admin (creation tracking)

### Inventory Control
* Products → Stock levels (current count)
* Products → Stock movements (history)
* Products → Minimum levels (alerts)

### Sales Structure
* Sales → Admin (processor)
* Sales → Items (one-to-many)
* Items → Products (reference)

## Data Management

### Initial Data
* Pre-loaded categories
* Default admin account
* Sample products
* Example transactions

### Data Protection
* Unique field enforcement
* Required field validation
* Relationship integrity
* Timestamp tracking
* Secure password storage
* Role-based access

## Best Practices

### Data Entry Standards
* Standardized SKU format
* Consistent category naming
* Fixed price precision
* Non-negative quantities

### Maintenance Tasks
* Regular backups
* Stock level monitoring
* Sales history archiving
* Admin account audits
