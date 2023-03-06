# Assistant Pascal

Assistant Pascal is a voice chatbot that uses Google Text-to-Speech (gTTS) and SpeechRecognition to listen and respond to user input. The chatbot is built using the SpeechRecognition library, the gTTS library, openai library, and the Pygame library.

Assistant Pascal est un chatbot vocal qui utilise Google Text-to-Speech (gTTS) et SpeechRecognition pour écouter et répondre aux entrées utilisateur. Le chatbot est construit en utilisant la bibliothèque SpeechRecognition, la bibliothèque openai, la bibliothèque gTTS et la bibliothèque Pygame.
## Installation

To use this chatbot, you will need to have Python 3.x and pipenv installed on your computer. If you do not already have Python installed, you can download the latest version from the [official Python website](https://www.python.org/downloads/). To install pipenv, run the following command in your terminal or command prompt:
```bash
pip install pipenv
```
Next, navigate to the project directory and run the following command to install the project dependencies:
```bash
pipenv install
```

This will create a new virtual environment and install the dependencies specified in the Pipfile.lock file.

## Usage

Look at constants.py to set preferences.

you need a folder called audio in your root folder of your project

To use the chatbot, activate the virtual environment by running the following command:
```bash
pipenv shell
```
This will activate the virtual environment and allow you to run the project commands.

To start the chatbot, run the following command:
```bash
python main.py
```
This will start the chatbot and prompt you to speak. You can ask the chatbot any question or give it any command by speaking into your microphone. The chatbot will respond with a spoken message and a printed message in the console.

## ChatBot ChatGPT Wrapper usage
```python

# Instantiate a Chatbot object with a GPT-3.5 Turbo model and a custom initial message
bot = ChatBot("davinci", "Hello, how can I assist you today?")

# Send a message to the chatbot with a low temperature
bot.send_message("Who won the world series in 2020?")
bot.get_response(temperature=0.3)

# Send a message to the chatbot with a high presence penalty
bot.send_message("What's the capital of France?")
bot.get_response(presence_penalty=0.8)

# Send a message to the chatbot with a high frequency penalty
bot.send_message("Tell me a joke.")
bot.get_response(frequency_penalty=0.8)
```

## Contributing

If you would like to contribute to this project, you can do so by submitting bug reports, feature requests, or pull requests on the GitHub repository. Please ensure that your contributions are in line with the project's goals and objectives.

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

## Credits

This project was inspired by [SpeechRecognition documentation](https://pypi.org/project/SpeechRecognition/), [gTTS documentation](https://pypi.org/project/gTTS/), and [Pygame documentation](https://www.pygame.org/docs/).

## Contact

If you have any questions or concerns about this project, please open a pull request.

