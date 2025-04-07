<h1>Test Assignment for the Junior Python Developer Position</h1>

<h3 style="color: red">General Task Description: </h3>
<p>It is required to implement a Telegram bot for expense tracking, which will interact with a server to perform CRUD operations via API requests.</p>

<div style="border: 1px solid white; padding: 10px; padding-top: 0px;">
<h3 style="color: red">Assignment</h3>

<h4>Implement the server-side of the Telegram bot as an API using the FastAPI framework.</h4>
<p>The API should include the following endpoints:</p>
<ul>
    <li>Get a list of expenses by date.</li>
    <li>Add an item to the expense list (when adding an expense item, the UAH/USD exchange rate should be parsed to record the expense also in USD; parsing can be done using Selenium or requests + BeautifulSoup).</li>
    <li>Delete an expense item by ID.</li>
    <li>Edit an expense item by ID.</li>
</ul>
<i>The API must use SQLAlchemy to interact with the database.</i>

<hr>

<h4>Implement the Telegram bot using the latest version of the aiogram library.</h4>

<p>After the /start command, the user receives a menu with the main functions. Using the "add expense" option, the user enters the name, date in the format dd.mm.YYYY, and the amount in UAH. The bot then sends the data to the API, where additional processing includes converting it to USD, and saves the record in the database. After a successful operation, the bot informs the user of the result and returns to the menu.</p>
<p>The "get report" function allows the user to specify a start and end date for generating a report. The bot contacts the API, retrieves data for the specified period, and creates an .xlsx file, which is sent to the user along with the total expenses. The main menu is then reopened.</p>
<p>For deleting an expense, the bot sends a file with a list of all expenses, including IDs. The user enters the ID of the desired item, and the bot sends a request to the API to delete it and informs the user of the result. After that, the bot returns to the main menu.</p>
<p>The "edit expense" function works similarly: the bot first sends a file with the list of expenses, the user selects an ID, receives information about the corresponding item, and enters new data. The bot then updates the record via the API, informs the user of the success, and returns to the menu.</p>

</div>