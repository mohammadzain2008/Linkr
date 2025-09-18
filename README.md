<h1 align='center'>Linkr</h1>

<div align='center'>

![GitHub Release](https://img.shields.io/github/v/release/mohammadzain2008/Linkr)
![GitHub License](https://img.shields.io/github/license/mohammadzain2008/Linkr)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/mohammadzain2008/Linkr/latest/total)
![GitHub repo size](https://img.shields.io/github/repo-size/mohammadzain2008/Linkr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/mohammadzain2008/Linkr/latest)
![GitHub last commit](https://img.shields.io/github/last-commit/mohammadzain2008/Linkr)
![GitHub milestone details](https://img.shields.io/github/milestones/progress-percent/mohammadzain2008/Linkr/1)

</div>

<hr>

<div align='center'>

[Introduction](#introduction)  •  [Installation](#installation)  •  [Usage](#usage)  •  [Releases](https://github.com/mohammadzain2008/Linkr/releases/)

</div>

## Table of Contents

- [Introduction](#introduction)
    - [A scenario where Linkr proves useful](#a-scenario-where-linkr-proves-useful)
    - [Why Linkr is better?](#why-linkr-is-better)
- [Installation](#installation)
    - [Source Code (for developers)](#source-code-for-developers)
    - [Executable files (only for version <2.1.0)](#executable-files-only-for-version-210)
- [Usage](#usage)
    - [Hosting files](#hosting-files)
        - [Setting up `ngrok`](#setting-up-ngrok)
        - [Hosting the directory using `ngrok`](#hosting-the-directory-using-ngrok)
    - [Different ways of using Linkr](#different-ways-of-using-linkr)
    - [Linkr CLI](#linkr-cli)
        - [Creating `linkr` manifests](#creating-linkr-manifests)
        - [Extracting `linkr` manifests](#extracting-linkr-manifests`)
    - [Linkr GUI](#linkr-gui)
    - [Linkr Terminal Command](#linkr-terminal-command)

## Introduction

Linkr is a simple file delivery system which downloads files hosted on a web server. 

- Using Linkr, a given directory can be summarised in a `linkr` file, also called a _Linkr Manifest_ which contains the information related to all the files in the directory and which servers host them.
- If the author is hosting the directory on a web server, any person with the Linkr Manifest can seamlessly download the directory to their device. This

This allows for mass distribution without having to upload gigantic files.

### A scenario where Linkr proves useful
<hr>

Suppose your friend has a game installed in their system which is about 200 GB in size and you want that game in your PC. You can use the following methods to achieve so:

- You can use a pen drive which is about 256 GB in size and ask your friend to transfer the game to it and then you can install the game in your PC. This roughly translates to about 400 GB of uploaded-downloaded data which takes quite some time.
- Alternatively, you can use a cloud service like Google Drive, One Drive, where your friend uploads the game and then you download the game from the cloud service, this, once again is time-consuming and requires large amount of cloud storage available which the average person does not purchase.
- Your friend can convert the game into a `.torrent` file and send you over that but once again, it takes a lot of time to do so since the file size is large.

This is where **Linkr** comes to the rescue. Let's go over the process of downloading your game using Linkr.

- First, your friend starts a local `http` server in the directory containing the 200 GB game. However, this is a local web server and cannot be accessed by you on a different device connected to a different network.
- To solve this, your friend exposes his/her `http` server using tools like `ngrok` which make this server accessible to you.
- Now, your friend runs **Linkr** and compresses the directory and sets the `url` to the one provided by `ngrok`. This creates a `.linkr` file which is quite small.
- Your friend sends you over this file and you extract it using **Linkr**. Now, Linkr will start downloading files from your friend's computer.
- This approach is much faster and does not involve any third-parties and thus ensures the integrity of the data.

### Why Linkr is better?
<hr>

- For the aforementioned methods, you upload and download the resource separately which is time-consuming. For Linkr however, the server uploads and you download simultaneously which drastically reduces total time.
- Linkr doesn't require third-party agents to partake in the supply chain. Only you and the web server hosting the files are connected without any other parties unlike cloud solutions or torrenting.

## Installation

### Source Code (for developers)
<hr>

To install the **Linkr source code**, run the following command.
```bash
git clone https://github.com/mohammadzain2008/Linkr.git
cd Linkr
```
All dependencies are mentioned in the `requirements.txt` file.

### Executable files (only for version <2.1.0)
<hr>

For regular users, you can download Linkr in one of two ways. **As of September 17, 2025, Linkr does not have binaries for macOS and Linux.**

1. Using **GitHub CLI**
```bash
gh release download v2.0.1 --repo mohammadzain2008/Linkr
```

2. Using **GitHub**

    - Go to `https://github.com/mohammadzain2008/Linkr/releases/tag/v2.0.1` and download the necessary executables.
    - To only use the command line interface (CLI), download `LinkrCLI-v2-0-1.exe`.
    - To use the Linkr GUI, donwload `LinkrGUI-v2-0-1.exe` along with `linkr.exe` because the GUI app requires the latter.
    - Also, ensure that `linkr.exe` and `LinkrGUI-v2-0-1.exe` are placed in the same directory always.

## Usage

### Hosting files
<hr>

#### Setting up `ngrok`
`ngrok` lets us expose our local web server so that anyone one the internet can access it. To set it up, follow the steps provided.
- Go to [https://ngrok.com/downloads/windows](https://ngrok.com/downloads/windows) and download ngrok. Follow the setup instructions until ngrok has been installed.
- Next, go to [https://ngrok.com/](https://ngrok.com/), sign up, and create a free account.
- After signing up, you will get an `authtoken` which you can find in your account settings.
- Open command prompt and enter the following:

```bash
ngrok config add-authtoken <your-authtoken>
```

- Once you get a confirmation message, you are good to go.

#### Hosting the directory using `ngrok`
A key part of the Linkr supply chain is hosting files. Thus, it is essential to know how to host your files in such a way that anyone on the internet can access them. **Python** is required for this process. You can download **Python** from [https://www.python.org/downloads/](https://www.python.org/downloads/). Once Python is installed, we can begin.
- First identify the directory you want to host. In our case, let the directory be `F:\john doe\myfiles\`.
- Next, navigate to the directory using File Explorer.
- Once you are there, in the search on the top, type `cmd`. This will open the command prompt in that directory.
- Now, enter the command given below.

```bash
python -m http.server 8080
```

    You should see the following message in the terminal if the process went as planned.

```bash
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

- Now, we need to expose our local web server so that anybody on the internet can access it. This can be achieved using **ngrok**. Open another command prompt window from anywhere and type the following:

```bash
ngrok http 8080
```

- You should see the following on your screen:

```bash
Session Status                online
Account                       <your-name> (Plan: Free)
Update                        update available (version 3.28.0, Ctrl-U to update)
Version                       3.24.0-msix
Region                        India (in)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://0a4aeebb8c3a.ngrok-free.app -> http://localhost:8080
```

    The useful thing here is the _Forwarding_, this is the address where your directory is hosted i.e. `https://0a4aeebb8c3a.ngrok-free.app`.

### Different ways of using Linkr
<hr>

After installing Linkr using one of the two methods mentioned above, you can now use the software. There are three ways to use Linkr:
- **Linkr CLI** (`LinkrCLI-v2-0-1.exe`)
- **Linkr GUI** (`LinkrGUI-v2-0-1.exe`)
- **Linkr Terminal Command** (`linkr.exe`)

### Linkr CLI
<hr>

**Linkr CLI** is a standalone application and does not need any other dependencies to run. Once started, the interface prompts you to choose between two option: **compress** and **extract**.
- **Compress** is used to create linkr manifests of a directory.
- **Extract** downloads the directory from a linkr manifest.
Let's first learn to create linkr manifests.

#### Creating `linkr` manifests
1. To create a `linkr` manifest, type `1` inside the CLI interface.
2. Now, enter the name of the package you want to create, it could simply be the name of your directory you are compressing.
3. Next, enter the path to the directory where your files are stored. It can either be the relative path or the absoulte path.
4. Now, enter the server URLs where your files are or will be hosted. You can enter multiple server URLs. While extraction, if one server URL fails, then the other URL will be used. For instance, if your files are stored at `https://example.com` and `https://example2.com/files`, then the input in the CLI will be `https://example.com,https://example2.com/files`. If you are using `ngrok`, then enter the _Forwarding_ address obtained from ngrok.

If you did the above correctly, you will get the following message:

```bash
[SUCCESS]: Created Package.linkr with 1 files.
```

This means that your `Package.linkr` file was created and is ready for distribution.

You will also get another message:

```bash
[WARNING]: Make sure to upload Sample.linkr file to the same servers where the files are hosted for integrity verification to prevent tampering.
Place the file so that it is accessible at the following URLs:
- http://example.com/Sample.linkr
- http://example2.com/files/Sample.linkr
```

It is highly recommended that you host your created Linkr manifest on the web servers hosting your files. This ensures that the integrity of your linkr manifest is preserved. This ensures that your distributed linkr manifest is not tampered with during distribution as the Linkr software always compares it to the one hosted by you. If you are using **ngrok**, simply place the linkr manifest inside the directory where you are hosting files.

This completes the compression process.

#### Extracting `linkr` manifests
1. To extract a linkr manifest, type `2` when prompted by the Linkr CLI.
2. Now, enter the absolute/relative path to the `.linkr` file.
3. Enter the name of the destination folder where you want the files to be placed.
4. You will now see the prompt:
```bash
Override checksum errors? (y/n):
```
    If you enable this, then any file that has been tampered with will not be downloaded. If you disable this, tampered files will not be deleted, but you will still be warned about them.
5. Now, you will see the prompt:
```bash
Perform integrity check with server? (y/n):
```
    If enabled, your linkr manifest will be compared with the one created by the author. It is highly recommended that you enable this. If the integrity check fails, the extraction process will be aborted.

You shall now be able to find your downloaded files inside the destination folder.

### Linkr GUI
<hr>

Using Linkr GUI is pretty straightforward as the interface is much more user-friendly than the CLI. However, if you plan on using the GUI, make sure that `linkr.exe` is in the same location as that of the GUI application.

### Linkr Terminal Command
<hr>

If you are inside the directory where `linkr.exe` is present, you can directly run Linkr from the command line by entering the following commands from `compress` and `extract` respectively.

```bash
linkr compress <package_name> <folder_path> <server_url_1> <server_url_2> ...
linkr extract <file_path> <folder_path> --override-checksum --no-integrity-check
```

If you don't want to override checksum errors, then remove the `--override-checksum` flag. If you want to perform linkr manifest integrity check, then remove the `--no-integrity-check` flag.