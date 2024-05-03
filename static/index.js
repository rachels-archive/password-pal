function generatePassword() {
    const lower = "abcdefghijklmnopqrstuvwxyz";
    const upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const numbers = "0123456789";
    const special = "!@#$%^&*()";

    var chars = "";

    var hasLower = document.getElementById("hasLower").checked;
    var hasUpper = document.getElementById("hasUpper").checked;
    var hasNumbers = document.getElementById("hasNumbers").checked;
    var hasSpecial = document.getElementById("hasSpecial").checked;

    chars += hasLower ? lower : "";
    chars += hasUpper ? upper : "";
    chars += hasNumbers ? numbers : "";
    chars += hasSpecial ? special : "";

    let password = "";

    if (!chars) {
      password = ""
    } else {
      var length = document.getElementById("passwordLength").value;
      const array = new Uint32Array(length);
      window.crypto.getRandomValues(array);

      for (let i = 0; i < length; i++) {
          password += chars[array[i] % chars.length];
      }
    }
    document.getElementById("password").value = password
}


$(document).on('submit','#deleteForm',function(e){
  var credentialId = document.getElementById("credentialId").value;
  var $form = $(this);
  e.preventDefault();
  $.ajax({
      type: "POST",
      url: "/deleteCredential",
      data: { credentialId: credentialId },
      success: function(response) {
          $form.closest('tr').remove();
          alert("Credential deleted successfully");
      },
      error: function(error) {
          // Handle error, e.g., show error message
          alert("Error deleting credential:", error);

      }
  });
});


function validatePasswordLength() {
  var passwordLengthInput = document.getElementById("passwordLength");

  var passwordLength = parseInt(passwordLengthInput.value, 10);

  if (passwordLength < 8) {
      alert("Minimum password length is 8 characters");
      passwordLengthInput.value = 8;
  }

  if (passwordLength > 20) {
    alert("Maximum password length is 20 characters");
    passwordLengthInput.value = 20;
  }
}

$(document).on('submit','#generateForm',function(e){
  e.preventDefault();

  // Get the password value
  var password = $("#password").val();

  // Password length validation (adjust the length as needed)
  if (password.length < 8) {
      alert("Password should be at least 8 characters long.");
      return; // Stop the form submission
  }


  $.ajax({
      type: "POST",
      url: "/generate",
      data: $("#generateForm").serialize(),
      success: function(response) {
          alert("New credentials saved successfully");
      },
      error: function(error) {
          // Handle error, e.g., show error message
          alert("Error saving credentials:", error.responseText);
      }
  });
});


function copyPassword(toCopy) {
    try {
      navigator.clipboard.writeText(toCopy);
      alert('Content copied to clipboard');
    } catch (err) {
      console.error('Failed to copy: ', err);
    }

}


function showEditForm(title, name, password) {
  var titleInput = document.getElementById("titleInput");
  var usernameInput = document.getElementById("usernameInput");
  var passwordInput = document.getElementById("passwordInput");

  titleInput.value = title
  usernameInput.value = name
  passwordInput.value = password
}