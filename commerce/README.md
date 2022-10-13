# CS50w - pset2 - Commerce

## Auctionly

This is my submission for problemset2 Commerce for cs50web

This is a django web app about an ecommerce auction website.

The website handles visits between anonymous users and registered ones.
An anonymous user can browse all the listings in the website and the category section;
he can see all the active listing, browse the content, the image, description, owner, starting price and current price, but cannot either place a bid, leave a comment or add the item to his watchlist.

If an user logs in the interface changes and now the user can visually differentiate between the auctions he posted that will be highlighted in blue, from the auctions other users posted, that will be highlited in green.

Every auction in the main view are displayed as a card containing the name of the owner of the listing, the image, the title, the current price and a snippet of the description that is actually a slice from the original description taken from the Listing model.

An authenticated user can either add or remove the item to his watchlist, we'll see the counter of the people following update, he can leave a comment where his username will be colored in blue, while other's comments will be displayed with a green username.
If the user is the owner of the item, he can only close the auction and not place further bids, while if he visited another user's auction, he can place a bid.

A lower bid price will be rejected and an error will appear, while if the bid was valid, the current price would update.

The owner of the listing will be able to close the auction, then the page updates displaying the name of the user that won the auction, or a message that mentions that "no one bought the item" if no bids were placed.
On the other hand if the user won the auction of an item from another user, and the auction closes, a message that "you won the auction" will appear.

An authenticated user can also create a new auction, where he will be prompted to input a title, a starting price for the item, a link to an image, the description and the category it should be listed under.
If no image URL was provided, it would default to a preset one just as a placeholder, same applies for the category that if none were selected, it would fall under the "No-category view"

Lastly, *My Listings* is a view that displays all the auction the current user has posted, that will also display all the auction we set as closed (they will visually appear with a grey accent), so that the owner can still be able to open up the listing and see the winner of the auction, without having to manually enter the id in the URL.

<hr>
The best feature I found so useful to implement from django was the ability to create an html template for an auction card, and the ability to implement the same template in every different view (Homepage, Category, My Listings and Watchlist) that just displays the same base template that will be handled differently by the logic of each view.

#### -- Conclusion --
This was by far the most interesting project I've done until now, it was my first experience using Django, and while the learning curve wasn't as easy as the one for Flask, the tools at our disposal are so many and so powerful that in the end adding or tweaking functinalities ad feature was actually a lot faster and easier after a bit of research.

