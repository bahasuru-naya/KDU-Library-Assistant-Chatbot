from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from groq import Groq


def connect_to_mongodb():
    uri = "mongodb+srv://phdbahasuru:qlZfdD77IUx3xj8G@cluster0.1omwaw2.mongodb.net/"
    database_name = "Book"

    try:
        # Create a MongoClient instance
        cli = MongoClient(uri)

        # Connect to the specified database
        db = cli[database_name]

        # select collection
        collection = db["book_data"]

        print(f"Successfully connected to database: {database_name}")
        return collection
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


class ActionGiveDescription(Action):
    def name(self) -> Text:
        return "action_give_description"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_name = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"title": book_name}, {"description": 1, "_id": 0})

            if book and "description" in book:
                book_des = book["description"]
                dispatcher.utter_message(f"Here's a brief description of'{book_name}': \n {book_des}")
            else:
                dispatcher.utter_message(f"No description found for the book titled '{book_name}'.")
        else:
            dispatcher.utter_message("You haven't provided the book name. Please specify the book name.")

        return []


class ActionGiveNumPages(Action):
    def name(self) -> Text:
        return "action_give_num_pages"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_name = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"title": book_name}, {"num_pages": 1, "_id": 0})

            if book and "num_pages" in book:
                book_num_pages = book["num_pages"]
                dispatcher.utter_message(f"The book {book_name} has {book_num_pages} pages.")
            else:
                dispatcher.utter_message(f"Can't find number of pages for the book titled '{book_name}'.")
        else:
            dispatcher.utter_message("You haven't provided the book name. Please specify the book name.")

        return []


class ActionGiveRatings(Action):
    def name(self) -> Text:
        return "action_give_ratings"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_name = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"title": book_name}, {"average_rating": 1, "_id": 0})

            if book and "average_rating" in book:
                book_ratings = book["average_rating"]
                dispatcher.utter_message(f"The average rating of {book_name} is {book_ratings}/5.")
            else:
                dispatcher.utter_message(f"Can't find ratings for the book titled '{book_name}'.")
        else:
            dispatcher.utter_message("You haven't provided the book name. Please specify the book title.")

        return []


class ActionGiveYear(Action):
    def name(self) -> Text:
        return "action_give_published_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_name = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"title": book_name}, {"published_year": 1, "_id": 0})

            if book and "published_year" in book:
                book_published_year = book["published_year"]
                dispatcher.utter_message(f"{book_name} was published in the year {book_published_year}.")
            else:
                dispatcher.utter_message(f"No published year found for the book titled '{book_name}'.")
        else:
            dispatcher.utter_message("You haven't provided the book name. Please specify the book name.")

        return []


class ActionGiveAuthor(Action):
    def name(self) -> Text:
        return "action_give_author"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_name = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"title": book_name}, {"authors": 1, "_id": 0})

            if book and "authors" in book:
                book_author = book["authors"]
                dispatcher.utter_message(f"{book_name} was written by {book_author}.")
            else:
                dispatcher.utter_message(f"No author found for the book titled '{book_name}'.")
        else:
            dispatcher.utter_message("You haven't provided the book name. Please specify the book name.")

        return []


class ActionGiveBookTitle(Action):
    def name(self) -> Text:
        return "action_give_book_title"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_author = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"authors": book_author}, {"title": 1, "_id": 0})

            if book and "title" in book:
                book_name = book["title"]
                dispatcher.utter_message(f"{book_name} was written by {book_author}.")
            else:
                dispatcher.utter_message(f"No book found for the author named '{book_author}'.")
        else:
            dispatcher.utter_message("You haven't provided the author name. Please specify the author name.")

        return []


class ActionGiveBookRecommendationCategory(Action):
    def name(self) -> Text:
        return "action_give_book_recommendation_with_category"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            category = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified category
            book_cursor = (db.find(
                {"categories": category},  # Filter by the given category
                {"title": 1, "authors": 1, "description": 1, "average_rating": 1, "_id": 0})
                           .sort("average_rating", -1).limit(1))

            try:
                # Extract the book document
                book = next(book_cursor)  # Get the first document from the cursor
                book_name = book["title"]
                book_author = book["authors"]
                book_description = book["description"]
                book_ratings = book["average_rating"]

                # Respond with the book details
                dispatcher.utter_message(
                    f"I highly recommend '{book_name}', an excellent book written by {book_author} "
                    f"in the {category} category. It boasts an impressive average rating of {book_ratings}/5. "
                    f"Here's a brief description to pique your interest: \"{book_description}\". "
                    f"I hope you enjoy reading it!"
                )
            except StopIteration:
                # No book found in the category
                dispatcher.utter_message(
                    f"No book found for the category named '{category}'. Here are the available categories in the library: \n"
                    f" - fiction \n"
                    f" - non-Fiction \n"
                    f" - children \n"
                    f" - educational \n"
                    f" - religious \n"
                    f" - art \n"
                    f" - comics  \n"
                    f" - poetry \n"
                    f" - lifestyle \n"
                    f" - technology \n"
                    f"Please try again."
                )
        else:
            # No category provided
            dispatcher.utter_message(
                f"You haven't provided the category of the book. Please specify the category. \n"
                f"Here are the available categories in the library: \n"
                f" - fiction \n"
                f" - non-Fiction \n"
                f" - children \n"
                f" - educational \n"
                f" - religious \n"
                f" - art \n"
                f" - comics  \n"
                f" - poetry \n"
                f" - lifestyle \n"
                f" - technology \n"
            )

        return []


