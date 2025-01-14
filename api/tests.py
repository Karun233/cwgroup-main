# your_app/tests/test_e2e.py

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from api.tests_setup import SeleniumTestCase  # Adjust import based on your project structure
from django.contrib.auth import get_user_model

class E2ETests(SeleniumTestCase):
    
    def fill_input(self, by, identifier, value):
        """Utility method to fill an input field."""
        element = self.driver.find_element(by, identifier)
        element.clear()
        element.send_keys(value)
    
    """def test_signup(self):
        
        self.driver.get(f'http://127.0.0.1:8000/register/')
        
        # Fill out the signup form fields
        self.fill_input(By.ID, "id_username", "TestUser")
        self.fill_input(By.ID, "id_name", "Test User Name")
        self.fill_input(By.ID, "id_email", "Test@gmail.com")
        self.fill_input(By.ID, "id_date_of_birth", "23/09/2003")
        self.fill_input(By.ID, "id_password1", "SecurePass123!")
        self.fill_input(By.ID, "id_password2", "SecurePass123!")  
        # Fill additional fields as necessary
        
        signup_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        signup_button.click()
        
        # Wait for redirect/confirmation (adjust URL/text as needed)
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login/")  # Example URL after signup
        )
        self.assertIn("/login/", self.driver.current_url)"""
    
    """def test_login(self):
        
        # Create a test user programmatically
        
        User = get_user_model()
        # Check if user already exists to avoid duplicate creation errors
        if not User.objects.filter(username="jeff").exists():
            User.objects.create_user(username="jeff", password="karun2003")
        
        self.driver.get(f'{self.live_server_url}/login/')
        
        self.fill_input(By.ID, "id_username", "jeff")
        self.fill_input(By.ID, "id_password", "karun2003")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        
        # Wait for redirection after login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard/")
        )
        self.assertIn("/dashboard/", self.driver.current_url)"""
    
    def test_edit_profile(self):
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username="jeff").exists():
            User.objects.create_user(username="jeff", password="karun2003")

        # --- Begin Login Process ---
        self.driver.get(f'http://127.0.0.1:8000/login/')
        
        self.fill_input(By.ID, "id_username", "jeff")
        self.fill_input(By.ID, "id_password", "karun2003")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        
        # Optional: Wait for redirection after login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")  # Adjust based on your redirect URL
        )
        
        # Instead of directly navigating to profile, click the navbar link
        profile_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/profile']"))
        )
        profile_link.click()
        
        # Wait until profile page loads, using presence of known element
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        
        # Fill in profile fields with new data
        self.fill_input(By.ID, "name", "Selenium Test User")
        self.fill_input(By.ID, "email", "changedemail@example.com")
        # ... fill other fields as needed
        
        save_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        save_button.click()
        
        # Wait for the alert indicating profile update success
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        
        # Switch to the alert, check its text, and accept it
        alert = self.driver.switch_to.alert
        self.assertIn("Profile updated successfully", alert.text)
        alert.accept()



    """def test_filter_users_by_age(self): 

        User = get_user_model()
        if not User.objects.filter(username="jeff").exists():
            User.objects.create_user(username="jeff", password="karun2003")

        # --- Begin Login Process ---
        self.driver.get(f'http://127.0.0.1:8000/login/')
        
        self.fill_input(By.ID, "id_username", "jeff")
        self.fill_input(By.ID, "id_password", "karun2003")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        
        
        profile_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/hobbies']"))
        )
        profile_link.click()
        
        # Wait 3 seconds visually before applying filters
        time.sleep(3)
        
            # Fill in the age filter fields using placeholder attributes to locate them
        self.fill_input(By.CSS_SELECTOR, "input[placeholder='No minimum']", "20")
        self.fill_input(By.CSS_SELECTOR, "input[placeholder='No maximum']", "30")
        
        
        
        # Wait for results to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-group-item"))
        )
        
        # Retrieve results
        results = self.driver.find_elements(By.CSS_SELECTOR, ".list-group-item")
        
        # Check if there is at least one result

        for user in results:
            try:
                # Find the span element that holds the age text
                age_span = user.find_element(By.CSS_SELECTOR, "span")
                age_text = age_span.text  # e.g., "(Age: 1)"
                
                # Use regex to extract numeric age
                match = re.search(r"Age:\s*(\d+)", age_text)
                self.assertIsNotNone(match, f"Couldn't parse age from text: {age_text}")
                age = int(match.group(1))
                
                self.assertTrue(20 <= age <= 30, f"User age {age} not in range")
            except Exception as e:
                self.fail(f"Error processing user age: {e}")"""

    
    """def test_send_friend_request(self):
        # --- Begin Login Process ---
        self.driver.get(f'http://127.0.0.1:8000/login/')
        
        self.fill_input(By.ID, "id_username", "TestUser")
        self.fill_input(By.ID, "id_password", "SecurePass123!")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        
        # Optionally wait for redirection after login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")
        )
        
        # --- Begin Friend Request Process ---
        # Wait for the search bar to be present on the page
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control"))
        )
        
        # Fill in the search bar with the target user's username
        self.fill_input(By.CSS_SELECTOR, "input.form-control", "john23")
        
        # Click the search button
        search_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.mt-2")
        search_button.click()
        
        # Wait for search results to load; assume list items appear after search
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li"))
        )
        
        target_user_name = "john23"  # Adjust to the target user's name
        list_items = self.driver.find_elements(By.CSS_SELECTOR, "li")
        found = False
        
        for item in list_items:
            # Check if the list item contains the target username text
            if target_user_name in item.text:
                # Find and click the send friend request button within this list item
                send_button = item.find_element(By.CSS_SELECTOR, "button.btn.btn-success.btn-sm")
                send_button.click()
                found = True
                break
                
        # Assert that the target user was found in the list
        self.assertTrue(found, f"User {target_user_name} not found in search results.")
        
        # Wait for confirmation/alert that the friend request was sent
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertIn("Friend request sent!", alert.text)
        alert.accept()"""
        
    """def test_accept_friend_request(self):
        # Begin Login Process as john23
        self.driver.get(f'http://127.0.0.1:8000/login/')
        self.fill_input(By.ID, "id_username", "john23")
        self.fill_input(By.ID, "id_password", "Smith2003")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        
        # Wait for redirection after login
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard")
        )
        
        # Wait for the friend requests to load on the dashboard or relevant page
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li"))
        )
        
        # Find list items and search for the friend request from "jeff"
        target_requester = "TestUser"
        list_items = self.driver.find_elements(By.CSS_SELECTOR, "li")
        found = False
        for item in list_items:
            if target_requester in item.text:
                # Find and click the accept friend request button within this list item
                accept_button = item.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-sm")
                accept_button.click()
                found = True
                break
        
        # Assert that the friend request was found and the accept button was clicked
        self.assertTrue(found, f"Friend request from {target_requester} not found.")
        
        # Wait for confirmation alert
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertIn("Friend request accepted!", alert.text)
        alert.accept()"""
