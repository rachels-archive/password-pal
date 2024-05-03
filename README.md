# Password Pal

#### Video Demo: https://youtu.be/eYUjr-SMG7Q

#### Description:

Password Pal is a secure password manager. With Password Pal, users can effortlessly generate and manage strong, unique passwords for their various accounts. The web app provides a user-friendly interface for creating, viewing, updating, and deleting login details. The following list are the key functions:

1.  **User Registration and Login:**

    - Users can securely create an account to access the password manager's features.
    - Secure login functionality is implemented, likely using hashed passwords for enhanced security.

2.  **Password Generator:**

    - Utilizes the `window.crypto.getRandomValues` function, leveraging the cryptographic functionality provided by the browser's Web Crypto API. This ensures that the generated passwords are truly random and secure.

3.  **Password Vault:**

    - Serves as a secure storage space for managing and organizing user credentials. Likely involves functionalities such as adding, viewing, updating, and deleting login details.

4.  **Form Validations:**

        -   Performs various checks on user input to ensure data integrity and security.
        -   Validates email formats during registration.
        -   Ensures required fields are filled.
        -   Verifies the strength of passwords entered, possibly using algorithms to assess complexity.

    <hr>

### Technology Stack:

1.  **Frontend Technologies:**

    - **HTML, CSS, JavaScript, jQuery:** These technologies are used to create the user interface and provide interactive features.

2.  **Backend Technologies:**

    - **Python, Flask, SQL:** Flask, a Python web framework, is used for the backend logic and handling server-side operations. SQL is employed for database operations.

3.  **Other Frameworks & Libraries:**

        -   **Bootstrap:** Enhances the frontend with a responsive and aesthetically pleasing design.
        -   **Font Awesome:** Used for scalable vector icons that can be customized easily.

    <hr>

### Enhancements:

1.  **Cryptographically Secure Password Generation:**

    - The use of `window.crypto.getRandomValues` ensures that passwords are generated using a cryptographically secure method, making it difficult for attackers to predict or manipulate the generated passwords.

2.  **Werkzeug's Security Module:**

    - The implementation of `check_password_hash` and `generate_password_hash` functions from Werkzeug's security module is a good security practice. It indicates the use of secure password hashing techniques for user account registration, protecting user credentials from unauthorized access.

3.  **AJAX Requests:**

    - The incorporation of AJAX requests enhances user experience by preventing unnecessary page refreshes. This leads to a more dynamic and seamless interaction with the application.

4.  **Clipboard API for Copying Passwords:**

    - Leveraging the `navigator.clipboard.writeText` function from the Clipboard API is a user-friendly enhancement. It allows users to copy generated passwords to the clipboard easily, adding convenience to the password management process.

    <hr>

### Challenges:

The main challenge revolved around putting into practice the knowledge gained throughout the course. Additionally, there was a challenge in integrating additional techniques such as AJAX requests to enhance the functionality of the application.
