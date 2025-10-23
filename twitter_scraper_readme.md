# Twitter Comment Scraper

A sophisticated Python script that uses Playwright to scrape comments from Twitter/X posts with advanced stealth techniques to avoid detection.

## Features

- 🎭 **Stealth Mode**: Advanced browser fingerprinting protection and anti-detection measures
- 🔐 **Session Persistence**: Saves authentication state to avoid repeated logins
- 🤖 **Human-like Behavior**: Random mouse movements and realistic delays
- 📊 **Structured Data**: Extracts comments with metadata (user IDs, comment IDs, reply relationships)
- 💾 **JSON Export**: Saves extracted comments to a structured JSON file

## Prerequisites

- Python 3.7+
- Chrome/Chromium browser installed
- Valid Twitter/X account

## Installation

1. **Clone or download this script**

2. **Install required packages**:
```bash
pip install playwright requests
```

3. **Install Playwright browsers**:
```bash
playwright install chrome
```

## Configuration

Before running the script, you need to configure the target post URL:

1. Open the script in your editor
2. Update the `POST_URL` variable with your target tweet:
```python
POST_URL = "https://x.com/USERNAME/status/TWEET_ID"
```

3. **Get the TweetDetail API URL**:
   - Open the tweet in your browser
   - Open Developer Tools (F12)
   - Go to Network tab
   - Filter for "TweetDetail"
   - Find the request and copy the full URL with query parameters
   - Update `TWEET_DETAIL_FULL_URL` in the script

## Usage

### First Run (Login Required)

```bash
python scraper.py
```

On first run:
1. The script will open Chrome and navigate to Twitter login
2. Because of getting timeouterror Manually log in to your Twitter account 
3. After successful login, press ENTER in the terminal
4. The session will be saved to `auth_state.json`



The script will use the saved session from `auth_state.json` and automatically:
- Navigate to the target post
- GraphQL Request
- The script calls the TweetDetail endpoint with the same headers as an authenticated X browser.
- Parses JSON to extract all full_text and comment-related objects.
- Extract comments using the Twitter API
- Save results to `comments.json`

## Output

The script generates `comments.json` with two sections:

```json
{
  "full_texts": [
    "Comment text 1",
    "Comment text 2",
    ...
  ],
  "comment_objects": [
    {
      "full_text": "Comment text",
      "id_str": "1234567890",
      "user_id_str": "9876543210",
      "in_reply_to_status_id_str": "1234567890"
    },
    ...
  ]
}
```

## Features Explained

### Stealth Techniques

- **Browser Fingerprinting Protection**: Masks automation indicators
- **Random User Agents**: Rotates between multiple realistic user agents
- **Variable Viewports**: Uses different screen resolutions
- **Canvas Fingerprinting**: Adds noise to canvas API
- **WebGL Spoofing**: Masks GPU information
- **Human-like Timing**: Random delays between actions
- **Mouse Movement**: Simulates natural cursor movement

### Session Management

- Authentication state is saved in `auth_state.json`
- Includes cookies, local storage, and session data
- Automatically reused on subsequent runs
- Delete the file to force a fresh login

## Troubleshooting

### "Storage state not found" Error
- This is normal on first run
- Follow the login prompts

### Login Issues
- Delete `auth_state.json` and try again
- Ensure you're using a valid Twitter account
- Check for any Twitter security challenges

### No Comments Extracted
- Verify the `TWEET_DETAIL_FULL_URL` is correct
- Check that the tweet has public comments
- Ensure the tweet ID in both URLs matches

### Browser Detection
- The script includes extensive stealth measures
- If detected, try:
  - Using a different IP address
  - Waiting before retrying
  - Updating user agents in the script

## File Structure

```
.
├── scraper.py           # Main script
├── auth_state.json      # Session storage (generated)
├── comments.json        # Extracted comments (generated)
└── README.md           # This file
```

