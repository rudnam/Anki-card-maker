# Anki card maker
#### Video Demo:  <https://youtu.be/JFYppvtlXMo>
#### Link: https://ankicardmaker.herokuapp.com/
## Description
This is a simple web application that takes in one or more sentences or phrases in Japanese and automatically makes Anki cards from the words that appear on the inputted sentences. Anki is an application that allows users to make flashcards to help users memorize terms and all sorts of things more effectively using spaced repetition. The cards generated by this application have the type "iKnow! Sentences-797eb", it currently does not support other card types.

## Using the application
On the homepage there is a textarea where the user can type in japanese sentences or phrases to generate the Anki cards from. The user can input more than one sentence/phrase as a time as long as each expression is separated by a newline, this is to make sure that the cards can properly detect the expression from where a word or term originated from. Click the "Generate cards" button to generate the cards.

The generated cards are shown on the table separated by field. The default output by the application are cards with its respective expressions where it originated from, meanings/definitions obtained from jisho.org, and the reading (for conjugated verbs only the root verb's pronunciation is given). The user can choose to edit fields of the generated cards by clicking the edit button on the right side of the row one wants to modify. The user can also quickly delete a card by clicking the delete button on the right side of a row. The user can quickly delete all cards by clicking the clear button.

Once satisfied with all the card fields, the user can download the cards as a csv file for importing to an anki deck.

## Available settings
The user can change some settings for the application by clicking the settings button on the top right of the webpage.
Available settings are the following:
* Definitions limit: maximum number of definitions taken from Jisho.
* Default audio: default data for the audio field.
* Default image_URI: default data for the image_URI field.
* Default iKnowID: default data for the iKnowID field.
* Default iKnowType: default data for the iKnowType field.
* Default Tag: default data for the Tag field.

## Adding cards to Anki deck using the csv file
The user can add the cards to an existing Anki deck by opening the Anki application, going to File > Import..., select the output.csv obtained from the Anki card maker. Make sure that the card type selected is "iKnow! Sentences-797eb" and deck selected is correct. The user can now use the cards generated by the application to help in studying Japanese vocabulary.

## Tools used

* Jisho api
* jisho-api 0.1.8 - jisho.org API and scraper in Python.
* Flask
* SQLite3
* SQLAlchemy
