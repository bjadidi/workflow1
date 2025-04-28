# Biopolymer-Selection-Workflow

A professional Streamlit-based tool to identify, evaluate, and compare biopolymers based on user-defined constraints and preferences.

## 🌟 Features
- **🔐 User Login**: Secure session-based login system
- **📥 Input Form**: Define performance, cost, sustainability, and geographical criteria
- **📊 Ranked Table**: Polymers are scored and visually color-coded based on match quality
- **💬 Feedback**: Users can provide polymer-specific feedback stored by username
- **⬇️ Downloads**: Results can be exported as Excel or CSV with star rating confirmation
- **📈 Analysis Tools**: Select performance metrics to visualize correlations
- **🎨 Modern UI**: Styled with animations and enhanced layout

## 🚀 Getting Started
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🗂️ Project Structure
```
Biopolymer-Selection-Workflow/
├── app/
│   └── pages/
│       ├── input_page.py         # Requirements form
│       └── output_page.py        # Polymer rankings & analysis
├── auth/
│   └── login.py                  # User login logic
├── data/
│   ├── polymer_database_placeholder.xlsx
│   └── feedback/                # Per-user saved feedback
├── app.py                       # Main application file
├── requirements.txt             # Dependencies
├── .gitignore
└── README.md
```

## 📌 Future Enhancements
- Hashed password login with user registration
- Persistent user sessions and history
- Admin panel for managing feedback and polymer database

---
Made with ❤️ for researchers, engineers, and sustainability innovators.