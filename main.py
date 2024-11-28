import openai
import time
import random
from pynput.keyboard import Controller, Key

# set your openai api key
openai.api_key = "YOUR_API_KEY_HERE"

# this lets us control the keyboard
keyboard = Controller()

# configuration variables
timeWait = (30, 50)  # how often it should wait, range for randomness
grammarAccuracy = 50  # set grammar accuracy 1-100 (100 = perfect grammar, 1 = poor grammar)
wpm = 60  # typing speed in words per minute (adjust based on your preference) recommend using human benchmark to work out your WPM

def get_openai_response(prompt, model="gpt-4o-mini"):
    """
    talks to openai and gets a response with instructions to set the grammar accuracy
    """
    # adjust the prompt to instruct OpenAI on the level of grammar to use
    prompt_with_grammar_instructions = f"Please respond with {grammarAccuracy}% grammatical accuracy, meaning the response should have some mistakes and not be perfectly structured.\n\n{prompt}"

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt_with_grammar_instructions}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"couldn't talk to openai: {str(e)}"

def simulate_typing(text):
    """
    types out the text slowly, with mistakes, pauses, and grammar adjustments
    """
    # calculate typing delay based on wpm (words per minute)
    words = len(text.split())
    typing_delay = 60 / (wpm * 5)  # approximate delay per character (assuming ~5 chars/word)

    for i, char in enumerate(text):
        # sometimes, pause for a few seconds like you're thinking
        if random.randint(*timeWait) == 1:  # small chance to pause
            pause_duration = random.uniform(2, 5)  # pause between 2 and 5 seconds
            print(f"\n[pausing for {pause_duration:.1f} seconds...]\n")
            time.sleep(pause_duration)

        # introduce small grammar mistakes based on grammarAccuracy
        if random.randint(1, 100) > grammarAccuracy:  # lower accuracy = more mistakes (need to fix it making mistakes to much)
            if char.isalpha():  # only make mistakes on letters
                mistake_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                keyboard.type(mistake_char)
                time.sleep(0.05)
                # backspace to "fix" the typo
                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
                time.sleep(0.1)

        # type the actual character with a delay
        keyboard.type(char)
        time.sleep(random.uniform(typing_delay * 0.8, typing_delay * 1.2))  # add natural variation

def main():
    print("ask me something:")
    user_input = input("> ")
    print("\nthinking...\n")
    response = get_openai_response(user_input)
    print("typing response into active window...")
    print("you have 2 seconds to go onto your preffered editor!")
    time.sleep(2)  # gives you time to switch to the google doc
    simulate_typing(response)

if __name__ == "__main__":
    main()
