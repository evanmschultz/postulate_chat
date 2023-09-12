# Postulate Chat

## An AI chatbot using Langchain, ChromaDB, and OpenAI

![Demo GIF or Video](/assets/Screen%20Recording%202023-09-12%20at%2012.43.09%20PM.GIF)

## Table of Contents

-   [Postulate Chat](#postulate-chat)
    -   [An AI chatbot using Langchain, ChromaDB, and OpenAI](#an-ai-chatbot-using-langchain-chromadb-and-openai)
    -   [Table of Contents](#table-of-contents)
    -   [Overview](#overview)
    -   [Features](#features)
    -   [Tech Stack](#tech-stack)
    -   [Installation](#installation)
    -   [Usage](#usage)
    -   [To-Do](#to-do)
    -   [Contributing](#contributing)
    -   [License](#license)

## Overview

Postulate Chat is an AI chatbot application built using Flask. It employs Langchain for conversational logic, ChromaDB for document storage, and OpenAI for natural language processing. The application comes with login and registration features, protecting the chat routes. It's designed to evolve, with several additional features planned for future releases.

## Features

-   **SQLAlchemy ORM**: Automatically creates a MySQL database if it doesn't already exist.
-   **Websockets**: Installed but not currently in use. The plan is to implement real-time AI responses.
-   **Code Formatting**: Auto-formats and styles code blocks using Prism.js.
-   **ChromaDB Vector Store**: Currently global; future updates will support user-specific documents.
-   **Document Ingestion**: Currently supports URLs. Future updates will include PDF, CSV, and other formats.
-   **Login & Registration**: Built-in authentication and route protection.
-   **ConversationalRetrievalChain with Langchain**: Provides the AI chat functionality.

## Tech Stack

-   Flask
-   SQLAlchemy
-   MySQL
-   Websockets
-   Prism.js

## Installation

1. Clone the repository and navigate to the project directory.
    ```bash
    git clone https://github.com/evanmschultz/postulate_chat.git
    cd postulate-chat
    ```
1. Navigate to the project directory.
1. Install virtual environment using Pipenv:
    ```
    pipenv install
    ```
1. Export your MySQL environment variables before running the application. You can set them in the terminal as follows:

    ```bash
    export DB_USER=your_mysql_username
    export DB_PASSWORD=your_mysql_password
    export DB_HOST=localhost
    export OPENAI_API_KEY=your_openai_api_key
    ```

    - Replace `your_mysql_username`, `your_mysql_password`, and `host` with your MySQL username, password, and host location, respectively.
    - Defaults to `root`, `rootroot`, and `localhost`.

1. Export your OpenAI Api key in the terminal as follows:

    ```bash
    export OPENAI_API_KEY=your_openai_api_key
    ```

    - Replace `your_openai_api_key` with your OpenAI API key.

1. Activate the virtual environment:
    ```
    pipenv shell
    ```
1. Run the Flask app:
    ```
    python3 server.py
    ```

## Usage

1. Register for an account.
1. Log in to access the chat functionality.
1. Go to the settings to ingest documents into ChromaDB.

## To-Do

-   [ ] Implement Websockets for real-time AI responses.
-   [ ] Make ChromaDB Vector Store user-specific.
-   [ ] Add support for PDF, CSV, and other document formats.
-   [ ] Implement verbosity in ConversationalRetrievalChain.
-   [ ] Transition all routes to JSON for API-like functionality.
-   [ ] Modularize chat functionality into 'services'.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License
