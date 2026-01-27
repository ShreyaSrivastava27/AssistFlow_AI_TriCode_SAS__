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
## We used System and User prompts-
SYSTEM_PROMPT = """
You are an AI support triage assistant for a SaaS company.

Your task:
- Read a customer support ticket
- Identify the underlying issue (not just keywords)
- Classify the issue category
- Determine urgency
- Suggest next actions for a human support agent
- Explain your reasoning clearly and concisely

You MUST return a valid JSON object only.
No markdown. No extra text.
"""

<br/>
Return Output as-<br/>
Return a JSON object with exactly these fields:<br/>
- issue (string)<br/>
- category (one of: Authentication, Billing, Performance, UI Bug, Integration, Other)<br>
- urgency (one of: Critical, High, Medium, Low)<br/>
- suggested_actions (array of strings)<br/>
- explanation (string)<br/>
- confidence (number between 0 and 1)<br/>
"""<br/>
Then we converted json output in user interface
<br/>

## 🔁 Input & Output

AssistFlow AI analyzes incoming customer support tickets and produces a structured, explainable response.
Based on the severity and complexity of the issue, the system either routes the ticket to a human agent or resolves it automatically using an AI agent.

### 📥 Input
Customer support ticket text:
"My payment was deducted twice but the order is still pending. Very frustrated."


## 📤 Output
The system generates a structured and explainable response for each customer support ticket.
<br/>
{<br/>
  "Issue Category": "Payment Issue",<br/>
  "Priority": "Critical",<br/>
  "Suggested Action": "Escalate to payments team and initiate refund process",<br/>
  "Reason": "Duplicate payment detected along with strong negative sentiment"<br/>
}<br/>



Our application reads a customer support message and tells the agent what the issue is, how urgent it is and what to do next the issue is handled by AI or if problem is critical then AI will lead it to human agent support.
## For AB testing
<b>We are storing user inputs live in tickets.csv for performing AB testing of our models</b>
<br/>
Model Comparison: Evaluate multiple models using confidence scores.
<br/>
Average Confidence Score: Calculate the mean confidence score of predictions for each model.
<br/>
Urgency Classification: Classify data points into predefined urgency levels (e.g., High, Medium, Low).
<br/>
Category Classification: Classify data points into relevant categories based on the content.
<br/>
A/B Testing Analysis: Compare models based on performance metrics and confidence levels.
<br/>

## 📊 Analytics & Insights

The Analytics dashboard provides:
- Ticket volume over time
- Issue category trends
- Urgency distribution
- Model confidence trends
- Issue complexity trends
- Model usage comparison (A/B testing)
- Drift detection and emerging issue signals
  
## 🛠 Tech Stack

Programming Language: Python
Used for building the complete backend logic and AI integration.

<b>Generative AI: Llama-3.1-8b-instant / Llama-3.3-70b-versatile/ Openai/gpt-oss-120b </b>
Enables fast and context-aware analysis of customer support tickets using large language models.

NLP Utilities: scikit-learn
Used for basic text preprocessing and supporting NLP operations.

<b>UI Framework: Streamlit</b>
Provides a simple and interactive web-based dashboard for real-time ticket analysis.

Deployment: Local
<br/>
<h1>Output Snapshots are avialable in Output_Snapshots</h1>
