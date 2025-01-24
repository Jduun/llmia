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

![Python](https://img.shields.io/badge/-Python-201c24?style=for-the-badge&logo=Python&logoColor=3474a8)
![Aiogram](https://img.shields.io/badge/-aiogram-201c24?style=for-the-badge&logo=aiogram&logoColor=3474a8)
![OpenAI API](https://img.shields.io/badge/-openai%20api-201c24?style=for-the-badge&logo=openai&logoColor=white)
![Groq API](https://img.shields.io/badge/-groq%20api-201c24?style=for-the-badge&logo=groq&logoColor=white)
![LiteLLM](https://img.shields.io/badge/-litellm-201c24?style=for-the-badge&logo=litellm&logoColor=white)


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