class ActionGiveMostRatedBook(Action):
    def name(self) -> Text:
        return "action_give_most_rated_book"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db = connect_to_mongodb()

        # Query the collection for the book with the specified title
        most_rated_book = db.find_one(
            sort=[("average_rating", -1)],  # Sort by average_rating in descending order
            projection={"title": 1, "authors": 1, "description": 1, "average_rating": 1, "_id": 0}
            # Include title, authors, description; exclude _id
        )

        if most_rated_book:
            book_name = most_rated_book["title"]
            book_author = most_rated_book["authors"]
            book_description = most_rated_book["description"]
            book_ratings = most_rated_book["average_rating"]
            dispatcher.utter_message(f"The most rated book is '{book_name}', written by {book_author}. "
                                     f"It has an impressive average rating of {book_ratings}/5. Here's a brief "
                                     f"description to spark your interest: "
                                     f"\"{book_description}\". Happy reading!")
        else:
            dispatcher.utter_message(f"Error!.No books found in the database.")

        return []


class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_name = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"title": book_name}, {"borrowed": 1, "_id": 0})

            if book["borrowed"]:
                dispatcher.utter_message(f"Sorry, {book_name} is currently borrowed. You can borrow it later.")
            else:
                dispatcher.utter_message(f"Good news! {book_name} is available. You can borrow it ")
        else:
            dispatcher.utter_message("You haven't provided the book name or provided book is not available in our "
                                     "library. Please try again with a different book name.")

        return []


class ActionShowBookCover(Action):
    def name(self) -> Text:
        return "action_show_book_cover"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities', [])

        if entities:
            book_name = entities[0]['value']

            db = connect_to_mongodb()

            # Query the collection for the book with the specified title
            book = db.find_one({"title": book_name}, {"thumbnail": 1, "_id": 0})

            if book and "thumbnail" in book:
                components = {
                    'url': book["thumbnail"]

                }

                dispatcher.utter_message(
                    text=f"Here is an cover image of {book_name}\n",
                    image=components['url']
                )

            else:
                dispatcher.utter_message("Sorry, I couldn't find that item in our library.")
        else:
            dispatcher.utter_message("You haven't provided the book name. Please specify the book name")

        return []


client = Groq(
    api_key="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",
)


class ActionNLUFallback(Action):
    def name(self) -> Text:
        return "action_nlu_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the latest user message
        user_message = tracker.latest_message['text']
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"General Sir John Kotelawala Defence University Library (KDUL) is the main student "
                               f"support services the University offer for the learning and advancement of knowledge "
                               f"of the KDU community."
                               f"The library supports students to achieve their learning goals and to make them "
                               f"learned professionals with higher graduate profiles. The library supports University "
                               f"to achieve its mission by providing dynamic and proactive information services. KDUL "
                               f"network is to provide a variety of resources in multiple formats which to enhance "
                               f"teaching, learning and research activities of the University."
                               f"The KDU Library network consists of the Main Library, Southern Campus Library, "
                               f"and two faculty libraries; the Library of Faculty of Medicine and the Faculty of "
                               f"Allied Health sciences. It caters to over 6000 members, including both students and "
                               f"staff.                                                                             "
                               f"'{user_message}' answer this question without greetings in one paragraph as book "
                               f"recommendation chatbot in General Sir John Kotelawala Defence University library at "
                               f"sri lanka and also write answer briefly and Don't answer unrelated questions about "
                               f"library and explain user that you can only answer"
                               f"library related questions "

                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        final_output = ""
        for chunk in completion:
            # print(chunk.choices[0].delta.content or "", end="")
            final_output += chunk.choices[0].delta.content or ""
        print(f"Fallback response - {final_output}")
        # remove unnecessary spaces
        cleaned_text = ' '.join(final_output.split())
        # Custom logic using user_message
        dispatcher.utter_message(text=f"{cleaned_text}")

        return []
