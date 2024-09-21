from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from arangodb_config import ArangoDB
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import bcrypt

app = FastAPI()
db = ArangoDB()
load_dotenv()

email_host_user = os.getenv("EMAIL_HOST_USER")
email_host_password = os.getenv("EMAIL_HOST_PASSWORD")

# Pydantic model for user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Pydantic model for OTP verification
class UserOTP(BaseModel):
    otp: str

# Email sending function
def send_otp_email(to_email: str, otp: str):
    from_email = email_host_user
    password = email_host_password
    
    # Email content
    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}"

    # Create MIME message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"OTP sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Create a user (accepts JSON body)
@app.post("/users/")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    if db.get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Generate a random OTP
    otp = str(random.randint(100000, 999999))

    # Hash the user's password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Store user data in the database
    db.create_user({
        "username": user.username,
        "email": user.email,
        "password": hashed_password,  # Store hashed password
        "otp": otp,
        "verified": False
    })

    # Send OTP email in the background
    background_tasks.add_task(send_otp_email, user.email, otp)

    return {"message": "User created successfully. OTP has been sent to your email."}

# Get a user by username
@app.get("/users/{username}")
async def get_user(username: str):
    user = db.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user with OTP verification
@app.put("/users/{username}")
async def update_user(username: str, user_otp: UserOTP):
    user = db.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user["otp"] == user_otp.otp:
        db.update_user_verified(username)
        return {"message": "User verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")

# Delete a user by username
@app.delete("/users/{username}")
async def delete_user(username: str):
    user = db.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete_user(username)
    return {"message": f"User '{username}' has been deleted."}
