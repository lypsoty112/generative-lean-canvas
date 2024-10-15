PYTHON_PATH = ./.venv/scripts/python.exe

# Run FastAPI app with Uvicorn
main: 
	@$(PYTHON_PATH) -m streamlit run main.py --server.headless true