# bot
export TOKEN=yourtoken
export USE_REDIS=false
export DEBUG=false

# client
export API_ID=api_id
export API_HASH=api_hash
export DEBUG=false

# telegram_ids
export BOT_ID=bot_id
export BOSS_ID=your personal id from telegram
export CLIENT_ID=id your client for telethon
export GROUP_ERROR_ID=group id to send errors, you should add the bot to the group
export GROUP_CACHE_ID=group id for cache files

# db
export USER=postgres
export PASSWORD=postgres
export DATABASE=defaultdb
export HOST=localhost
export PORT=5252
export DB_URI="postgres://${USER}:${HOST}:${PORT}/${DATABASE}?sslmode=require"
