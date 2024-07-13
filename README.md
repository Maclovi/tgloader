# YouTube Audio Downloader Bot

## Overview

**YouTube Audio Downloader Bot** is a Telegram bot that allows users to download audio from YouTube links. The bot is designed with future scalability in mind, allowing for easy extension to support additional sources beyond YouTube.

## Features

- Download audio from YouTube links.
- File download limit up to 2 GB 
- Future support planned for additional sources.

## Installation

### Requirements

- Python 3.10 or higher
- PostgreSQL 14 or higher
- Telegram bot token (from [BotFather](https://t.me/botfather))
- Telegram application with **api_id & api_hash** ([create client](https://my.telegram.org/))
- Telegram group for errors
- Telegram group for cache
### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Maclovi/tgloader.git 
cd tgloader
```
### Dependencies

Install the required Python libraries:

```bash
pip install .
```
### How to start
1. Edit code in a correspoing way
2. Rename example.config.ini to config.ini
3. Fill out the confg.ini

## Usage

Run the bot:
```bash
runbot
```
### Authorization

After starting the bot, first of all you need to log in.
The bot will ask you to log in for YouTube and then for the Telegram client.
### Commands

- **/start** - Display a welcome message and usage instructions.
## Example

1. Send the `/start` command to see the welcome message and instructions.
2. Send link from youtube to extract audio
## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Future Plans

- Adding support for downloading from other sources like SoundCloud, Vimeo, etc.
- Implementing a web interface for easier access.

## Author

**Sergey** - [GitHub Profile](https://github.com/Maclovi)

---

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/Maclovi/tgloader/issues).
