const usernameField = document.querySelector("#usernameField");
const InvalidFlied = document.querySelector(".invalid-feedback");

usernameField.addEventListener("keyup", (e) => {
  let usernameVal = e.target.value;

  usernameField.classList.remove("is-invalid");
  usernameField.classList.add("is-valid");
  InvalidFlied.style.display = "none";

  if (usernameVal.length <= 0) {
    usernameField.classList.remove("is-valid");
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

        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          InvalidFlied.style.display = "block";
          InvalidFlied.innerHTML = `<p>${data.username_error}</p>`;
        }
      });
  }
});
