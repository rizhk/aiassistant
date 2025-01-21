
docker run  -it --name aiassistant -d -v $(pwd):/workspace::consistent -p 8000:8000 aiassistant
# pip install langchain openai python-dotenv
# pip install --no-cache-dir -r requirements.txt