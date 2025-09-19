-- Complete e-commerce database schema
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    region TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price_cents INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    amount_cents INTEGER,
    method TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE IF NOT EXISTS refunds (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    amount_cents INTEGER,
    reason TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Insert sample data
INSERT INTO customers (name, email, region) VALUES 
('John Doe', 'john@example.com', 'North'),
('Jane Smith', 'jane@example.com', 'South'),
('Bob Johnson', 'bob@example.com', 'East'),
('Alice Brown', 'alice@example.com', 'West'),
('Charlie Wilson', 'charlie@example.com', 'North');

INSERT INTO orders (customer_id, order_date, status) VALUES
(1, '2023-05-01', 'completed'),
(1, '2023-05-15', 'completed'),
(2, '2023-05-10', 'completed'),
(3, '2023-05-20', 'completed'),
(4, '2023-06-01', 'completed'),
(5, '2023-06-05', 'completed'),
(2, '2023-06-10', 'pending');

INSERT INTO products (name, category, description) VALUES
('Laptop', 'Electronics', 'High-performance laptop'),
('Smartphone', 'Electronics', 'Latest smartphone model'),
('Book', 'Education', 'Programming book'),
('Headphones', 'Electronics', 'Noise-cancelling headphones'),
('Desk', 'Furniture', 'Office desk');

INSERT INTO order_items (order_id, product_id, quantity, unit_price_cents) VALUES
(1, 1, 1, 100000),
(1, 3, 2, 2500),
(2, 2, 1, 80000),
(3, 4, 1, 15000),
(4, 5, 1, 20000),
(5, 2, 2, 80000),
(6, 3, 3, 2500);

INSERT INTO payments (order_id, amount_cents, method) VALUES
(1, 105000, 'credit_card'),
(2, 80000, 'paypal'),
(3, 15000, 'credit_card'),
(4, 20000, 'bank_transfer'),
(5, 160000, 'credit_card'),
(6, 7500, 'paypal');

INSERT INTO refunds (order_id, amount_cents, reason) VALUES
(1, 5000, 'Damaged product'),
(3, 15000, 'Customer changed mind');
