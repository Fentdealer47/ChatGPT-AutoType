import openai
import time
import random
from pynput.keyboard import Controller, Key

# set your openai api key
openai.api_key = "" # insert your open ai key here

# this lets us control the keyboard
keyboard = Controller()

def get_openai_response(prompt, model="gpt-4o-mini"):
    """
    talks to openai and gets a response
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"couldn't talk to openai: {str(e)}"

def simulate_typing(text):
    """
    types out the text slowly, with mistakes and pauses
    """
    for i, char in enumerate(text):
        # sometimes, pause for a few seconds like you're thinking
        if random.randint(1, 50) == 1:  # small chance to pause
            pause_duration = random.uniform(2, 5)  # pause between 2 and 5 seconds
            print(f"\n[pausing for {pause_duration:.1f} seconds...]\n")
            time.sleep(pause_duration)
        
        # occasionally make a typo, then fix it
        if random.randint(1, 20) == 1:  # small chance to mess up
            mistake_char = random.choice("abcdefghijklmnopqrstuvwxyz")  # random wrong letter
            keyboard.type(mistake_char)
            time.sleep(0.05)
            # backspace to "fix" the typo
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            time.sleep(0.1)
        
        # type the actual character with a small delay
        keyboard.type(char)
        time.sleep(random.uniform(0.03, 0.1))  # random typing speed

def main():
    print("ask me something:")
    user_input = input("> ")
    print("\nthinking...\n")
    response = get_openai_response(user_input)
    print("typing response into active window...")
    time.sleep(2)  # gives you time to switch to the google doc or whatever
    simulate_typing(response)

if __name__ == "__main__":
    main()
