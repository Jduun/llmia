# LLMia

## Table of Contents
- [About](#about)
- [Features](#features)
- [Techonologies](#technologies)
- [Installation and Setup](#installation-and-setup)
- [License](#license)

## About
Telegram bot for text RPG game with LLM and Text2Image.

## Features
- The bot based on LLM acts as a Dungeon Master, dynamically crafting a rich and engaging story where players’ decisions drive the narrative.  
- Bot generates images using Text2Image models to visually represent the current game situation and enhance immersion.  
- Bot includes inventory management and a health system, allowing players to use and manage items.  


## Technologies
Python, Aiogram, OpenAI API, GroqAPI, LiteLLM

## Installation and Setup
1. Clone the repository:
    ```
    git clone https://github.com/Jduun/llmia.git
    ```

2. Navigate to the project folder:
    ```
    cd llmia
    ```

3. Create file with environment variables:
    ```
    cp .env.example .env
    ```
    Change the values of the environment variables to your own.

4. Build project:
    ```
    docker compose up --build
    ```

## License
This project is licensed under the terms of the [MIT License](./LICENSE).
