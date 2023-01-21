# Geek Bot

___
This telegram bot helps to track movies, series and
similar content recommended by other users from the same
group. There is a rating system for each group. Group member
can rate the recommended content. The score given by the user will
be taken into account in the rating system of this group.

## Prepare to run a project

___
At first you need an installed
[PostgreSQL](https://www.postgresql.org/).<br/>
Then install required Python packages using `pip`:

```
$ pip install -r requirements.txt
```

After that you can establish a connection to your database
and telegram bot at `config` folder. <br/>
`database/alchemist.py` file for setting up a database
connection. <br/>
`telebot/telebot.py` file for setting up a telegram bot
token. <br/>
Then run the `main.py` at the root folder.

## Project structure

___

```
/config
|—/database
|—/telebot
/src
|—/controller
|—/model
|—/service
|—/view
```

> ### `config`
> Database and telegram bot configuration
>> #### `database`
>>Database connection settings
>> #### `telebot`
>> Telegram bot connection settings
> ### `src`
> Software logic components
>> #### `controller`
>> Handles user actions with telegram bot interface,
> > reacting appropriately by calling `service` and
> > `view` methods
>> #### `model`
>> Database structure and data access layer
>> #### `service`
>> Reading and modifying the database according to the
> > business logic
>> #### `view`
>> User interface layer