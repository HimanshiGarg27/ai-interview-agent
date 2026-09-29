AI Interview Agent 🤖💼
An intelligent, AI-powered mock interview application designed to simulate real-world technical and behavioral interviews. Originally developed for ViCodathon 2026, this tool evaluates candidate responses in real-time, generates dynamic follow-up questions, and provides comprehensive feedback to help job seekers refine their interview skills.
🌟 Key Features
Dynamic Question Generation: Adapts questions based on the chosen role, experience level, and the candidate's previous answers.
Real-Time AI Feedback: Analyzes responses for clarity, technical accuracy, and completeness using large language models.
Interactive UI: Built with Streamlit for a seamless, responsive, and distraction-free user experience.
Performance Scoring: Delivers a post-interview breakdown highlighting strengths and actionable areas for improvement.
🛠️ Tech Stack
Language: Python 3.9+
Frontend/Framework: Streamlit
AI/Machine Learning: Generative AI APIs (e.g., Gemini) for natural language understanding and generation.
Deployment: Streamlit Community Cloud
🚀 Installation and Setup
Prerequisites
Ensure you have Python installed on your system along with pip for package management. You will also need an active API key for your chosen LLM provider.
1. Clone the Repository
   git clone https://github.com/yourusername/ai-interview-agent.git
cd ai-interview-agent
2. Create a Virtual Environment (Recommended)
   python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies
   pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add your API keys:
LLM_API_KEY="your_api_key_here"
5. Run the Application
   streamlit run app.py
   The application will launch locally at http://localhost:8501.
📂 Project Structure
ai-interview-agent/
├── app.py                 # Main Streamlit application entry point
├── requirements.txt       # Project dependencies
├── .env.example           # Example environment variables file
├── README.md              # Project documentation
├── utils/                 # Helper functions for API calls and state management
│   ├── ai_engine.py       # LLM integration and prompt engineering
│   └── ui_components.py   # Custom Streamlit layout elements
└── assets/                # Images, icons, or stylesheets
🤝 Contributing
Contributions are welcome! If you have ideas for new features, better prompt engineering for the AI, or UI enhancements:
Fork the project.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.
📜 License
Distributed under the MIT License. See LICENSE for more information.
