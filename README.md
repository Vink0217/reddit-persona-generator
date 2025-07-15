# Reddit Persona Generator

A web application that analyzes Reddit user profiles to generate detailed personas using AI-powered analysis. This tool scrapes Reddit user data (posts and comments) and uses Google's Gemini AI to extract personality traits, motivations, frustrations, and emotional profiles.

## 🚀 Features

- **User Data Extraction**: Scrapes Reddit posts and comments using PRAW
- **AI-Powered Analysis**: Uses Google Gemini AI for persona generation
- **Comprehensive Personas**: Generates detailed profiles including:
  - Basic demographics (age, occupation, location)
  - Personality traits and archetypes
  - Motivations and frustrations
  - Emotional analysis with scoring
  - Goals and behavioral patterns
- **Web Interface**: Clean, responsive web UI built with FastAPI and Tailwind CSS
- **Database Storage**: MongoDB integration for data persistence
- **Real-time Processing**: Live persona generation with loading indicators

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.8+
- MongoDB (local or cloud instance)
- Reddit API credentials
- Google Gemini API key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/reddit-persona-generator.git
   cd reddit-persona-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Reddit API Credentials
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=your_app_name/1.0 by /u/yourusername
   
   # Google Gemini API
   GEMINI_API_KEY=your_gemini_api_key
   
   # MongoDB Connection
   MONGODB_URI=mongodb://localhost:27017/
   ```

## 🔑 API Setup

### Reddit API Setup

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill out the form:
   - **Name**: Your app name
   - **App type**: Choose "script"
   - **Description**: Optional
   - **About URL**: Optional
   - **Redirect URI**: `http://localhost:8000` (or leave blank for scripts)
4. Note down the **Client ID** (under the app name) and **Client Secret**

### Google Gemini API Setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the API key to your `.env` file

### MongoDB Setup

**Option 1: Local MongoDB**
1. Install MongoDB locally
2. Start MongoDB service
3. Use default connection string: `mongodb://localhost:27017/`

**Option 2: MongoDB Atlas (Cloud)**
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Get connection string and add to `.env`

## 🚀 Usage

### Running the Web Application

1. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Open your browser**
   
   Navigate to `http://localhost:8000`

3. **Analyze a Reddit user**
   - Enter a Reddit username or URL (e.g., `https://reddit.com/u/username` or just `username`)
   - Click "Generate Persona"
   - Wait for analysis to complete (may take 1-2 minutes)
   - View the generated persona dashboard

### Running the Command Line Script

For direct command-line usage:

```bash
python Summary.py
```

Enter the Reddit username when prompted.

## 📁 Project Structure

```
reddit-persona-generator/
├── main.py              # FastAPI web application
├── Summary.py           # Core analysis logic
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── templates/
│   ├── index.html       # Home page template
│   └── combined.html    # Persona display template
├── sample_users/        # Sample persona analyses
│   └── sample_user_analysis.txt
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `REDDIT_CLIENT_ID` | Reddit API client ID | Yes |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | Yes |
| `REDDIT_USER_AGENT` | Reddit API user agent | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `MONGODB_URI` | MongoDB connection string | No (defaults to local) |

### Customization

- **Data Limits**: By default, the app fetches 100 recent posts and comments. Modify in `Summary.py`:
  ```python
  posts = list(redditor.submissions.new(limit=100))
  comments = list(redditor.comments.new(limit=100))
  ```

- **Persona Fields**: Customize the persona analysis structure in the `json_format_definition` within `analyze_with_llm()` function

## 📊 Sample Output

The application generates personas with the following structure:

- **Basic Info**: Name, age, occupation, location, status
- **Personality Traits**: Key characteristics
- **Motivations**: What drives the user
- **Frustrations**: Common pain points
- **Goals & Needs**: Aspirations and requirements
- **Emotional Profile**: Scored analysis (0-100) for:
  - Happiness
  - Confidence
  - Anxiety
  - Anger
  - Sadness

## 🚨 Limitations & Considerations

- **Rate Limits**: Reddit API has rate limits (60 requests/minute)
- **Public Data Only**: Only analyzes publicly available posts/comments
- **Privacy**: Respect user privacy and Reddit's terms of service
- **AI Accuracy**: Persona analysis is AI-generated and may not be 100% accurate
- **Data Freshness**: Analysis based on recent activity (last 100 posts/comments)

## 🔒 Privacy & Ethics

- This tool only analyzes publicly available Reddit data
- No personal information is stored beyond what's publicly posted
- Users can request data deletion by contacting the administrator
- Follow Reddit's API terms of service and rate limiting guidelines

## 🐛 Troubleshooting

### Common Issues

1. **"FATAL: GEMINI_API_KEY not set"**
   - Ensure your `.env` file contains the correct `GEMINI_API_KEY`

2. **MongoDB Connection Error**
   - Check if MongoDB is running locally
   - Verify your `MONGODB_URI` is correct

3. **Reddit API Errors**
   - Verify your Reddit API credentials
   - Check if you're hitting rate limits
   - Ensure the username exists and has public posts

4. **Empty Persona Generated**
   - User might have no public posts/comments
   - Account might be too new or inactive
   - Check if the username is spelled correctly

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [PRAW](https://praw.readthedocs.io/) for Reddit API access
- [Google Gemini](https://ai.google.dev/) for AI-powered analysis
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Tailwind CSS](https://tailwindcss.com/) for styling

---

## 📧 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information about the problem

**Happy analyzing! 🎉**
