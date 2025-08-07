# NHL-Elo
Decision Support System for NHL games using the Elo rating system

To start the interface clone the repository and open main.py. Build the code in main.py to start the interface.

# Elo Rating System for NHL
This project uses the Elo rating system to track and predict team performance over time. Originally developed for ranking chess players, Elo has been adapted here to reflect team strength dynamically based on game outcomes.

Each team starts with a baseline rating. After each game:

The winner takes points from the loser.

Upsets yield larger rating changes.

Home-ice advantage can be optionally factored in.

Below is a sample visualization of Elo ratings over time for three NHL teams:

<img width="479" height="279" alt="image" src="https://github.com/user-attachments/assets/755fe0ab-2c49-4742-ab1b-ca21d9c85693" />

This chart illustrates how team ratings evolve through the season, reflecting win/loss trends and relative strength shifts.
