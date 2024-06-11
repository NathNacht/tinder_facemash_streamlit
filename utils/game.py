import streamlit as st
import random

class Game:
    def __init__(self, db):
        """Initialize the Game class with a database instance."""
        self.db = db

    def display_play_page(self):
        """Display the game play page."""
        player_name = st.text_input("Enter your name to start playing:", "")
        if player_name:
            if 'player_id' not in st.session_state:
                st.session_state.player_id = self.db.add_player(player_name)
            self.start_game()

    def start_game(self):
        """Start the game and handle game logic."""
        if 'level' not in st.session_state:
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.timer = 30
        
        real_image, genai_image = self.db.get_random_images()
        images = [(real_image, 1), (genai_image, 0)]
        random.shuffle(images)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select Left Image", key="left"):
                self.check_selection(images[0][1] == 1)
            st.image(images[0][0][4], use_column_width=True)
        with col2:
            if st.button("Select Right Image", key="right"):
                self.check_selection(images[1][1] == 1)
            st.image(images[1][0][4], use_column_width=True)

    def check_selection(self, is_real_image):
        """Check the user's selection and update the game state."""
        if is_real_image:
            st.session_state.score += 1
            st.session_state.level += 1
            st.session_state.timer *= 0.9
            st.write(f"Correct! Your current score: {st.session_state.score}")
            self.start_game()
        else:
            st.write("Wrong! Game Over!")
            st.write(f"Your final score: {st.session_state.score}")
            st.session_state.page = 'home'