<h2>Conductor</h2>

<h4>Реализованная функциональность</h4>
<ul>
    <li>Авторизация(Cookie Token, Header Token)</li>
    <li>Аутентификация/Регистрация</li>
    <li>Личный кабинет спортсмена</li>
    <li>Возможность проходить задачи в roadmap</li>
    <li>Возможность сохранять прогресс адаптации</li>
    <li>Сеть(контакты)</li>
    <li>Панель управления для HR/руководителя</li>
</ul>


<h4>Особенность проекта в следующем:</h4>
<ul>
    <li>Гибкость системы ролей</li>
    <li>Полная адаптивность сайта/приложения</li>
    <li>Плавная смена темы в ночную/дневную</li>  
</ul>


<h4>Основной стек технологий:</h4>
<ul>
    <li>python3.11, FastAPI, mongodb, pymongo, nginx, ubuntu22, certbot, pydantic</li>
	<li>MongoDB</li>
	<li>HTML/CSS/JS</li>
 </ul>


<h4>Демо</h4>
<p>Демо сервиса доступно по адресу: https://divarteam.ru/</p>
<p>Реквизиты тестового пользователя</p>
<p>Руководитель: <b>Ivan</b> - <b>1</b></p>
<p>HR: <b>Ivan</b> - <b>1</b></p>
<p>Сотрудник: <b>Ivan</b> - <b>1</b></p>


СРЕДА ЗАПУСКА
------------
1) Ubuntu 22
2) ASGI(uvicorn)
3) MongoDB,
4) Nginx
5) Python3.11


УСТАНОВКА
------------
###
Настройка системы
~~~
sudo apt update
sudo apt upgrade
apt autoremove
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11
~~~
Создаём пользователя
~~~
adduser conductor
usermod -aG sudo conductor
su - conductor
~~~

Установка poetry
~~~
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/home/conductor/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="/home/conductor/.local/bin:$PATH"' >> ~/.profile
poetry config virtualenvs.in-project true
exec "$SHELL"
poetry --version
~~~

Установка репозитория
~~~
git clone git@github.com:papergoldbag/conductor.git
cd conductor
poetry env use python3.11
poetry install
~~~

Нужно создать файл .env и поместить туда
~~~
mongo_user = "..."
mongo_password = "..."
mongo_host = "..."
mongo_port = ...
mongo_auth_db = "..."
mongo_db_name = "..."

mailru_login = '...'
mailru_password = '.'

tg_bot_token = '...'
tg_admin_ids = [...]
~~~


### База данных
Установка
~~~
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl daemon-reload
sudo systemctl enable mongod
sudo systemctl restart mongod
~~~

Создание доступа
~~~
mongosh
use admin
db.createUser({
  user: "admin",
  pwd: passwordPrompt(),
  roles:[{role: "userAdminAnyDatabase" , db:"admin"}]
})
db.createUser(
{
  user: "root",
  pwd: passwordPrompt(),
  roles: ["root"]
})
db.createUser(
{
  user: "conductor",
  pwd: passwordPrompt(),
  roles: [
  {role: "readWrite", db: "production"}
  ]
})
~~~


### Сайт как сервис
Нужно скопировать файл conductor.service в /etc/systemd/system/conductor.service
~~~
sudo cp ./conductor.service /etc/systemd/system/conductor.service
sudo systemctl start conductor
~~~


### Бот как сервис
Нужно скопировать файл conductor_bot.service в /etc/systemd/system/conductor_bot.service
~~~
sudo cp ./conductor_bot.service /etc/systemd/system/conductor_bot.service
sudo systemctl start conductor_bot
~~~


### Настройка Proxy Nginx
Установка
~~~
sudo apt install nginx
~~~
Конфигурация
~~~
rm -rf /etc/nginx/sites-enabled/default
sudo cp ./conductor.nginx /etc/nginx/sites-enabled/conductor
~~~
Перезапуск
~~~
sudo systemctl restart nginx
~~~


### Запуск системы через Docker
Систему также возможно запустить через Docker


### РАЗРАБОТЧИКИ
<h4>Илья Хакимов - Frontend https://t.me/ilyakhakimov03 </h4>
<h4>Денис Шайхльбарин - Android https://t.me/BrightOS </h4>
<h4>Арсен Сабирзянов - Backend https://t.me/arpakit </h4>
<h4>Иван Ермолов - Data-Scientist https://t.me/ivan_20190721 </h4>
<h4>Рустам Афанасьев - Project manager, Analytic https://t.me/rcr_tg </h4>


front: https://github.com/PirateThunder/atoll_front.git
mobile: https://github.com/BrightOS/AtollMobile.git