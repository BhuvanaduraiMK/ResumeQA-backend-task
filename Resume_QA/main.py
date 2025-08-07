
import os


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv


from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in .env")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash", 
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)


MOCK_RESUME_CONTENT = """
Bhuvanadurai M
Aspiring Data Analyst | Python & SQL Developer | Final Year CSE (Data Science)

Summary:
I am a Computer Science Engineering (Data Science) graduate passionate about Data Science, Data Analytics, and Python development. I have hands-on experience in scalable data processing, sentiment analysis using Spark, and frontend development. Skilled in Python, SQL, Power BI, and have built several academic and internship projects. I am eager to contribute to data-driven roles in fast-paced environments.

Projects:
- Scalable Data Processing for Social Media Analysis (Final Year Project): Built a complete data pipeline using Apache Spark, PySpark, and Docker to process Twitter data, perform sentiment analysis using NLTK and ML models, and visualize results using Power BI. Achieved up to 91% accuracy.
- Weather Forecast App: Created a responsive web app using HTML, CSS, JavaScript, and API integration to display real-time weather.
- Internship Project at Velozion: Developed static webpages using HTML, CSS, and Bootstrap as part of a Front-End Developer internship.

Skills:
Programming: Python, SQL, JavaScript (Basics), HTML, CSS, Bootstrap
Tools: Apache Spark, PySpark, Docker, Power BI, Git, NLTK, scikit-learn
Concepts: Data Processing, Sentiment Analysis, ML Algorithms, Data Visualization, Web Development

Education:
- B.E. in Computer Science and Engineering (Data Science), Annamalai University (2025)

Certificates:
- Python for Everybody (Coursera)
- Microsoft Excel - Excel from Beginner to Advanced (Udemy)
- Deep Learning and Reinforcement Learning (SWAYAM)
- Power BI Analytics (College/Project-based)
- Internship Certificate – Front-End Development, Velozion Company

Achievements:
- Winner of 6 Technical and Sports Events including:
  • 1st Prize – Paper Presentation, TECH AERO 360 (Arasu Engineering College)
  • 2nd Prize – CODE HUB, TECHNOVA '24
  • 3rd Prize – Newsletter Writing, COMPSEM '24 (Annamalai University)

LinkedIn: https://www.linkedin.com/in/bhuvanadurai-mk/
GitHub: https://github.com/BhuvanaduraiMK

"""


template = """
You are a helpful AI assistant trained to answer questions strictly from resume content.
If the answer is not in the resume, respond with "Information not found."

Resume:
---------------------
{resume}
---------------------

Question: {query}
Answer:
"""

prompt = PromptTemplate.from_template(template)


chain = (
    RunnableMap({"resume": lambda x: MOCK_RESUME_CONTENT, "query": lambda x: x["query"]})
    | prompt
    | llm
    | StrOutputParser()
)


app = FastAPI(
    title="Resume Q&A with LangChain + Gemini",
    description="Ask questions about a resume using LangChain and Google Gemini",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    response: str


@app.get("/")
def root():
    return {"message": "Resume Q&A System (Gemini) is live. Use POST /query to ask questions."}

@app.post("/chat", response_model=QueryResponse)
async def query_resume(request: QueryRequest):
    try:
        response = chain.invoke({"query": request.query})
        return QueryResponse(query=request.query, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
