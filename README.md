# Geek Bot

___
This telegram bot helps to track movies, series and
similar content recommended by group's members.

## Bot commands

___
`/register` — registers user at bot's database. <br/>
`/manage_mustwatch` — shows the content management
interface which allows user to recommend content to any registered
group member. It is also possible to delete recommended content from
this group, view the list of recommendations and rate watched
content.
`/mustwatch_rating` — shows the list of content sorted
by overall rating of the group. The rating of the movie is calculated
based on the scores given by group's users.

## Prepare to run a project

___

1. Set a telegram bot token at `.env` file:
   `TOKEN=your_telegram_bot_token`<br/>
2. Install
   [Docker](https://www.docker.com/).<br/>

3. Run `docker-compose up` command at repository

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