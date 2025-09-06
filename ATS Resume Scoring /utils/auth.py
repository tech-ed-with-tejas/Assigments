import os
import asyncio
import logging
from typing import Optional, Tuple

import streamlit as st
from dotenv import load_dotenv
from httpx_oauth.clients.google import GoogleOAuth2

# -----------------------------------------------------------------------------
# 1) Load Environment Variables
# -----------------------------------------------------------------------------
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
APP_ENV = os.getenv("APP_ENV", "local")  # local | production

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise EnvironmentError(
        "Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in environment."
    )

# -----------------------------------------------------------------------------
# 2) Configuration
# -----------------------------------------------------------------------------
SCOPES = [ "email", "profile"]
google_oauth_client = GoogleOAuth2(
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, scopes=SCOPES
)

REDIRECT_URI = (
    os.getenv("REDIRECT_URI")
    or ("https://your-production-domain.com/callback" if APP_ENV == "production" else "http://localhost:8501/")
)

client: GoogleOAuth2 = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)






def logout(email):
    
    del st.session_state['token']

    st.experimental_rerun()

    
    
async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile", "email"])
    # st.text(authorization_url)
    return authorization_url

async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    token = await client.get_access_token(code, redirect_uri)
    
    return token


async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email




    


def get_login_str():
    # ksks
    # client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    authorization_url = asyncio.run(
        get_authorization_url(client, REDIRECT_URI))
    # login_ui(authorization_url)
    return authorization_url


def get_token(code):



    
    token = asyncio.run(get_access_token(
            client, REDIRECT_URI, code))
    
                

    return token
   

def get_username(token):
    user_id, user_email = asyncio.run(
                            get_email(client, token['access_token']))
    return user_id, user_email


# # -----------------------------------------------------------------------------
# # 3) Async OAuth Functions
# # -----------------------------------------------------------------------------
# async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str) -> str:
#     """Get the Google OAuth2 authorization URL."""
#     return await client.get_authorization_url(
#         redirect_uri,
#         scope=SCOPES,
#         extras_params={"access_type": "offline", "prompt": "consent"}  # for refresh tokens
#     )

# async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str) -> Optional[dict]:
#     """Exchange authorization code for an access token."""
#     try:
#         return await client.get_access_token(code, redirect_uri)
#     except Exception as e:
#         logging.error(f"Error fetching access token: {e}")
#         return None


# async def get_email(client: GoogleOAuth2, token: str):
#     user_id, user_email = await client.get_id_email(token)
#     return user_id, user_email
    
# async def refresh_tokens(refresh_token: str):
#     # httpx-oauth provides refresh_token() on the base OAuth2 client
#     new_token = await google_oauth_client.refresh_token(refresh_token)
#     # Google may not always return a new refresh_token; keep existing if missing
#     if "refresh_token" not in new_token and refresh_token:
#         new_token["refresh_token"] = refresh_token
#     return new_token
# # -----------------------------------------------------------------------------
# # 4) Streamlit-Compatible Wrappers
# # -----------------------------------------------------------------------------
# def get_login_url() -> str:
#     """Generate the Google login URL (synchronous wrapper)."""
#     return asyncio.run(get_authorization_url(google_oauth_client, REDIRECT_URI))

# def exchange_code_for_token(code: str) -> Optional[dict]:
#     """Exchange the code for an access token (synchronous wrapper)."""
#     return asyncio.run(get_access_token(google_oauth_client, REDIRECT_URI, code))

# def get_username(token):
#     user_id, user_email = asyncio.run(
#                             get_email(google_oauth_client, token['access_token']))
#     return user_id, user_email
