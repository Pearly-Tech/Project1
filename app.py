import streamlit as st
import random

def binary_search_game():
    st.title("Binary Search Guessing Game")
    
    mode = st.radio("Select mode:", ("User Guessing", "Machine Guessing"))

    # Set the range for the random number
    low = st.number_input("Enter the lower bound:", value=1)
    high = st.number_input("Enter the upper bound:", value=100)

    if st.button("Start Game"):
        if mode == "User Guessing":
            # Generate a random number
            secret_number = random.randint(low, high)
            st.session_state.secret_number = secret_number
            st.session_state.attempts = 0
            st.session_state.feedback = ""
            st.session_state.guess_history = []
        else:
            st.session_state.low = low
            st.session_state.high = high
            st.session_state.attempts = 0
            st.session_state.guess = None
            st.session_state.feedback = ""

    if mode == "User Guessing":
        if 'secret_number' in st.session_state:
            guess = st.number_input("Make a guess:", value=low, min_value=low, max_value=high)
            if st.button("Submit Guess"):
                st.session_state.attempts += 1
                st.session_state.guess_history.append(guess)
                if guess < st.session_state.secret_number:
                    st.session_state.feedback = "Too low! Try again."
                elif guess > st.session_state.secret_number:
                    st.session_state.feedback = "Too high! Try again."
                else:
                    st.session_state.feedback = f"Congratulations! You've guessed the number {st.session_state.secret_number} in {st.session_state.attempts} attempts!"
            
            st.write(st.session_state.feedback)
            st.write(f"Guess History: {st.session_state.guess_history}")

            if st.session_state.feedback.startswith("Congratulations"):
                if st.button("Play Again"):
                    del st.session_state['secret_number']
                    del st.session_state['attempts']
                    del st.session_state['feedback']
                    del st.session_state['guess_history']
    
    elif mode == "Machine Guessing":
        if 'low' in st.session_state and 'high' in st.session_state:
            if st.session_state.attempts == 0:
                st.session_state.feedback = "Think of a number between {} and {}!".format(low, high)

            if st.session_state.attempts < 10:  # Limit to a number of attempts
                guess = (st.session_state.low + st.session_state.high) // 2
                st.session_state.guess = guess
                st.session_state.attempts += 1

                st.write(f"Machine guesses: {guess}")

                response = st.radio("Is the guess correct?", ("Correct", "Too Low", "Too High"), key='machine_response')

                if response == "Too Low":
                    st.session_state.low = guess + 1
                    st.session_state.feedback = "Machine will try again!"
                elif response == "Too High":
                    st.session_state.high = guess - 1
                    st.session_state.feedback = "Machine will try again!"
                else:  # Correct
                    st.session_state.feedback = f"Machine guessed the number {guess} in {st.session_state.attempts} attempts!"
                    if st.button("Play Again"):
                        del st.session_state['low']
                        del st.session_state['high']
                        del st.session_state['attempts']
                        del st.session_state['feedback']

            else:
                st.write("Machine couldn't guess your number in 10 attempts. You win!")

        st.write(st.session_state.feedback)

if _name_ == "_main_":
    binary_search_game()