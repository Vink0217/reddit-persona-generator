# GitHub Setup and Push Guide

## 📋 Prerequisites

1. **Install Git** (if not already installed):
   - Windows: Download from [git-scm.com](https://git-scm.com/)
   - macOS: `brew install git` or download from git-scm.com
   - Linux: `sudo apt install git` (Ubuntu/Debian) or `sudo yum install git` (CentOS/RHEL)

2. **Create a GitHub Account** at [github.com](https://github.com) if you don't have one

## 🚀 Step-by-Step GitHub Setup

### Step 1: Create a New Repository on GitHub

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill out the repository details:
   - **Repository name**: `reddit-persona-generator`
   - **Description**: "AI-powered Reddit user persona generator using Gemini AI"
   - **Visibility**: Choose Public or Private
   - **Initialize**: Leave unchecked (we'll push existing code)
5. Click "Create repository"

### Step 2: Prepare Your Local Project

1. **Navigate to your project directory**:
   ```bash
   cd /path/to/your/reddit-persona-generator
   ```

2. **Create the necessary files**:
   
   Create these files in your project directory:
   - `README.md` (use the README artifact I created)
   - `requirements.txt` (use the requirements artifact I created)
   - `sample_user_analysis.txt` (use the sample analysis artifact I created)

3. **Create a .gitignore file**:
   ```bash
   # Create .gitignore file
   touch .gitignore
   ```
   
   Add this content to `.gitignore`:
   ```
   # Environment variables
   .env
   .env.local
   .env.development.local
   .env.test.local
   .env.production.local
   
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   build/
   develop-eggs/
   dist/
   downloads/
   eggs/
   .eggs/
   lib/
   lib64/
   parts/
   sdist/
   var/
   wheels/
   *.egg-info/
   .installed.cfg
   *.egg
   
   # Virtual Environment
   venv/
   env/
   ENV/
   
   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo
   *~
   
   # OS
   .DS_Store
   Thumbs.db
   
   # Logs
   *.log
   
   # Database
   *.db
   *.sqlite3
   
   # Temporary files
   *.tmp
   *.temp
   ```

### Step 3: Initialize Git and Push to GitHub

1. **Initialize Git repository**:
   ```bash
   git init
   ```

2. **Add your files**:
   ```bash
   git add .
   ```

3. **Configure Git** (if first time):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

4. **Make your first commit**:
   ```bash
   git commit -m "Initial commit: Reddit Persona Generator"
   ```

5. **Add the remote repository**:
   ```bash
   git remote add origin https://github.com/yourusername/reddit-persona-generator.git
   ```
   
   Replace `yourusername` with your actual GitHub username.

6. **Push to GitHub**:
   ```bash
   git push -u origin main
   ```
   
   If you get an error about "main" vs "master", try:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### Step 4: Verify Your Repository

1. Go to your GitHub repository URL
2. You should see all your files including:
   - `main.py`
   - `Summary.py`
   - `README.md`
   - `requirements.txt`
   - `sample_user_analysis.txt`
   - `templates/` folder with HTML files

## 🔧 Alternative: Using GitHub Desktop

If you prefer a GUI:

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Sign in with your GitHub account
3. Click "Clone a repository from the Internet"
4. Select your repository
5. Choose local path
6. Use the GUI to commit and push changes

## 📁 Final Project Structure

Your GitHub repository should have this structure:

```
reddit-persona-generator/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── Summary.py
├── sample_user_analysis.txt
└── templates/
    ├── index.html
    └── combined.html
```

## 🚨 Important Notes

1. **Never commit your .env file** - it contains sensitive API keys
2. **The .gitignore file** prevents sensitive files from being uploaded
3. **Keep your API keys secure** - never share them publicly
4. **Update README.md** with your actual GitHub username in clone URLs

## 🔄 Future Updates

When you make changes to your code:

1. **Add changes**:
   ```bash
   git add .
   ```

2. **Commit changes**:
   ```bash
   git commit -m "Description of changes"
   ```

3. **Push to GitHub**:
   ```bash
   git push
   ```

## 🎉 Success!

Your Reddit Persona Generator is now on GitHub! Share the repository URL with others, and they can follow the README instructions to set it up and run it locally.

**Repository URL Format**: `https://github.com/yourusername/reddit-persona-generator`
