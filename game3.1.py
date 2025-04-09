import logging
import random
from telethon import TelegramClient, events
from colorama import Fore, Style

# 🔹 Configurable Settings
API_ID = 24600747
API_HASH = "bb28ae5ce2b87fa5a6e31e64ba8ea7e2"
SESSION_NAME = "wordseek"
GROUP_ID = -1002378227989
WORDLIST_FILE = "/storage/emulated/0/seekword.txt"

# 🔹 Logging Setup (Colorful & Bold)
logging.basicConfig(
    format=f"{Fore.YELLOW + Style.BRIGHT}%(asctime)s - %(message)s{Style.RESET_ALL}",
    level=logging.INFO
)

# 🔹 Load Wordlist
def load_words(file_path):
    try:
        with open(file_path, "r") as f:
            words = [line.strip().upper() for line in f.readlines() if len(line.strip()) == 5]
        logging.info(f"{Fore.GREEN}📂 Total words loaded: {len(words)}{Style.RESET_ALL}")
        return words
    except Exception as e:
        logging.error(f"{Fore.RED}🚨 Error loading words: {e}{Style.RESET_ALL}")
        return []

WORDS = load_words(WORDLIST_FILE)

# 🔹 Bot Setup
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# 🔹 Game Data
games = {}

# 🔹 Used Words Memory (Temporary Storage)
used_words = set()

# 🔹 Select Best Guess (Avoiding Used Words)
def get_best_guess(remaining_words):
    available_words = [word for word in remaining_words if word not in used_words]
    return random.choice(available_words) if available_words else None

# 🔹 Filter Words Based on Feedback
def filter_words(last_guess, feedback, word_list):
    pattern = list("_____")
    new_list = []

    for i, mark in enumerate(feedback):
        if mark == "🟩":
            pattern[i] = last_guess[i]

    for word in word_list:
        if word == last_guess or word in used_words:
            continue

        valid = True
        for i, mark in enumerate(feedback):
            if (mark == "🟥" and last_guess[i] in word) or \
               (mark == "🟨" and (last_guess[i] not in word or last_guess[i] == word[i])) or \
               (mark == "🟩" and last_guess[i] != word[i]):
                valid = False
                break

        if valid:
            new_list.append(word)

    logging.info(f"{Fore.CYAN}🔎 Words left after filtering: {len(new_list)}{Style.RESET_ALL}")

    # Fallback: Pattern Matching (Backup System)
    if len(new_list) == 0:
        matched_words = [word for word in WORDS if all(p == "_" or p == w for p, w in zip(pattern, word)) and word not in used_words]
        if matched_words:
            logging.info(f"{Fore.LIGHTBLUE_EX}🔄 Using Backup Pattern Matching...{Style.RESET_ALL}")
            return matched_words

    return new_list

# 🔹 Handle Incoming Messages
@client.on(events.NewMessage(chats=GROUP_ID))
async def handle_message(event):
    global used_words
    text = event.text.strip()
    logging.info(f"{Fore.BLUE}📩 New message received: {text}{Style.RESET_ALL}")

    # 🎮 Start Game
    if "game started" in text.lower():
        chat_id = event.chat_id
        games[chat_id] = {"possible_words": WORDS.copy(), "guesses": [], "feedback": []}
        used_words.clear()  # 🔄 Reset Used Words on New Game
        logging.info(f"{Fore.MAGENTA}🎮 Game started in chat {chat_id}{Style.RESET_ALL}")

        first_guess = get_best_guess(games[chat_id]["possible_words"])
        if first_guess:
            used_words.add(first_guess)  # ✅ Mark word as used
            await client.send_message(GROUP_ID, first_guess)
            logging.info(f"{Fore.GREEN}✅ First guess sent: {first_guess}{Style.RESET_ALL}")

    # 🟢 Restart Game on Win
    elif "Congrats! You guessed it correctly." in text:
        logging.info(f"{Fore.YELLOW}🎉 Game won! Restarting...{Style.RESET_ALL}")
        await client.send_message(GROUP_ID, "/new@WordSeek2Bot")

    # 🔎 Process Feedback
    elif any(emoji in text for emoji in ["🟩", "🟨", "🟥"]):
        chat_id = event.chat_id
        if chat_id not in games:
            logging.warning(f"{Fore.RED}⚠️ Feedback received but game not found!{Style.RESET_ALL}")
            return

        lines = text.split("\n")
        last_line = lines[-1].split()
        guess, feedback = last_line[-1].upper(), last_line[:-1]

        logging.info(f"{Fore.LIGHTMAGENTA_EX}🔠 Extracted Guess: {guess}{Style.RESET_ALL}")
        logging.info(f"{Fore.LIGHTCYAN_EX}📊 Extracted Feedback: {feedback}{Style.RESET_ALL}")

        games[chat_id]["guesses"].append(guess)
        games[chat_id]["feedback"].append(feedback)
        filtered_words = filter_words(guess, feedback, games[chat_id]["possible_words"])

        # Backup System Activation if No Valid Words Found
        if not filtered_words:
            logging.info(f"{Fore.RED}🚨 No valid words found! Activating Backup System...{Style.RESET_ALL}")
            filtered_words = filter_words(guess, feedback, WORDS)  # Use full word list with pattern match

        games[chat_id]["possible_words"] = filtered_words

        # Sending Words One-by-One if Multiple Matches Exist
        if len(filtered_words) == 1:
            next_guess = filtered_words[0]
        else:
            next_guess = get_best_guess(filtered_words)  # Ensure No Repeated Words

        if next_guess:
            used_words.add(next_guess)  # ✅ Mark word as used
            await client.send_message(GROUP_ID, next_guess)
            logging.info(f"{Fore.GREEN}✅ Next guess sent: {next_guess}{Style.RESET_ALL}")

# 🔹 Run Bot
async def main():
    await client.start()
    logging.info(f"{Fore.LIGHTGREEN_EX}🤖 Bot is running...{Style.RESET_ALL}")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
