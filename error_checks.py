# Check if the username is long enough

class UserCreationErrors():
    def 
    if len(new_user.username) < MIN_USERNAME_LENGTH:
        error_message = "Username too short."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)
    
    # Validate the email
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if not email_regex.match(new_user.email):
        error_message = "Invalid E-Mail."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)

    # Check if the username already exists
    existing_user = db.query(data_models.User).filter(data_models.User.username == new_user.username).first()
    if existing_user:
        error_message = "Username already taken."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)
    
    # Check if the email already exists
    existing_mail = db.query(data_models.User).filter(data_models.User.email == new_user.email).first()
    if existing_mail:
        error_message = "E-Mail already registered."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)