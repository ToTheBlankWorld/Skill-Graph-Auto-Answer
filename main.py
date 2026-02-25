import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from groq import Groq

# Load environment variables
load_dotenv()

EMAIL_OR_HALL = os.getenv('EMAIL_OR_HALL')
PASSWORD = os.getenv('PASSWORD')
LOGIN_URL = os.getenv('LOGIN_URL')
ASSESSMENT_URL = os.getenv('ASSESSMENT_URL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
SPEED_MODE = os.getenv('SPEED_MODE', 'default').lower()

class SkillGraphAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.option_inputs = {}  # Store radio button inputs for selection
        
    def start_browser(self):
        """Initialize and start Chrome browser"""
        print("Starting Chrome browser...")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-popup-blocking')
            
            self.driver = webdriver.Chrome(options=options)
            print("✓ Chrome browser opened successfully!")
            
            self.wait = WebDriverWait(self.driver, 15)
            time.sleep(2)
            print("✓ WebDriver ready!")
        except Exception as e:
            print(f"✗ Error starting browser: {e}")
            raise
            
            
        
    def login(self):
        """Login to Skill Graph"""
        print(f"\nNavigating to login page...")
        try:
            self.driver.get(LOGIN_URL)
            time.sleep(5)  # Wait longer for page to load
            print("✓ Login page loaded")
            
            # Increase wait timeout for finding elements
            wait_long = WebDriverWait(self.driver, 20)
            
            print("Looking for email/hall ticket field...")
            # Find username field - name="username"
            username_field = wait_long.until(
                EC.presence_of_element_located((By.NAME, "username")),
                message="Username field not found after 20 seconds"
            )
            print("✓ Email field found")
            
            print(f"Entering email: {EMAIL_OR_HALL}")
            username_field.clear()
            username_field.send_keys(EMAIL_OR_HALL)
            print(f"✓ Email/Hall entered: {EMAIL_OR_HALL}")
            
            print("Looking for password field...")
            # Find password field - name="password"
            password_field = self.driver.find_element(By.NAME, "password")
            print("✓ Password field found")
            
            print("Entering password...")
            password_field.clear()
            password_field.send_keys(PASSWORD)
            print("✓ Password entered")
            
            print("Looking for Sign in button...")
            # Click sign in button - type="submit" with class btn btn-primary btn-block
            sign_in_button = self.driver.find_element(
                By.XPATH, 
                "//button[@type='submit' and contains(@class, 'btn-primary')]"
            )
            print("✓ Sign in button found")
            
            print("Clicking Sign in button...")
            sign_in_button.click()
            print("Logging in... (waiting for redirect)")
            
            # Wait longer for page to load after login (the server might be slow)
            print("Please wait while the page redirects...")
            time.sleep(10)
            print("✓ Login successful!")
            return True
            
        except Exception as e:
            print(f"✗ Login failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def navigate_to_assessment(self):
        """Navigate to assessment page"""
        print(f"\nNavigating to assessment page...")
        try:
            self.driver.get(ASSESSMENT_URL)
            time.sleep(3)
            print("✓ Assessment page loaded")
        except Exception as e:
            print(f"✗ Error navigating to assessment: {e}")
        
    def wait_for_user_to_start_assessment(self):
        """Wait for user to select and resume the assessment"""
        print("\n" + "="*70)
        print("ASSESSMENT SELECTION - YOUR ACTION NEEDED")
        print("="*70)
        print("\nPlease do the following in the Chrome browser:")
        print("1. Look for the assessment in the list")
        print("2. Click on it to select it")
        print("3. Click the 'Resume' or 'Start' button")
        print("\nThe script will automatically start answering questions once")
        print("the first question appears on screen...")
        print("\n⏳ Waiting for you to start the assessment...")
        print("(You have up to 10 minutes to do this)")
        print("="*70 + "\n")
        
        # Wait for the question row to appear (indicating assessment has started)
        try:
            # Look for the question text element
            start_time = time.time()
            timeout = 600  # 10 minutes timeout
            
            while True:
                elapsed = time.time() - start_time
                
                # Check if question has appeared
                try:
                    self.driver.find_element(By.XPATH, "//div[@class='row pt-2']//span[contains(@style, 'font-family')]")
                    print("\n✓ Assessment loaded! Starting auto-answer mode...\n")
                    time.sleep(2)
                    return True
                except:
                    pass
                
                # Every 10 seconds, print a message to show script is still waiting
                if int(elapsed) % 10 == 0 and elapsed > 0:
                    remaining = int(timeout - elapsed)
                    if remaining > 0:
                        print(f"⏳ Still waiting... ({remaining} seconds remaining)")
                
                # Check if we've exceeded timeout
                if elapsed > timeout:
                    print(f"\n✗ Timeout: You didn't start the assessment within {timeout} seconds")
                    return False
                
                time.sleep(1)
                
        except Exception as e:
            print(f"✗ Error waiting for assessment: {e}")
            return False
    
    def extract_question_counter(self):
        """Extract question counter to see current/total (e.g., 'Ques 55 / 60')"""
        try:
            counter_element = self.driver.find_element(By.XPATH, "//h6[@class='font-weight-bold']")
            counter_text = counter_element.text.strip()  # "Ques 55 / 60"
            
            # Parse the counter (e.g., "Ques 55 / 60" -> (55, 60))
            parts = counter_text.split('/')
            if len(parts) == 2:
                current = int(parts[0].split()[-1].strip())
                total = int(parts[1].strip())
                return current, total
        except Exception as e:
            pass
        return None, None
    
    def is_last_question(self):
        """Check if current question is the last one (current == total)"""
        current, total = self.extract_question_counter()
        if current is not None and total is not None:
            return current == total
        return False
    
    def extract_question(self):
        """Extract current question text"""
        try:
            # Get question text from the row with pt-2 class containing span with font-family
            question_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='row pt-2']//span[contains(@style, 'font-family')]"))
            )
            question_text = question_element.text
            
            # Also get and display question counter
            current, total = self.extract_question_counter()
            if current and total:
                print(f"\n{'='*60}")
                print(f"Ques {current} / {total}")
                print(f"{'='*60}")
            
            print(f"\nQuestion: {question_text}")
            return question_text
        except Exception as e:
            print(f"Error extracting question: {e}")
            return None
    
    def extract_options(self):
        """Extract multiple choice options"""
        try:
            # Get all option elements
            option_labels = self.driver.find_elements(By.XPATH, "//label[@class='form-check-label']")
            print(f"  Found {len(option_labels)} options")
            
            options = {}
            option_inputs = {}
            
            for i, label in enumerate(option_labels):
                try:
                    # Try multiple ways to extract the text
                    option_text = None
                    
                    # Method 1: Try span > p
                    try:
                        option_text = label.find_element(By.XPATH, ".//span//p").text.strip()
                    except:
                        pass
                    
                    # Method 2: Try just span
                    if not option_text:
                        try:
                            option_text = label.find_element(By.XPATH, ".//span").text.strip()
                        except:
                            pass
                    
                    # Method 3: Get all text from the label
                    if not option_text:
                        option_text = label.text.strip()
                    
                    # Remove the radio button text if present
                    if option_text:
                        # Remove leading/trailing whitespace and special characters
                        option_text = option_text.strip()
                        
                        # If the text contains newlines, take the last part (usually the actual option)
                        lines = option_text.split('\n')
                        option_text = lines[-1].strip() if lines else option_text
                        
                        if option_text:
                            letter = chr(65 + i)  # A, B, C, D...
                            options[letter] = option_text
                            
                            # Store the input element for later use
                            input_elem = label.find_element(By.XPATH, ".//input[@type='radio']")
                            option_inputs[letter] = input_elem
                            print(f"  {letter}) {option_text}")
                except Exception as e:
                    print(f"  Error extracting option {i}: {e}")
            
            # Store the input elements as instance variable
            self.option_inputs = option_inputs
            return options
        except Exception as e:
            print(f"Error extracting options: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_ai_answer(self, question, options):
        """Use Groq API to get answer to the question"""
        try:
            print("\nAsking AI for answer...")
            
            if not GROQ_API_KEY:
                print("✗ Error: Groq API key not found!")
                return None
            
            # Initialize Groq client
            client = Groq(api_key=GROQ_API_KEY)
            
            options_text = "\n".join([f"{key}: {value}" for key, value in options.items()])
            prompt = f"""You are an educational assistant. Answer the following question by choosing the correct option.

Question: {question}

Options:
{options_text}

Solve this step by step and provide your detailed explanation. At the very end, you MUST respond with:

FINAL ANSWER: [SINGLE LETTER - A or B or C or D]

Replace [SINGLE LETTER - A or B or C or D] with only the correct letter (A, B, C, or D). This is mandatory."""
            
            try:
                print(f"  Using model: llama-3.1-8b-instant")
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are an educational assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                if response and response.choices:
                    answer = response.choices[0].message.content.strip()
                    print(f"✓ AI Answer: {answer}")
                    return answer
            except Exception as e:
                print(f"  ✗ Model failed: {str(e)[:100]}")
                return None
            
            return None
            
        except Exception as e:
            print(f"✗ AI Error: {str(e)[:80]}")
            return None
    
    def parse_answer_letter(self, answer_text, options):
        """Parse the answer letter from AI response with better logic"""
        if not answer_text:
            return None
        
        answer_text_upper = answer_text.upper()
        available_letters = list(options.keys())
        
        # Method 1: Look for "FINAL ANSWER: X" pattern (most reliable)
        import re
        final_answer_pattern = r'FINAL\s+ANSWER\s*:\s*([A-D])'
        match = re.search(final_answer_pattern, answer_text_upper)
        if match:
            letter = match.group(1)
            if letter in available_letters:
                print(f"  (Extracted FINAL ANSWER: {letter})")
                return letter
        
        # Method 2: Look for other clear patterns
        patterns = [
            r'(?:answer|option)\s*[:\s]+([A-D])',  # "Answer: C" or "Option C"
            r'^([A-D])[\s\.\)]',  # Starts with letter followed by space/dot/paren
            r'\*\*([A-D])\*\*',  # **C** (bold markdown)
            r'`([A-D])`',  # `C` (code block)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, answer_text_upper)
            if match:
                letter = match.group(1)
                if letter in available_letters:
                    print(f"  (Parsed from: {answer_text[:60]}...)")
                    return letter
        
        # Method 3: Look for any letter A-D that exists in options
        for letter in available_letters:
            if letter in answer_text_upper:
                # Check context - avoid matching letters in explanations
                idx = answer_text_upper.find(letter)
                # Check if it has option-like context
                context = answer_text_upper[max(0, idx-10):min(len(answer_text_upper), idx+10)]
                if any(word in context for word in ['OPTION', 'ANSWER', 'CORRECT', 'CHOICE', 'FINAL']):
                    print(f"  (Parsed from: {answer_text[:60]}...)")
                    return letter
        
        # Method 4: Just take first valid letter found
        for char in answer_text_upper:
            if char in available_letters:
                print(f"  (Parsed from: {answer_text[:60]}...)")
                return char
        
        return None

    def find_and_select_answer(self, answer_text, options):
        """Find the answer in options and select it"""
        try:
            # Extract the letter from AI response with better parsing
            answer_letter = self.parse_answer_letter(answer_text, options)
            
            if not answer_letter:
                print("Could not extract answer letter")
                return False
            
            # Check if answer exists in options
            if answer_letter not in options:
                print(f"Answer option '{answer_letter}' not found in choices!")
                print("Please manually select the correct option and continue...")
                self.wait_for_continue()
                return False
            
            # Find and click the option
            option_text = options[answer_letter]
            print(f"Selecting option {answer_letter}: {option_text}")
            
            # Use the stored input element from extract_options
            if hasattr(self, 'option_inputs') and answer_letter in self.option_inputs:
                input_elem = self.option_inputs[answer_letter]
                # Scroll into view before clicking
                self.driver.execute_script("arguments[0].scrollIntoView(true);", input_elem)
                time.sleep(0.5)
                # Click the radio button
                input_elem.click()
            else:
                # Fallback: try to find by text
                option_element = self.driver.find_element(
                    By.XPATH, 
                    f"//span//p[contains(text(), '{option_text}')]/../..//input[@type='radio']"
                )
                option_element.click()
            
            time.sleep(1)
            print(f"Option {answer_letter} selected!")
            return True
            
        except Exception as e:
            print(f"Error selecting answer: {e}")
            return False
    
    def wait_for_continue(self):
        """Wait for user to click continue button"""
        print("\nWaiting for you to click 'Save & Next'...")
        input("Press Enter after you've manually selected and are ready to continue...")
    
    def click_save_next(self):
        """Click the 'Save & Next' button"""
        try:
            print("Clicking 'Save & Next' button...")
            save_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Save')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            time.sleep(0.5)
            try:
                save_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", save_button)
            
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Error clicking button: {e}")
            return False
    
    def check_assessment_complete(self):
        """Check if assessment is complete"""
        try:
            # Look for submit or completion buttons
            submit_buttons = self.driver.find_elements(
                By.XPATH, 
                "//button[contains(text(), 'Submit') or contains(text(), 'Complete') or contains(text(), 'Finish')]"
            )
            
            # If we find a submit button instead of Save & Next, assessment is near completion
            if len(submit_buttons) > 0:
                return True
            
            # Also check if Save & Next button is disabled
            save_buttons = self.driver.find_elements(
                By.XPATH,
                "//button[contains(@class, 'btn-primary') and contains(text(), 'Save')]"
            )
            if len(save_buttons) > 0:
                # If button is disabled, assessment might be complete
                return save_buttons[0].get_attribute('disabled') is not None
            
            return False
        except:
            return False
    
    def process_questions(self):
        """Process all questions in the assessment"""
        question_count = 0
        max_questions = 100  # Safety limit
        consecutive_fails = 0
        max_failures = 3
        
        while question_count < max_questions:
            question_count += 1
            print(f"\n{'='*60}")
            print(f"Processing Question {question_count}")
            print(f"{'='*60}")
            
            # Extract question and options
            question = self.extract_question()
            if not question:
                print("Could not extract question")
                consecutive_fails += 1
                if consecutive_fails >= max_failures:
                    print("Multiple extraction failures - assessment likely complete")
                    break
                time.sleep(2)
                continue
            
            consecutive_fails = 0  # Reset failure counter on success
            
            options = self.extract_options()
            if not options:
                print("Could not extract options")
                break
            
            # Get AI answer
            answer = self.get_ai_answer(question, options)
            manual_selection = False
            
            if not answer:
                print("Could not get AI answer, asking for manual selection...")
                self.wait_for_continue()
                manual_selection = True
            else:
                # Try to select the answer
                if not self.find_and_select_answer(answer, options):
                    # Answer not in choices, wait for manual selection
                    self.wait_for_continue()
                    manual_selection = True
            
            # Check if this is the last question
            if self.is_last_question():
                print("\n" + "="*60)
                print("✓ FINAL QUESTION ANSWERED!")
                print("✓ EXAM DONE!")
                print("="*60)
                break
            
            # Click Save & Next for non-final questions
            if not self.click_save_next():
                print("Could not click Save & Next button")
                break
            
            time.sleep(2)
        
        print(f"\n{'='*60}")
        print("Assessment Processing Complete!")
        print(f"Total questions processed: {question_count}")
        print(f"{'='*60}")
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            print("Closing browser...")
            self.driver.quit()
    
    def run(self):
        """Main execution flow"""
        try:
            print("\n" + "="*60)
            print("SKILL GRAPH AUTOMATION STARTING")
            print("="*60)
            print(f"Email/Hall: {EMAIL_OR_HALL}")
            print(f"Assessment URL: {ASSESSMENT_URL}")
            print("="*60 + "\n")
            
            self.start_browser()
            
            if not self.login():
                print("✗ Login failed")
                print("\nBrowser will stay open for 30 seconds to see the error...")
                time.sleep(30)
                return
            
            self.navigate_to_assessment()
            
            if not self.wait_for_user_to_start_assessment():
                print("\n✗ Assessment not started in time")
                print("\nBrowser will stay open for 30 seconds...")
                time.sleep(30)
                return
            
            self.process_questions()
            
            time.sleep(3)
            print("\n" + "="*60)
            print("✓ EXAM DONE!")
            print("="*60)
            print("\n📋 Next Steps:")
            print("1. Chrome browser is still open with your exam")
            print("2. Review your answers if needed")
            print("3. Manually click 'Submit' button in the browser")
            print("4. After submission, press any key to end the script")
            print("\n" + "="*60)
            
            # Wait for user to submit and then press key
            input("\nPress Enter after you have submitted the exam...")
            
            print("\n" + "="*60)
            print("✓ Thank you! Closing script...")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n✗ Script interrupted by user")
        except Exception as e:
            print(f"\n✗ Error in main execution: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Don't close browser automatically - let user see results
            print("\nBrowser is still open - close it manually when you're done.")
            time.sleep(1)

if __name__ == "__main__":
    automation = SkillGraphAutomation()
    automation.run()
