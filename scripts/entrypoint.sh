#!/bin/bash

dropdb -f CryptoBotDB

createdb -h localhost -p 5432 -U postgres CryptoBotDB
psql -d CryptoBotDB -f /Users/vadim/Documents/BotProject/.:migrations/V1_initial_schema.sql

#python3 /Users/vadim/Documents/BotProject/App_Code/BotCode.py