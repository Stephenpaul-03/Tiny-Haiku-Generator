# Tiny Haiku Generator

Generate 5-7-5 haikus using classic books from [Project Gutenberg](https://www.gutenberg.org). This tool uses Markov chains to create text and filters results by syllable count for proper haiku structure.


## Features

- Search and download public domain books
- Clean and process text automatically
- Train a Markov model for text generation
- Generate 5-7-5 haikus from trained models
- Optional clipboard copy support


## Installation

1. **Clone the repository**

```bash
git clone https://github.com/Stephenpaul-03/Tiny-Haiku-Generator.git
cd Tiny-Haiku-Generator
````

2. **Install required packages**

```bash
pip install -r requirements.txt
```

##  Usage

Run the main script:

```bash
python main.py
```

Follow the prompts to:

* Search for a book
* Download and clean the text
* Train a model
* Generate haikus


##  Project Structure

```
Tiny-Haiku-Generator/
├── main.py          # User interface and control flow
├── scraper.py       # Book search and download logic
├── trainer.py       # Text processing and haiku generation
├── Books/           # Saved and cleaned book files
├── Trained_Models/  # Pickled Markov models
├── requirements.txt # Python dependencies
```

>NOTE: Models are saved after training for faster reuse


## License

This project is open-source and available under the [MIT License](LICENSE).

