# AssistFlow_AI_TriCode_SAS__
# AssistFlow AI  
### AI-Powered Customer Support Ticket Triage System

AssistFlow AI is an intelligent support assistant that automatically understands customer support tickets, predicts their priority, and suggests next actions using NLP and Generative AI.

---

## 🚨 Problem Statement
Customer support teams receive a large number of tickets daily through emails, chats, and web forms.  
Traditional keyword-based systems fail to:
- Understand the actual context of customer issues
- Identify urgent tickets accurately
- Suggest actionable next steps  

This leads to delayed resolutions and poor customer satisfaction.

---

## 💡 Solution Overview
AssistFlow AI acts as an **AI co-pilot for support agents** by:
- Analyzing customer tickets using NLP and GenAI
- Classifying tickets into issue categories
- Predicting ticket priority (Critical / High / Medium / Low)
- Suggesting appropriate next actions with explanations

---

## ✨ Key Features
- Context-aware ticket understanding using Generative AI  
- Automated issue classification  
- Intelligent priority prediction  
- Actionable solution recommendations  
- Explainable AI output (reason behind decisions)  
- Interactive dashboard  

---

## 🔁 Input & Output

### 📥 Input
Customer support ticket text:
"My payment was deducted twice but the order is still pending. Very frustrated."


## 📤 Output
The system generates a structured and explainable response for each customer support ticket.

```json
{
  "Issue Category": "Payment Issue",
  "Priority": "Critical",
  "Suggested Action": "Escalate to payments team and initiate refund process",
  "Reason": "Duplicate payment detected along with strong negative sentiment"
}




🛠 Tech Stack

Programming Language: Python
Used for building the complete backend logic and AI integration.

Generative AI: OpenAI / Gemini / Groq (LLaMA-3)
Enables fast and context-aware analysis of customer support tickets using large language models.

NLP Utilities: scikit-learn
Used for basic text preprocessing and supporting NLP operations.

UI Framework: Streamlit
Provides a simple and interactive web-based dashboard for real-time ticket analysis.

Deployment: Local
The application is deployed locally for hackathon demonstrations, ensuring quick setup and reliable execution.
