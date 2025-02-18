# GitLab User Domains Extractor

## 📌 Overview

This script extracts all user emails from a GitLab instance, retrieves unique email domains, and saves them to a file.  
The extracted domains can be used to configure the **whitelist in GitLab Admin settings**.

## 🚀 Features

- Connects to GitLab API securely  
- Extracts all users and their emails  
- Identifies **unique email domains**  
- Saves data to files:
  - **`all_users_with_domains.txt`** – List of users with their emails  
  - **`unique_domains.txt`** – Extracted unique email domains  
- Handles **API errors, missing emails, and connection issues**  
- Supports **environment variables** and **CLI arguments** for configuration  

---

## 📂 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GurbanV/gitlab-user-domains.git
   cd gitlab-user-domains
   pip3 install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Option 1: Using Environment Variables (.env)**:
  Create a .env file in the project root and add your GitLab credentials:
  ```bash
  GITLAB_URL=https://your-gitlab-instance.com
  PRIVATE_TOKEN=your-private-token
  ```
  The script will automatically load these variables.

2. **Option 2: Using Command-Line Arguments**:
   You can also pass GitLab credentials directly as arguments:
   ```bash
   python main.py --gitlab-url "https://your-gitlab-instance.com" --token "your-private-token"
   ```
   
## 📜 Usage
Run the script:
  ```bash
  python3 main.py
  ```
Or with custom GitLab credentials:
  ```bash
  python3 main.py --gitlab-url "https://your-gitlab-instance.com" --token "your-private-token"
  ```

**Output Files**:
  - all_users_with_domains.txt – Contains all usernames and emails
  - unique_domains.txt – Contains unique email domains
   

## 🛠 Error Handling
The script includes robust error handling for:

Authentication failures (exit code 2)
Connection issues (exit code 3)
API errors (exit code 4)
File writing errors (exit codes 5 and 6)
Unexpected errors (exit code 7)
If an error occurs, detailed logs will be displayed in the console.


## 🏗️ Contributing
1. Fork the repo
2. Create a new branch:
  ```bash
git checkout -b feature-branch
  ```
3. Commit changes:
  ```bash
git commit -m "Add new feature"
  ```
4. Push to branch:
  ```bash
git push origin feature-branch
  ```  
5. Open a Pull Request


## 📄 License
This project is licensed under the MIT License. See LICENSE for details.


## ⭐ Support
If this script helped you, give it a ⭐ on GitHub!

