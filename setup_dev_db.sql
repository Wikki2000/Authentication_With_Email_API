-- create database
CREATE DATABASE api_db;

-- Create user
CREATE ROLE api WITH LOGIN PASSWORD 'test_pwd';

-- Grant priviledge to the created role
GRANT ALL PRIVILEGES ON DATABASE api_db TO api;
