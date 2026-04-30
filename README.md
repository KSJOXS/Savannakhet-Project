# Savannakhet Smart Travel Project

Savannakhet Smart Travel is a modern web application designed to enhance the travel experience in Savannakhet, Laos. The platform provides comprehensive information about destinations, hotels, restaurants, and nature spots, while also fostering a community for travelers to share their experiences.

## 🛠 Features by User Role

### 👤 User Functions
Registered users can interact with the platform to plan their trips and share their travel stories.

*   **Discovery & Exploration**
    *   **Explore All Places:** Search and browse through various categories including Hotels, Restaurants, Nature, and Landmarks.
    *   **Story of Savannakhet:** Learn about the history and culture of the region.
    *   **Dynamic Search:** Quick search for destinations, hotels, and attractions.
*   **Community Interaction**
    *   **Social Feed:** A Facebook-style community page to view updates from other travelers.
    *   **Post Updates:** Share stories, travel tips, and photos with the community.
    *   **Write Reviews:** Rate and review visited locations with text and images.
*   **Travel Tools**
    *   **Currency Converter:** Real-time exchange rate tool for travelers.
    *   **Lao Phrasebook:** Essential Lao phrases for better communication.
    *   **Transport Guide:** Information on how to get around Savannakhet.
*   **Personal Management**
    *   **My Profile:** Manage personal information and profile images.
    *   **My Trips (Favorites):** Save favorite locations for future reference.
    *   **Review History:** Track all previously posted reviews and ratings.
    *   **Bookings:** View and manage hotel reservation history.
*   **Contribution**
    *   **Submit Place:** Crowdsource new locations by submitting them for admin review.
    *   **Photo Sharing:** Upload photos of landmarks and attractions.

---

### 🛡 Admin Functions
Administrators have full control over the platform's content and user base through a dedicated dashboard.

*   **Dashboard & Analytics**
    *   Overview of platform statistics, including user activity and content growth.
*   **Content Management**
    *   **Manage Places:** Add, edit, or remove travel destinations, hotels, and restaurants.
    *   **Category Management:** Organize locations into relevant categories.
    *   **Submission Review:** Approve or reject places submitted by the community.
*   **User Management**
    *   **User Directory:** View and search all registered users.
    *   **Account Control:** Edit user details, suspend accounts, or restore suspended users.
    *   **Role Assignment:** Manage administrative permissions.
*   **Moderation & Support**
    *   **Comment Moderation:** Manage and moderate user reviews and community posts.
    *   **Contact Messages:** View and respond to inquiries from the contact form.
*   **System Configuration**
    *   **Opening Hours:** Configure business hours for specific locations.
    *   **Platform Settings:** Manage system-wide configurations and localized content.

## 🧠 AI Recommendation System (GNN)

The platform features an advanced **Graph Neural Network (GNN)** recommendation engine built with **PyTorch Geometric**. Unlike traditional algorithms, our GNN understands the deep relationships between users and destinations.

### 🏗 Architecture
- **Heterogeneous Graph:** Models complex interactions between two node types: `User` and `Place`.
- **Node Features:**
  - **Places:** Encoded with category information and average ratings to handle "Cold Start" scenarios.
  - **Users:** Dynamic preference embeddings based on interaction history.
- **Algorithm:** Uses **GraphSAGE (SAGEConv)** for inductive representation learning, allowing the system to recommend new places efficiently.
- **Learning Task:** Trained via **Link Prediction** with **Negative Sampling** and **BCE Loss** to predict the likelihood of a user visiting a specific location.

### 🎯 Key AI Features
- **Personalized Recommendations:** Tailored "For You" section based on graph-wide behavioral patterns.
- **Similar Places:** Item-item collaborative filtering using cosine similarity of GNN node embeddings.
- **Explainable AI:** Provides reasons for recommendations (e.g., "Because you liked [Place Name]").
- **Dynamic Hero Category:** Automatically identifies and highlights the user's favorite travel category.

---

## 🌐 Localization
The platform supports multiple languages to cater to a global audience:
*   English 🇬🇧
*   Lao 🇱🇦
*   Vietnamese 🇻🇳
*   Thai 🇹🇭

## 🚀 Technology Stack
- **Frontend:** Vue.js 3 (Vite), Vue Router, Vue-i18n
- **Backend:** Python (FastAPI), SQLAlchemy, MySQL
- **AI/ML:** PyTorch, PyTorch Geometric (PyG)
- **Styling:** Vanilla CSS (Modern design with Glassmorphism and animations)
- **Icons:** FontAwesome
