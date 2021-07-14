
# запуск тестов в консоли
python -m unittest

# coverage
coverage run --source=bot,handers,settings -m unittest
coverage report -m

# сменить пользователя на postgres
psql -h localhost -U postgres

# create PostgreSQL database
psql -c "create database vk_chat_bot"
psql -d vk_chat_bot