Notes: 

    Removing from local and syncing with .gitignore: git rm -r --cached __pycache__ 
    Deleting branch after merging with main: git branch -d first-changes


    Create virtual env, so requirements.txt only necessary packages: https://mnzel.medium.com/how-to-activate-python-venv-on-a-mac-a8fa1c3cb511

    1. Create venv: command-shift-P
    2. Install necessary packages (pip install package_name)
        Install from requirements (pip install -r requirements.txt)
    3. Create requirements.txt with (pip freeze > requirements.txt)
        Install 


    Session State Basics for StreamLit: https://www.youtube.com/watch?v=92jUAXBmZyU&feature=youtu.be&ab_channel=Streamlit

    CSV Import Help: https://medium.com/@vijayveeranar/unleashing-the-power-of-langchain-and-openai-gpt-conversing-with-csv-files-3e500cc6bb50




Thought Process on Model Architecture:
    1. Using CSV_agent to find semantic similarity may not be the most efficient. It just takes the input and searches the data frame to see if it contains the string. 
        a. What if we made it generate semantically similar strings to the one provided? It may not be efficient but it could work? 
    2. Instead, what if we used cosine similarity to easily find situations where they were similar? Approach #1 may be slow for larger datasets
    

    






