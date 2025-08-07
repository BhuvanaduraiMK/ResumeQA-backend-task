Resume Q&A Backend – Mittai Healthcare Pvt. Ltd.
	
 	This backend project is developed as part of a task for Mittai Healthcare Pvt. Ltd. 
  	It supports resume-related Q&A operations using Python and provides an API interface for 
  	backend operations.

Folder Structure
      
      mittai-backend-task/
		│
		├── Resume_QA/
		│   ├── main.py              
		│   ├── requirements.txt     
		│   ├── .env                 
		│   ├── img/
		│	└── final_result.png            
		├── README.md          
		└── .gitignore           

Tech Stack ⚙️ 
   - Python 3.x
   - FastAPI
   - Uvicorn (if using FastAPI)
   - Virtualenv

How to Run the Project 🚀
	
 	Step 1:Create a virtual environment 
		python -m venv venv	
        Step 2: Activate your virtual environment
		venv\Scripts\activate       
        Step 3: Install dependencies
		pip install -r requirements.txt 
        Step 4: Run the backend
		uvicorn main:app --reload  #(for FastAPI)

Important:
	Make sure your .env contains required environment variables like API keys or DB URLs.

🙋 Author
Bhuvanadurai M
Final Year – B.E CSE (Data Science)
Annamalai University
