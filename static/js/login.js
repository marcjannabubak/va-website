class Login {
    constructor(form, fields) {
        this.form = form;
        this.fields = fields;
        this.validateOnSubmit();
    }

    validateOnSubmit() {
        let self = this;
        this.form.addEventListener("submit", (e) => {
            e.preventDefault();
            var error = 0;
            self.fields.forEach((field) => {
                const input = document.querySelector(`#${field}`);
                if (self.validateFields(input) === false) {
                    error++;
                }
            });
            if (error === 0) {
                this.form.submit();
            }
        });
    }

    validateFields(field) {
        if (field.value.trim() === "") {
            this.setStatus(
                field,
                `${field.previousElementSibling.innerText} cannot be blank`,
                "error"
            );
            return false;
        } else {
            if (field.type === "password") {
                if (field.value.length < 6) {
                    this.setStatus(
                        field,
                        `${field.previousElementSibling.innerText} must be at least 6 characters`,
                        "error"
                    );
                    return false;
                } else {
                    this.setStatus(field, null, "success");
                    return true;
                }
            } else {
                this.setStatus(field, null, "success");
                return true;
            }
        }
    }

    setStatus(field, message, status) {
        const errorMessage = field.parentElement.querySelector(".error-message");
        if (status === "error") {
            errorMessage.innerText = message;
            errorMessage.style.display = "block";
            field.style.borderColor = "red";
        }
        if (status === "success") {
            errorMessage.innerText = "";
            errorMessage.style.display = "none";
            field.style.borderColor = "green";
        }
    }
}

document.getElementById("openLogin").addEventListener("click", () => {
    document.getElementById("loginOverlay").style.display = "flex";
});

window.onclick = function(event) {
    let overlay = document.getElementById("loginOverlay");
    if (event.target === overlay) {
        overlay.style.display = "none";
    }
}

const form = document.querySelector(".loginForm");
if (form) {
    const fields = ["username", "password"];
    const validator = new Login(form, fields);
}