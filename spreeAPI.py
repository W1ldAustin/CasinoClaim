# Drake Hooks + WaterTrooper
# Casino Claim 2
# Spree API
# Version 4
# Notes:

import re
import os
import asyncio
import discord
from dotenv import load_dotenv
from seleniumbase import SB

# ───────────────────────────────────────────────────────────
# Config & Constants
# ───────────────────────────────────────────────────────────

load_dotenv()
SPREE_CRED = os.getenv("SPREE")  # format "username:password"

SITE_URL = "https://spree.com"
LOBBY_URL = "https://spree.com/slots"

LOGIN_BUTTON = ("//button[@data-cy='login-btn']")

EMAIL_INPUT_ID = ("login-form-email-input")
PASSWORD_INPUT_ID = ("login-form-password-input")
LOGIN_SUBMIT_XPATH = ("//button[@data-cy='login-form-submit-button']")

CLAIM_BUTTON_XPATH = ("//button[@data-cy='claim-bonus-button' and not(@disabled)]")

XPATH_COUNTDOWN = ("//button[@disabled and contains(normalize-space(.), ':')]")

# ───────────────────────────────────────────────────────────
# Spree Helpers
# ───────────────────────────────────────────────────────────

def _is_logged_in(driver) -> bool:
    """Detect if already logged in."""
    try:
        driver.find_element(By.CLASS_NAME, "profile-info")
        return True
    except NoSuchElementException:
        pass
    try:
        driver.find_element(By.ID, "CoinsBalance")
        return True
    except NoSuchElementException:
        return False

# ───────────────────────────────────────────────────────────
# Spree Flow
# ───────────────────────────────────────────────────────────

async def spree_uc(ctx, channel: discord.abc.Messageable):

    await channel.send("Launching **Spree** (UC)...")

    if ":" not in SPREE_CRED:
        await channel.send("❌ Missing `SPREE` as 'email:password' in your .env.")
        return

    username, password = SPREE_CRED.split(":", 1)

    try:
        with SB(uc=True, headed=True) as sb:

            # 1a) Navigate to site
            print("[Spree] Navigating to site...")
            try:
                sb.maximize()
                sb.wait(10)
                sb.uc_open_with_reconnect(SITE_URL, 4)
                sb.wait_for_ready_state_complete()
                print("[Spree] Site loaded.")
            except Exception:
                print("[Spree] Unable to load site.")

            # 1b) Login to site
            print("[Spree] Attempting to login...")
            try:
                sb.click(LOGIN_BUTTON)
                sb.wait(10)
            except Exception:
                print("[Spree] Unable to click login button.")

            try:
                sb.type(f"input[id='{EMAIL_INPUT_ID}']", username)
                sb.wait(5)
            except Exception:
                print("[Spree] Unable to enter email.")

            try:
                sb.type(f"input[id='{PASSWORD_INPUT_ID}']", password)
                sb.wait(5)
            except Exception:
                print("[Spree] Unable to enter password.")

            try:
                sb.uc_gui_click_captcha()
                sb.wait(5)
            except Exception:
                print("[Spree] Unable to click captcha")

            try:
                sb.click(LOGIN_SUBMIT_XPATH)
                print("[Spree] Submitted credentials.")
                sb.wait(10)
            except Exception:
                print("[Spree] Unable to click login submit button")

            # 1c) Refreash the page to deal with random popup
            print("[Spree] Refreashing the site...")
            try:
                sb.refresh()
                sb.wait(10)
            except Exception:
                print("[Spree] Unable to refresh site.")

            # 1d) Claim daily bonus
            print("[Spree] Attempting to claim daily bonus...")
            try:
                claim = sb.click(CLAIM_BUTTON_XPATH)
                await channel.send("Spree Daily Bonus Claimed!")
            except Exception:
                print("[Spree] Unable to claim daily bonus.")

            # 1f) If no claim, try to read the countdown
            print("[Spree] Checking for countdown...")
            try:
                countdown_btn = sb.find_element(XPATH_COUNTDOWN)
                raw       = countdown_btn.text.strip()                # e.g. "22 : 27 : 06"
                countdown = re.sub(r"Coins in\s+", "", raw)           # => "22:27:06"
                await channel.send(f"Next Spree Bonus Available in: {countdown}")
                return
            except:
                print("[Spree] Unable to read countdown.")
                screenshot = "spree_countdown_error.png"
                sb.driver.save_screenshot(screenshot)
                await channel.send("[Spree] Unable to read countdown.",file=discord.File(screenshot))
                os.remove(screenshot)

    except Exception as e:
        print(f"[Spree][ERROR] Exception during automation: {e}")     