# Project Status Notice

Please read this important notice regarding the project. Because I am working alone on this system without any help, updates are taking a long time to build and release. I need **community support** immediately. If developers do not join the project to help out, I will be forced to close this repository down in **approximately three weeks**. If you want to keep this project alive, please reach out, open an issue, or submit a pull request today.

----------------------------------------------------------------

# Webbey-AI

**Webbey-AI** provides a secure, lightweight, and locally-driven AI assistant for **GitHub** and other websites. The application allows users to interact with a smart chat bot directly inside a website panel while maintaining complete ownership and control over their private connection data.

## Security Principles and Private Tokens

Unlike alternative browser assistants that require you to upload your secret personal access tokens to an external server, **Webbey-AI** uses a strict **zero-storage architecture**.

When you boot the application on your computer, you enter your authorization token directly into a temporary memory slot inside your system **RAM**. This configuration enforces three absolute safety parameters:

* **No Saved Data:** No data is saved to your computer disk, database, or browser configuration profile.
* **Direct Routing:** Your authentication keys are passed **directly to GitHub and only to GitHub**.
* **Volatile Memory:** The exact moment you stop running the script, your temporary tokens are **completely wiped** from your system memory.

----------------------------------------------------------------

## Operating Configurations

The application is designed to be highly adaptive and runs across different machine setups depending on your needs.

### Local Sandbox Mode
This mode is designed for development, testing, and private use on your personal laptop or desktop computer. It spins up a temporary test site on your local machine and uses **port 5000** to listen for your messages.

### Cloud Server Mode
This mode is designed specifically for deployment on remote **virtual private servers (VPS)**, **virtual dedicated servers (VDS)**, or **raw bare-metal server infrastructure**. It switches the system to a heavy production server framework, locks the API down with a secure admin passkey, and opens up communication on **port 8080**.

----------------------------------------------------------------

## How You Can Help

To prevent this repository from closing in **three weeks**, I am actively looking for volunteers to help with the following tasks:

* **Front-End Design:** Helping to polish and style the main visual elements of the admin interface file.
* **System Scripts:** Improving the shell automation files to streamline starting up and switching modes.
* **Feature Extensions:** Adding deeper integrations so the assistant can read repository source files and interact with pull requests.

If you are interested in preserving this project, please clone the repository, make your modifications, and submit a **pull request** as soon as possible. Your assistance is greatly appreciated.

----------------------------------------------------------------

## License & Contact

* **License:** Distributed under the **MIT License**. Feel free to use, modify, and distribute.
* **Contact:** Reach out by opening a **New Issue** or **Discussion** directly on the GitHub repository page to coordinate maintenance tasks.
