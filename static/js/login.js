const themes = [
    {
        background: "#1A1A2E",
        color: "#FFFFFF",
        primaryColor: "#0F3460"
    },
    {
        background: "#461220",
        color: "#FFFFFF",
        primaryColor: "#E94560"
    },
    {
        background: "#192A51",
        color: "#FFFFFF",
        primaryColor: "#967AA1"
    },
    {
        background: "#F7B267",
        color: "#000000",
        primaryColor: "#F4845F"
    },
    {
        background: "#F25F5C",
        color: "#000000",
        primaryColor: "#642B36"
    },
    {
        background: "#231F20",
        color: "#FFF",
        primaryColor: "#BB4430"
    }
];

const setTheme = (theme) => {
    const root = document.querySelector(":root");
    root.style.setProperty("--background", theme.background);
    root.style.setProperty("--color", theme.color);
    root.style.setProperty("--primary-color", theme.primaryColor);
    root.style.setProperty("--glass-color", theme.glassColor);
};

const displayThemeButtons = () => {
    const btnContainer = document.querySelector(".theme-btn-container");
    themes.forEach((theme) => {
        const div = document.createElement("div");
        div.className = "theme-btn";
        div.style.cssText = `background: ${theme.background}; width: 25px; height: 25px`;
        btnContainer.appendChild(div);
        div.addEventListener("click", () => setTheme(theme));
    });
};

displayThemeButtons();


const loginForm = document.querySelector("#login-form");
// const loginButton = document.querySelector("#login-button");
const loginButton = document.querySelector("#login-button");
loginButton.addEventListener("click", async function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // const formData = new FormData(loginForm);
    // // const data = Object.fromEntries(formData.entries());
  
    // console.log("Form data:", data); // Log the form data for debugging
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    // const password = data.password;
    const data = {
        username: username,
        password: password
    };

    console.log("Username:", username); // Log the username for debugging
    console.log("Password:", password); // Log the password for debugging

    try{
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            window.location.href = "/admin_viagens"; // Redirect to the dashboard on successful login
        } else {
            const errorText = await response.json();
            console.log(`Login failed: ${errorText}`); // Display error message
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("An error occurred. Please try again later.");
    }

    

    // try {
    //     const response = await fetch("/api/auth/login", {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json"
    //         },
    //         body: JSON.stringify(data)
    //     });

    //     if (response.ok) {
    //         window.location.href = "/dashboard"; // Redirect to the dashboard on successful login
    //     } else {
    //         const errorText = await response.text();
    //         alert(`Login failed: ${errorText}`); // Display error message
    //     }
    // } catch (error) {
    //     console.error("Error during login:", error);
    //     alert("An error occurred. Please try again later.");
    // }
});
