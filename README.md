

Built as a mini e-commerce system to demonstrate full-stack development skills.

# 🛒 Grocery Web Application

This is a grocery web application I built using Flask to understand how real-world e-commerce systems work. The project allows users to browse products, add items to cart, apply discounts, and place orders with a simple and clean interface.

---

## 🚀 Features

### 🛍️ User Side
- Simple login system using sessions  
- Product catalog with multiple items  
- Search products by name  
- Filter products by category  
- Add items to cart  
- Increase / decrease quantity in cart  
- Supports multiple products in cart  
- Apply discount (10%, 20%, 30%)  
- Checkout and payment page  
- View placed orders  

---

### ⚙️ Backend / System
- Cart is managed using session  
- Total price updates dynamically  
- Data stored using SQLite database  
- Orders are saved and tracked  
- Delivery page to update order status  
- Option to clear old delivery records  

---

### 🎨 UI / Design
- Dark theme UI  
- Clean and simple layout  
- Responsive design (works on mobile)  
- Product grid view (5 items per row)  
- Styled login page with centered layout  

---

## 🛠️ Tech Used

- Python (Flask)
- HTML, CSS
- SQLite

---

## 📂 Project Structure

grocery-web-app/
│
├── app.py
├── database.db
├── templates/
│ ├── login.html
│ ├── catalog.html
│ ├── cart.html
│ ├── payment.html
│ ├── orders.html
│ └── delivery.html
│
├── static/
│ └── style.css
│
├── README.md
└── .gitignore



---

## ▶️ How to Run

```bash
pip install flask
python app.py

Open browser:

http://127.0.0.1:5000/


## 💡 What I Learned

- How to build a full web app using Flask  
- Handling sessions for cart management  
- Connecting frontend with backend  
- Working with SQLite database  
- Designing simple and clean UI  

---

## 🚀 Future Improvements

- Add proper user authentication  
- Integrate real payment gateway  
- Improve UI further  
- Deploy project online  

---

## 👨‍💻 Author

Abhishek Kasnale






