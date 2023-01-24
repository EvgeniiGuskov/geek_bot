# Geek Bot

___
This telegram bot helps to track movies, series and
similar content recommended by group members.

## Bot commands

___
`/register` — registers the user in the bot's database. <br/>
`/manage_mustwatch` — shows the content management interface,
which allows users to recommend content to any registered group
member. It is also possible to delete recommended content from this
group, view the list of recommendations and rate watched content.<br/>
`/mustwatch_rating` — shows the list of content sorted by an overall
rating of the group. The movie's rating is calculated based on the
scores given by group members.<br/>
You can invite the [bot](https://t.me/geek_keeper_bot) to any telegram
group for testing.

## Prepare to run a project

___

1. Set the telegram bot token at `.env` file:<br/>
   `TOKEN=your_telegram_bot_token`<br/>
2. Install
   [Docker](https://www.docker.com/)<br/>

3. Run `docker-compose up` command at repository
