const usernameField = document.querySelector("#usernameField");
const InvalidFlied = document.querySelector(".invalid-feedback");
const emailInvalidField = document.querySelector(".email-invalid-feedback");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const checkSuccess = document.querySelector(".check-success");
const passwordShowToggle = document.querySelector(".show-password");
const submitButton = document.querySelector(".submit-Button");
const tbody = document.querySelector(".table-output");

tbody.style.display = none;

passwordShowToggle.style.cursor = "pointer";
// Password hide and show function
const passwordShowHandler = () => {
  if (passwordShowToggle.textContent === "Show") {
    passwordShowToggle.textContent = "Hide";
    passwordField.setAttribute("type", "text");
  } else {
    passwordShowToggle.textContent = "Show";
    passwordField.setAttribute("type", "password");
  }
};

passwordShowToggle.addEventListener("click", passwordShowHandler);

// Username Email call back
usernameField.addEventListener("keyup", (e) => {
  let usernameVal = e.target.value;
  checkSuccess.style.display = "block";

  checkSuccess.textContent = `Checking ${usernameVal}`;

  usernameField.classList.remove("is-invalid");
  usernameField.classList.add("is-valid");
  InvalidFlied.style.display = "none";

  if (usernameVal.length <= 0) {
    usernameField.classList.remove("is-valid");
    checkSuccess.style.display = "none";
  }
  if (usernameVal.length > 0) {
    console.log("111", 111);
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        checkSuccess.style.display = "none";

        if (data.username_error) {
          submitButton.disabled = true;
          usernameField.classList.add("is-invalid");
          InvalidFlied.style.display = "block";
          InvalidFlied.innerHTML = `<p>${data.username_error}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});

// Email Api call back
emailField.addEventListener("keyup", (e) => {
  let emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailField.classList.add("is-valid");
  emailInvalidField.style.display = "none";

  if (emailVal.length <= 0) {
    emailField.classList.remove("is-valid");
  }

  if (emailVal.length > 0) {
    console.log("111", 111);
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);

        if (data.email_error) {
          submitButton.disabled = true;
          emailField.classList.add("is-invalid");
          emailInvalidField.style.display = "block";
          emailInvalidField.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});
