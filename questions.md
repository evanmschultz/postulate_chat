# Questions on Structure, etc.

-   [ ] Langchain Structure

    -   Currently, I have the models handling the connection to the database, but they also are handling the creation of the chat chain. I originally thought of having a `chat_services` module to handle the chain, but had trouble connecting it in the dark so to speak, so I moved to a more top down approach to just get it to work, now I need to completely refactor my code, again. lol
    -   I have the file ingestion services broken up into their separate parts, yet, some of the things are strictly functions, but are built as classes, should I refactor those to just be functions, if so, how should I do it?

-   [ ] Vector Database Handling

    -   The vector database runs in memory. I want a separate vector database for each user, ie. each user chats only with their files, and doesn't have access to anyone elses. Currently the vector database is created at ingestion. I want it to be created when a user is created, and then added to at ingestion, and pulled from at chat. This also creates text files in case someone wants to view them later, yet, it is more for testing purposes and I don't want to keep that functionality in the final product, as the text files can be created from the vector database.

-   [ ] Chat services

    -   As mentioned above, the chat chain is handled by the chat model (the connection to the database). I think it would be better to have a separate chat services module to handle the chat chain, and then have the chat model handle the connection to the database. This would allow for more modularity,extensibility, and stability whenever langchain introduces a breaking chain. At least that is what I am thinking.

-   [ ] User Model

    -   Currently there is a separate module for the user validation. The way I had it set up made adding the update and delete CRUD functionality difficult and confusing. How should I update the current structure to make it modular, extensible, and stable?

-   [ ] Chat Memory and History

    -   Currently, I am using langchain's buffer memory class (it holds the history in memory). Eventually, I want to have the memory stored in the vector database with metadata denoting it as memory so a chain can pull only the relevant history when needed. How should I go about updating the current structure with that in mind?

-   [ ] Routes

    -   Currently my routes feel confused, partially separated by the page they are displayed on or the module they affect. Please take a look at them and see if you have suggestions on how to handle the routing?

-   [ ] Database

    -   Using SQLAlchemy ORM to handle the creation and management of the database. In production, where would the database live in my current setup? Should I create a completely separate service outside of the `flask_app` to store the database? If so, how? If not, how should I handle the database in production?
