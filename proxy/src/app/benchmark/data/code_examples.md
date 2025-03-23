# Code Examples for Benchmarking

This file contains various code examples that can be used for benchmarking the SynthLang compression system. These examples include different programming languages, paradigms, and complexity levels.

## Python Examples

### Data Science Pipeline

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load the dataset
#load_data
df = pd.read_csv('customer_data.csv')

# Exploratory Data Analysis
#analyze_data
print(f"Dataset shape: {df.shape}")
print(df.info())
print(df.describe())

# Check for missing values
#check_missing
missing_values = df.isnull().sum()
print(f"Missing values per column:\n{missing_values}")

# Data Visualization
#visualize_data
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.savefig('correlation_matrix.png')

# Feature Engineering
#engineer_features
# Create new features
df['purchase_frequency'] = df['total_purchases'] / df['customer_tenure_days']
df['average_order_value'] = df['total_spend'] / df['total_purchases']
df['days_since_last_purchase'] = pd.to_datetime('today') - pd.to_datetime(df['last_purchase_date'])
df['days_since_last_purchase'] = df['days_since_last_purchase'].dt.days

# Encode categorical variables
df = pd.get_dummies(df, columns=['customer_segment', 'preferred_channel'])

# Prepare data for modeling
#prepare_model_data
X = df.drop(['customer_id', 'churn_status', 'last_purchase_date'], axis=1)
y = df['churn_status']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a model
#train_model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate the model
#evaluate_model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
#analyze_importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance.head(10))
plt.title('Top 10 Feature Importance')
plt.tight_layout()
plt.savefig('feature_importance.png')

# Save the model
#save_model
import joblib
joblib.dump(model, 'churn_prediction_model.pkl')
joblib.dump(scaler, 'feature_scaler.pkl')

print("Model training and evaluation complete!")
```

### Web API with FastAPI

```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Initialize FastAPI app
#init_app
app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks with user authentication",
    version="1.0.0"
)

# Database connection
#connect_db
MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.task_manager

# Security
#setup_security
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
#define_models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=8)

class User(BaseModel):
    id: str
    username: str
    email: str
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: int = Field(1, ge=1, le=5)
    completed: bool = False

class Task(TaskCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
```

## JavaScript Examples

### React Component with Hooks

```javascript
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format } from 'date-fns';
import { toast } from 'react-toastify';

// API service
#api_service
const fetchProductDetails = async (id) => {
  const response = await fetch(`/api/products/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch product details');
  }
  return response.json();
};

const fetchCategories = async () => {
  const response = await fetch('/api/categories');
  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }
  return response.json();
};

const updateProduct = async ({ id, data }) => {
  const response = await fetch(`/api/products/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error('Failed to update product');
  }
  
  return response.json();
};

// Component
#component_definition
const ProductDetail = () => {
  // Hooks
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  
  // State
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: 0,
    categoryId: '',
    tags: [],
    stockQuantity: 0,
    isActive: true
  });
  
  // Queries
  const { 
    data: product, 
    isLoading: isLoadingProduct, 
    isError: isProductError,
    error: productError,
    refetch: refetchProduct
  } = useQuery(['product', id], () => fetchProductDetails(id), {
    onSuccess: (data) => {
      setFormData({
        name: data.name,
        description: data.description,
        price: data.price,
        categoryId: data.categoryId,
        tags: data.tags || [],
        stockQuantity: data.stockQuantity,
        isActive: data.isActive
      });
    }
  });
  
  // Handlers
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  // Render
  if (isLoadingProduct) {
    return <div>Loading...</div>;
  }
  
  if (isProductError) {
    return <div>Error: {productError.message}</div>;
  }
  
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
    </div>
  );
};

export default ProductDetail;
```

## SQL Examples

### Complex Database Query

```sql
-- Find top customers by revenue with their purchase patterns
#customer_revenue_analysis
WITH customer_revenue AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        SUM(oi.quantity * oi.unit_price) AS total_spent,
        COUNT(DISTINCT o.order_id) AS order_count,
        MIN(o.order_date) AS first_order_date,
        MAX(o.order_date) AS last_order_date,
        DATEDIFF(DAY, MIN(o.order_date), MAX(o.order_date)) AS customer_lifespan_days
    FROM 
        customers c
    JOIN 
        orders o ON c.customer_id = o.customer_id
    JOIN 
        order_items oi ON o.order_id = oi.order_id
    WHERE 
        o.order_status = 'completed'
        AND o.order_date >= DATEADD(YEAR, -1, GETDATE())
    GROUP BY 
        c.customer_id, c.first_name, c.last_name, c.email
),
purchase_patterns AS (
    SELECT
        cr.customer_id,
        cr.total_spent / NULLIF(cr.order_count, 0) AS avg_order_value,
        cr.order_count / NULLIF(cr.customer_lifespan_days, 0) * 30 AS monthly_purchase_frequency,
        (SELECT TOP 1 p.category_id 
         FROM order_items oi 
         JOIN orders o ON oi.order_id = o.order_id 
         JOIN products p ON oi.product_id = p.product_id 
         WHERE o.customer_id = cr.customer_id 
         GROUP BY p.category_id 
         ORDER BY COUNT(*) DESC) AS favorite_category_id
    FROM 
        customer_revenue cr
),
customer_segments AS (
    SELECT
        cr.*,
        pp.avg_order_value,
        pp.monthly_purchase_frequency,
        c.name AS favorite_category,
        CASE
            WHEN pp.avg_order_value > 100 AND pp.monthly_purchase_frequency > 2 THEN 'High Value'
            WHEN pp.avg_order_value > 100 THEN 'Big Spender'
            WHEN pp.monthly_purchase_frequency > 2 THEN 'Frequent Buyer'
            ELSE 'Regular Customer'
        END AS customer_segment,
        NTILE(5) OVER (ORDER BY cr.total_spent DESC) AS revenue_quintile
    FROM
        customer_revenue cr
    JOIN
        purchase_patterns pp ON cr.customer_id = pp.customer_id
    LEFT JOIN
        categories c ON pp.favorite_category_id = c.category_id
)
SELECT
    cs.*,
    RANK() OVER (ORDER BY cs.total_spent DESC) AS revenue_rank,
    PERCENT_RANK() OVER (ORDER BY cs.total_spent) AS revenue_percentile
FROM
    customer_segments cs
WHERE
    cs.revenue_quintile = 1  -- Top 20% of customers
ORDER BY
    cs.total_spent DESC;
```

### Database Schema Creation

```sql
-- E-commerce Database Schema
#create_database_schema
-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role VARCHAR(20) NOT NULL DEFAULT 'customer'
);

-- User addresses
CREATE TABLE addresses (
    address_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    address_type VARCHAR(20) NOT NULL, -- 'billing' or 'shipping'
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Product categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(category_id),
    image_url VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2),
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER REFERENCES categories(category_id),
    weight DECIMAL(8, 2),
    dimensions VARCHAR(50),
    is_featured BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    order_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    shipping_address_id INTEGER REFERENCES addresses(address_id),
    billing_address_id INTEGER REFERENCES addresses(address_id),
    payment_method VARCHAR(50),
    shipping_method VARCHAR(50),
    subtotal DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) NOT NULL,
    shipping_cost DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    tracking_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Order items
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0
);

-- Create indexes for performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_addresses_user ON addresses(user_id);
