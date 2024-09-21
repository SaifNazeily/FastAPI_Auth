# FastAPI User Authentication API with OTP Verification

This FastAPI project is a user authentication system with email OTP verification, connected to an ArangoDB database. It allows users to create accounts, receive an OTP via email, verify their account using the OTP, and manage user data (get, update, delete).

## Features

- **User Registration with OTP Verification**: Users register with a username, email, and password. An OTP is sent to their email for verification.
- **Email OTP**: Sends a one-time password to users' email addresses for account verification.
- **User Management**: Supports user creation, retrieval, update, and deletion.
- **ArangoDB Integration**: User data is stored in an ArangoDB collection.
- **Background Task**: OTP emails are sent in the background to ensure non-blocking API requests.

## Tech Stack

- **Backend**: FastAPI
- **Database**: ArangoDB
- **Email**: SMTP (Gmail)
- **Environment Variables**: Python-dotenv for securely managing environment variables

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- ArangoDB
- SMTP credentials for sending OTP emails

## Environment Variables

Create a `.env` file in the root of the project and add the following:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
