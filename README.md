# Gipherr

This is a **Telegram bot** that allows users to track the total views of GIFs from Giphy. Users can add projects with GIF URLs, check their view counts, and receive **daily updates**.

## 🚀 Features
- Add GIFs to track using `/setproject <name> <GIF_URL>`
- View all added projects with `/listprojects`
- Fetch view counts with `/getviews`
- Remove a project with `/removeproject <name>`
- **Automatic daily updates** at **8 AM** and **8 PM**

## 🛠 Setup Instructions

### 1️⃣ Install Dependencies
Ensure you have **Python** installed, then run:
```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up `.env`
Create a `.env` file in the project directory and add:
```
TELEGRAM_BOT_KEY=your_bot_token_here
```

### 3️⃣ Run the Bot
```bash
python bot.py
```

## 📌 Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/setproject <name> <GIF_URL>` | Add a GIF to track |
| `/listprojects` | List all added projects |
| `/getviews` | Fetch view counts for all GIFs |
| `/removeproject <name>` | Remove a project |


### Enjoy!

#### For any queries or support, please contact us at 72pxperinch@gmail.com.


