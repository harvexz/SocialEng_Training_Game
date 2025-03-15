# Cybersecurity Awareness Game

A narrative-driven educational game designed to teach cybersecurity awareness through interactive scenarios that simulate real-world social engineering attacks.

## Overview

This game presents players with realistic social engineering and cybersecurity scenarios where they must make decisions that either protect or compromise sensitive information and systems. The game serves as a gamified training tool for recognizing and responding to social engineering attacks.

## How to Run

- Run the compiled version of the game (to be uploaded)
- Alternatively, run using Ren'Py launcher by opening the project directory

## File Structure

```
Experiment/
├── game/
│   ├── script.rpy             # Main game script with level implementations
│   ├── screens.rpy            # UI screens and interface definitions
│   ├── persistent_data.rpy    # Persistent data handling and achievements
│   ├── gui/                   # GUI elements and styling
│   │   └── document_assets/   # Assets for documents, ID cards, etc.
│   ├── images/                # Game images and character sprites
│   └── audio/                 # Sound effects and music
└── README.md                  # This file
```

## Game Features

- **Narrative-Driven Learning**: Learn through engaging storylines rather than traditional training
- **Decision-Based Gameplay**: Make choices that affect the outcome and demonstrate security awareness
- **Scoring System**: Earn points for correct security decisions and lose points for security mistakes
- **Ranking System**: Progress through ranks (Novice, Intermediate, Expert, Elite) based on your score
- **Achievements**: Unlock achievements for demonstrating specific security awareness skills
- **Statistics Tracking**: View your progress, completed levels, and achievements in the Stats screen
- **Data Collection**: Anonymous gameplay data is collected for research purposes

## Level Breakdown

### Tutorial
- Introduction to game mechanics and basic cybersecurity concepts
- Learn how to navigate the interface and make decisions

### Level 1: The Networker
- **Focus**: Physical security and in-person social engineering
- **Scenario**: An unknown person claiming to be IT staff requests access to the server room
- **Skills Tested**: Verifying identity, following security protocols, recognizing suspicious behavior
- **Key Decisions**: Whether to grant access, request identification, or verify with management

### Level 2: Email Security
- **Focus**: Phishing detection and email security
- **Scenario**: Sort through various emails to identify legitimate vs. phishing attempts
- **Skills Tested**: Recognizing phishing indicators, verifying sender authenticity, identifying suspicious links
- **Mechanics**: Email interface with options to mark messages as safe or phishing

### Level 3: Infiltration - The Insider Threat
- **Focus**: Insider threats and multi-channel verification
- **Scenario**: Three challenges involving phone calls, chat messages, and document verification
- **Skills Tested**: Verifying identity across different communication channels, recognizing manipulation tactics
- **Challenges**:
  - Phone Call: Respond to a suspicious call requesting sensitive information
  - Chat: Navigate a conversation with someone claiming to need access to sensitive documents
  - Document: Verify the legitimacy of an invoice before processing payment

### Level 4: Physical Security - Tailgating
- **Focus**: Physical access control and tailgating prevention
- **Scenario**: Encounter with someone attempting to enter the building without scanning their ID
- **Skills Tested**: Enforcing security protocols, reporting suspicious behavior, attention to detail
- **Key Features**: Flashback mechanics, email reporting system, memory/observation challenges

## Important Functions

- `save_progress()`: Saves game progress, updates rank, and logs data
- `update_rank()`: Updates player rank based on score
- `check_achievements()`: Checks and awards achievements based on game progress
- `log_data()`: Exports gameplay data to CSV for research analysis
- `check_email()`: Handles email verification in Level 2

## Data Collection

The game collects anonymous gameplay data for research purposes, including:
- Current level
- Score
- Level completion status
- Replay status
- Current rank

This data is stored in a CSV file (`player_data.csv`) and is used to analyze player performance and improve the game's educational effectiveness.

## Project Aim

This project aims to create an engaging, gamified training tool for cybersecurity awareness with a focus on social engineering attacks. By presenting realistic scenarios in an interactive narrative format, the game helps players:

- Recognize common social engineering tactics
- Practice appropriate responses to security threats
- Develop security-conscious habits that transfer to real-world situations
- Learn in an engaging environment that promotes retention better than traditional training methods

## Future Development

- Additional levels focusing on other security domains
- More detailed feedback and learning resources
- Expanded achievement system
- Customizable difficulty settings
- Integration with organizational training programs

## Credits

Created as part of a dissertation project on gamified cybersecurity awareness training.
