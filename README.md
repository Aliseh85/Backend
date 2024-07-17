InsaitBackend is a backend application that takes a question from the user via a JSON POST request, returns an answer using the OpenAI API, and stores it in a PostgreSQL database. The id is the primary key for our database. For database tables and migrations, we used Alembic. The application is operated within Docker and managed with Docker Compose.

#The application includes a test suite to ensure the functionality works as expected.
#1 test_ask: Tests the /ask endpoint for a valid question.
#2 test_ask_no_question: Tests the /ask endpoint when no question is provided.
#3 test_ask_openai_error: Tests the /ask endpoint when the OpenAI API returns an error.


###############################################################
#notes for me 
# check dockers and openai key and composer.
# we used alembic to make migration to our database
#ports 5000 and 5432

 
