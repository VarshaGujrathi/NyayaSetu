# NyayaSetu - Legal Empowerment Platform

NyayaSetu is an AI-powered legal empowerment platform designed to simplify complex legal documents and make them accessible to citizens, particularly in rural areas. By leveraging advanced machine learning models and natural language processing, NyayaSetu transforms legal jargon into plain language, identifies risky clauses, ensures compliance, and provides interactive features for better understanding of legal rights.

## 🌟 Features

### Legal Simplification

- Automatically converts complex legal terms into simple, everyday language
- Supports multiple regional languages for better accessibility
- Provides audio explanations using text-to-speech technology

### Clause Risk Indicator

- AI-powered analysis to highlight potentially risky clauses in legal documents
- Color-coded risk levels (High, Medium, Low) for quick identification
- Detailed explanations for each identified risk

### Voice & Text Interaction

- Interactive chatbot for legal queries
- Supports both voice input and text-based conversations
- Instant responses to common legal questions

### Compliance Alerts

- Automated checking of legal document compliance
- Flags missing signatures, dates, stamps, and other critical elements
- Supports various document types (sale deeds, agreements, etc.)

### Smart Form Auto-Fill

- Intelligent extraction of data from uploaded documents
- Automatic population of legal forms with extracted information
- Reduces manual data entry and minimizes errors

### Document Comparison

- Side-by-side comparison of legal document versions
- Detects additions, deletions, and modifications
- Semantic analysis to understand the impact of changes

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/nyayasetu.git
   cd nyayasetu
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional, for admin access):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## 📖 Usage

1. **Upload Document:** Start by uploading a legal document (PDF, DOCX, etc.) through the Legal Simplifier page.

2. **Review Summary:** The system will generate a simplified summary of the document.

3. **Check Risks:** Review highlighted risky clauses with explanations.

4. **Compliance Check:** Verify document compliance with legal requirements.

5. **Compare Versions:** Upload multiple versions to compare changes.

6. **Interactive Queries:** Use voice or text to ask legal questions.

## 🏗️ Project Structure

```
nyayasetu/
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── main/                         # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── clause_detector.py        # Clause detection logic
│   ├── comparison_utils.py       # Document comparison utilities
│   ├── compliance_engine.py      # Compliance checking engine
│   ├── confidence_engine.py      # Confidence calculation
│   ├── models.py                 # Django models
│   ├── semantic_diff.py          # Semantic difference analysis
│   ├── tests.py                  # Unit tests
│   ├── urls.py                   # URL patterns
│   ├── utils.py                  # Utility functions
│   ├── views.py                  # View functions
│   └── compliance_rules/         # JSON compliance rules
│       ├── agreement_of_assignment.json
│       ├── development_agreement.json
│       ├── leave_and_licence.json
│       ├── sale_deed_agri.json
│       ├── simple_mortgage.json
│       ├── transfer_deed_flat.json
├── media/                        # User-uploaded files
│   └── pdf_pages/
├── models/                       # ML models
│   ├── nyaysetu_stage1/          # First-stage ML model
│   └── nyaysetu_stage2/          # Second-stage ML model
├── nyayasetu/                    # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py
├── static/                       # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   └── images/
├── templates/                    # HTML templates
│   ├── index.html
│   ├── clause_risk_indicator.html
│   ├── compliance_alerts.html
│   ├── document_comparison.html
│   ├── legal_helpline_integration.html
│   ├── legal_simplifier.html
│   ├── regional_law_mapping.html
│   ├── smart_form_autofill.html
│   └── voice_text_interaction.html
└── README.md                     # This file
```

## 🛠️ Dependencies

The project relies on several key libraries:

- **Django:** Web framework
- **Transformers:** For natural language processing tasks
- **PyTorch:** Deep learning framework
- **spaCy:** NLP library for text processing
- **Google Generative AI:** For advanced AI capabilities
- **gTTS:** Google Text-to-Speech for audio generation
- **PDFMiner/PyPDF2:** PDF text extraction
- **Sentence Transformers:** For semantic similarity
- **OpenAI:** For additional AI features

See `requirements.txt` for the complete list of dependencies.

## 🤝 Contributing

We welcome contributions to NyayaSetu! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**NyayaSetu Project Team**

- **Institution:** Department of AI & DS, K J Somaiya Institute of Technology, Mumbai
- **Email:** contact@nyayasetu.in
- **Phone:** +91 XXXXXXXX

## 🙏 Acknowledgments

- Built with Django web framework
- Powered by advanced machine learning models
- Inspired by the need for legal accessibility in India

---

_"Where law meets clarity, and citizens meet empowerment."_</content>
<parameter name="filePath">d:\Major_Project\NyayaSetu\README.md
