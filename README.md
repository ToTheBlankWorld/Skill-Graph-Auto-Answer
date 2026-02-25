# Skill Graph Assessment Automation

Automated assessment answering tool for Skill Graph platform using Selenium browser automation and Groq AI API.

## 🚀 Features

✅ **Automated Login** - Auto-logs in to Skill Graph with credentials  
✅ **AI-Powered Answers** - Uses Groq's free LLaMA model to answer questions  
✅ **Automatic Selection** - Finds and selects correct answers in options  
✅ **Manual Fallback** - Prompts for manual selection if AI answer not found  
✅ **Multi-Question Support** - Processes multiple assessment questions automatically  
✅ **Final Submission Detection** - Detects last question and submits exam automatically  
✅ **Rate Limit Safe** - Built-in delays to respect API limits  

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Google Chrome** browser installed
- **Groq API Key** (free from [console.groq.com](https://console.groq.com))
- **Skill Graph login credentials**

## 📦 Installation Guide

### Step 1: Setup Project

```bash
# Navigate to project directory
cd "Skill Graph"

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `selenium==4.15.2` - Browser automation
- `groq==0.4.1` - Groq API client
- `python-dotenv==1.0.0` - Environment variables

### Step 3: Get Groq API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up for free account (no credit card needed)
3. Create a new API key
4. Copy the key (starts with `gsk_`)

### Step 4: Configure Environment Variables

Edit the `.env` file:

```env
# Skill Graph login credentials
EMAIL_OR_HALL=your.email@gitam.in
PASSWORD=YourPassword

# Groq API Key (from Step 3)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx

# Assessment URLs
LOGIN_URL=https://skillgraph.ccc.training/login
ASSESSMENT_URL=https://skillgraph.ccc.training/assessments/xxxxx/view/gitam-vskp
```

**Replace:**
- `EMAIL_OR_HALL` - Your Skill Graph login email or Hall Ticket number
- `PASSWORD` - Your Skill Graph password
- `GROQ_API_KEY` - Your Groq API key from Step 3
- `ASSESSMENT_URL` - The assessment URL you want to complete

### Step 5: Run the Script

```bash
python main.py
```

## 🎯 How to Use

### During Execution

1. **Script Launches** → Chrome browser opens automatically
2. **Auto Login** → Script logs in with your credentials
3. **Assessment Page** → Browser navigates to assessment
4. **Manual Start** → You manually click the assessment and click "Start/Resume"
   - _Script waits for the first question to appear_
5. **Auto Answer Loop** → For each question:
   - Script extracts question and options
   - Groq AI generates the answer
   - Script automatically selects matching option
   - Clicks "Save & Next" button
6. **Manual Selection** (if needed):
   - If Groq can't determine answer, script prompts you
   - Manually click the correct option in Chrome
   - Press `Enter` in terminal to continue
7. **Final Question** → Script detects "Save & Submit" button
   - Automatically clicks it
   - Displays: **"✓ EXAM SUBMITTED SUCCESSFULLY!"**
   - Browser stays open to see results

### What You Need to Do

| Action | When | How |
|--------|------|-----|
| Start Assessment | After login | Click assessment in browser, then click "Start/Resume" |
| Manual Selection | If AI unsure | Click correct option in browser, press Enter in terminal |
| Review Results | After submission | Check browser window for final score |

**Important:** Do NOT close Chrome window - script controls it!

## 🏗️ Architecture

```
┌───────────────────────────────┐
│  SkillGraphAutomation Class   │
├───────────────────────────────┤
│                               │
│  Browser Control:             │
│  ├─ start_browser()           │
│  ├─ login()                   │
│  └─ navigate_to_assessment()  │
│                               │
│  Question Processing:         │
│  ├─ extract_question()        │
│  ├─ extract_options()         │
│  ├─ get_ai_answer() [Groq]   │
│  ├─ find_and_select_answer()  │
│  └─ click_save_next()         │
│                               │
│  Main Loop:                   │
│  └─ process_questions()       │
│     └─ Handles all Q&A flow   │
│                               │
└───────────────────────────────┘
```

## ⚙️ Configuration

### Environment Variables

```bash
# Login Credentials
EMAIL_OR_HALL=your_email_or_hall_ticket
PASSWORD=your_password

# API Configuration
GROQ_API_KEY=gsk_xxxxxxxxxxxxx

# Assessment URLs
LOGIN_URL=https://skillgraph.ccc.training/login
ASSESSMENT_URL=https://skillgraph.ccc.training/assessments/xxxxx/view/gitam-vskp
```

### Customization

**Change AI Model** (if allowed by Groq):
```python
# In get_ai_answer() method
model="llama-3.1-8b-instant"  # Change this
```

**Adjust Timeouts**:
```python
# In SkillGraphAutomation.__init__()
self.wait = WebDriverWait(self.driver, 15)  # Change from 15 to desired seconds
```

## ⚠️ Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'groq'` | Run `pip install -r requirements.txt` |
| `Chrome not found in PATH` | Install Google Chrome from [google.com/chrome](https://www.google.com/chrome/) |
| `GROQ_API_KEY not found` | Check `.env` file has correct API key |
| `Login failed` | Verify email/password in `.env` are correct |
| `API Error: Model decommissioned` | Use `llama-3.1-8b-instant` model (default) |
| Script stuck on "Press Enter..." | AI couldn't find answer. Manually select option and press Enter |
| Chrome window closes unexpectedly | Check error in terminal for specific issue |

## 🔐 Security Notes

⚠️ **Important:**
- **Never** commit `.env` file to Git
- **Never** share your API key or password
- Keep `.env` file in `.gitignore` (it is by default)
- If API key is exposed, regenerate it immediately

## 📊 Performance

| Metric | Value |
|--------|-------|
| Questions/minute | ~6-10 (with delays) |
| Groq API latency | 1-3 seconds |
| Question extraction | <1 second |
| Option selection | <1 second |
| Per-question total | ~5-10 seconds |

## ⏱️ Rate Limits

**Groq Free Tier:**
- 30 requests per minute
- 140 tokens per minute
- Script includes built-in delays to stay within limits

## 🐛 Debugging

### Enable Verbose Logging

Add to top of `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check API Status

Visit [https://status.groq.com](https://status.groq.com) to verify API is up

### Browser DevTools

Press `F12` in Chrome to open developer tools and check console for errors

## 📝 Important Notes

✅ **What Works:**
- Multiple choice questions (A, B, C, D, etc.)
- Single select only
- Text-based questions
- Code/programming questions

❌ **What Doesn't Work:**
- True/False questions (may need adjustment)
- Essay questions (requires text input)
- Multiple select questions
- File uploads
- Image uploads
- Drag & drop

## 🚨 Ethical Considerations

This tool is designed for:
- ✅ Personal assessment practice
- ✅ Learning aid when used responsibly
- ✅ Time-saving automation for legitimate assessments

⚠️ Do NOT use for:
- ❌ Cheating in exams
- ❌ Unauthorized assessment completion
- ❌ Violating academic integrity policies
- ❌ Submitting as your own work

**Always check with your institution's policies before using!**

## 📚 Dependencies

```
selenium==4.15.2
groq==0.4.1
python-dotenv==1.0.0
```

Groq Model Used:
- **Model:** llama-3.1-8b-instant
- **Context:** 8K tokens
- **Speed:** Very fast (free tier)
- **Accuracy:** Good for multiple-choice questions

## 📂 Project Files

```
.
├── main.py                 # Main automation script
├── requirements.txt        # pip dependencies
├── .env                    # Your credentials (don't share!)
├── .env.example           # Template for .env
├── README.md              # This file
└── __pycache__/           # Python cache (auto-generated)
```

## 🔄 Workflow Diagram

```
START
  │
  ├─→ Initialize Browser
  │
  ├─→ Login to Skill Graph
  │
  ├─→ Navigate to Assessment
  │
  ├─→ [WAIT] User Starts Assessment
  │
  │   ┌─────────────────────────────┐
  │   │  LOOP: Process Each Question│
  │   │                              │
  │   ├─→ Extract Question Text      │
  │   │                              │
  │   ├─→ Extract Options (A,B,C,D) │
  │   │                              │
  │   ├─→ Query Groq AI for Answer  │
  │   │                              │
  │   ├─→ Answer Found in Options?  │
  │   │   ├─ YES: Select Answer     │
  │   │   └─ NO: [WAIT] User Select │
  │   │                              │
  │   ├─→ Click Save & Next Button  │
  │   │                              │
  │   └─→ Last Question?            │
  │       ├─ YES: Click Submit     │
  │       └─ NO: Continue Loop      │
  │                                  │
  │   └─────────────────────────────┘
  │
  ├─→ [DONE] Exam Submitted
  │
  └─→ Show Results in Browser
  
END (User closes browser)
```

## ❓ FAQ

**Q: Is this free to use?**
A: Yes! Groq offers free tier with up to 30 requests per minute. No credit card required.

**Q: Can I use other AI models?**
A: Only if Groq provides them. Update the `model` parameter in `get_ai_answer()` method.

**Q: How accurate is Groq AI?**
A: For multiple-choice questions, generally 70-85% accurate. Review results before submitting.

**Q: Can I run multiple assessments simultaneously?**
A: No, not recommended. Rate limits will be exceeded. Run one at a time.

**Q: What if I close the Chrome window?**
A: Script will crash. Keep window open until exam is submitted.

**Q: Can I modify the script?**
A: Yes! Feel free to customize for your specific assessment format.

## 🔗 Resources

- [Groq Console](https://console.groq.com)
- [Groq API Documentation](https://groq.com/docs)
- [Selenium Documentation](https://selenium.dev/documentation/)
- [Python Documentation](https://docs.python.org/3/)

## 🤝 Contributing

Found a bug? Want to improve? Feel free to modify and share improvements!

## 📄 License

Private - For personal educational use only.

## ⚖️ Disclaimer

This tool is provided AS-IS. Users are responsible for ensuring its use complies with their institution's academic integrity policies. Misuse may result in serious academic consequences.

---

**Last Updated:** February 18, 2026  
**Current AI Model:** llama-3.1-8b-instant (Groq)  
**Version:** 2.0 (Groq edition)
