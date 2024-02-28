<h1 align="center">🤖 KDU Scheduler Bot 🤖</h1>

<p align="center">All the schedule right in the pocket!</p>
<p align="center">Don't miss your next lesson ever again!</p>

## Usage

Follow these steps to set up and run the bot:

1. **Clone the Repository**
2. **Setup the Environment Variables**
    
    Create an environment variables file: ```.env```
   
    Open the newly created `.env` file and set the environment variables, listed below.

4. **Launch the Bot**
    
    Docker will help you run all the instances, neccassary for correct bot functioning.
    You can run your bot with the single following command:

    <i>Launch for the first time:</i>
    ```docker-compose up --build```

    <i>Default launch (after the project initial build):</i>
    ```docker-compose up```

    <i>Default launch (if you want to hide docker console logging):</i>
    ```docker-compose up -d```

## Environment Variables

<table>
<thead>
  <tr>
    <th>Variable</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>TOKEN</td>
    <td>String</td>
    <td>Bot Token (access yours from the BotFather telegram bot)</td>
  </tr>
  <tr>
    <td>MONGO_USER</td>
    <td>String</td>
    <td>Provide Mongo DB user</td>
  </tr>
  <tr>
    <td>MONGO_PASS</td>
    <td>String</td>
    <td>Provide Mongo DB password</td>
  </tr>
  <tr>
    <td>MONGO_DB</td>
    <td>String</td>
    <td>Provide Mongo DB database name</td>
  </tr>
  <tr>
    <td>MONGO_HOST</td>
    <td>String</td>
    <td>Provide Mongo DB host</td>
  </tr>
  <tr>
    <td>MONGO_PORT</td>
    <td>String</td>
    <td>Provide Mongo DB port</td>
  </tr>
  <tr>
    <td>CONTAINER_NAME</td>
    <td>String</td>
    <td>Provide Mongo DB docker container name</td>
  </tr>
  <tr>
    <td>DATABASE_URL</td>
    <td>String</td>
    <td>
      mongodb://${MONGO_USER}:${MONGO_PASS}@mongodb:${MONGO_PORT}/${MONGO_DB}?authSource=admin
    </td>
  </tr>
  </tr>
</tbody>
</table>

## Other

<p>KDU website: <a href="http://195.162.83.28/cgi-bin/timetable.cgi?n=700">click</a></p>
<p>Technical support email: <code>tel.admin@ukd.edu.ua</p></code>
