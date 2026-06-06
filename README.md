<div align="center">
  
# 🏢 CODEX VendorBridge

**A modern, full-stack Procurement & ERP System**

[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

*Streamlining the Request for Quotation (RFQ) process, vendor management, and purchase order lifecycles.*

</div>

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🔐 **Role-Based Access** | Distinct dashboards and secure permissions for Admins, Procurement Officers, Approvers, and Vendors. |
| 🏢 **Vendor Management** | Easily onboard, track, and manage vendor details, categories, and performance ratings. |
| 📋 **RFQ Lifecycle** | Create dynamic Requests for Quotations, specify items, and intelligently assign them to active vendors. |
| 📝 **Quotations System** | Vendors can securely log in, view their assigned RFQs, and submit structured quotations. |
| ✅ **Approval Workflows** | Managers and Approvers can review quotations and approve or reject them with inline comments. |
| 🧾 **Automated POs** | Approved quotations seamlessly and automatically generate Purchase Orders and tracking Invoices. |
| 📊 **Real-time Dashboard** | Track active workflows and calculate spending metrics with dynamic UI components. |

---

## 🏗️ Project Architecture

<details>
<summary><b>🐍 Backend Structure (Django)</b></summary>

```text
CODEX-backend/
├── accounts/          # User models, authentication APIs, serializers
├── invoices/          # Invoices generation and management
├── procurement/       # RFQ, Quotation, PO, Approval models & views
├── vendors/           # Vendor profiles and directories
├── vendorbridge/      # Main Django project settings & URL routing
├── manage.py          # Django CLI entry point
├── seed_db.py         # Database dummy data seeder
└── requirements.txt   # Python dependencies
```
</details>

<details>
<summary><b>📱 Frontend Structure (Flutter)</b></summary>

```text
CODEX-vendorbridge/
├── lib/
│   ├── core/          # Constants, API client, custom themes
│   ├── data/          # Data models and API repository layers
│   ├── providers/     # State management (ChangeNotifiers)
│   ├── screens/       # UI Pages (Dashboard, RFQs, Vendors, etc.)
│   ├── widgets/       # Reusable UI components (Sidebar, Cards, Badges)
│   ├── main.dart      # App entry point & multi-provider setup
│   └── routes.dart    # GoRouter navigation paths and guards
└── pubspec.yaml       # Flutter packages and assets
```
</details>

---

## 🚀 Getting Started

### 1. Backend Setup

Open a terminal and navigate to the backend directory:
```bash
cd CODEX-backend
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Run database migrations & seed dummy data:
```bash
python manage.py migrate
python seed_db.py
```

Start the Django development server:
```bash
python manage.py runserver
```

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd CODEX-vendorbridge
```

Install Flutter dependencies and run:
```bash
flutter pub get
flutter run
```
> **Note:** If testing on a physical Android/iOS device, ensure your API endpoints in `api_constants.dart` point to your local machine's IP address instead of `localhost`.

---

## 🔑 Default Seeded Accounts

If you ran `seed_db.py`, you can log in immediately with these dummy accounts. 
**Password for all accounts:** `password`

| Role | Username / Email |
| :--- | :--- |
| **System Admin** | `admin@codex.com` |
| **Procurement Officer** | `procurement@codex.com` |
| **Manager / Approver** | `approver@codex.com` |
| **Vendor** | `sales@techcorp.in` |
