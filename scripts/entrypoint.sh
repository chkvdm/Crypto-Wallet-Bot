#!/bin/bash

# bash script for create Crypto_Wallet_bot.
# V2_initial_schema include ON DELETE CASCADE mode for balance and transaction table!
# V3_initial_schema include new transaction type. Use V3!!

dropdb -f CryptoBotDB

createdb -h localhost -p 5432 -U postgres CryptoBotDB
psql -d CryptoBotDB -f /Users/vadim/Documents/Crypto_Wallet_Bot/migrations/V3_initial_schema.sql

#python3 /Users/vadim/Documents/BotProject/App_Code/BotCode.py