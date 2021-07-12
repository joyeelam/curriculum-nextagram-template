Current Features:
1. Create, edit and delete user profile
    - user can create profile using Google OAuth, random username & password is assigned
    - change profile picture
    - change username, email, password
2. Log-in and log-out
    - user can log-in using Google OAuth
3. Upload posts with optional captions
4. Edit posts
    - add/edit caption
    - option to delete post
5. Explore page that shows posts from all users
6. Search option to find users by username
7. Users can set profile as private
8. Users can view posts individually
9. Users can donate selected amount to posts
10. Dashboard on user profiles - total donations, no. of posts, (to add followers count as well)

Features to add:
1. Mailgun API sending email

---- to fix ----
1. Add slide buttons to carousel
2. Streamline use of user vs current_user in templates/forms
3. Clean up spacing and streamline use of single quotes/double quotes
4. Fix flash messages content
5. Add proper alt attribute to img tags
6. Rendering of posts - latest upload comes first
7. Rendering of users.index - show by images, not users

---- non-RESTFUL (to edit/modify) ----
1. users.update - added "update" to differentiate with "upload"
2. users.upload - added "upload" to differentiate with "update"
3. users.show - used <username> instead of <id>
4. users.search - used "search"
5. posts.create

12 July 2021 (to review & fix)
1. donations/views.py
	- Line 29, 32
		- Since these two lines are actually identical, you can skip the one on line 29, and remove the else on line 32, that way both conditions will lead to "post/show.html" on error
2. users/views.py
	- Line 123
		- This part can be done by using list comprehension to shorten code, e.g.
		sum([d.amount for d in [d for d in i.donations]])
		- Theres also n + 1 happening here, for each image, get donations use prefetch here to prevent that, you can prefetch more than two things, https://docs.peewee-orm.com/en/latest/peewee/api.html?highlight=prefetch#prefetch

<!-- 7 July 2021 -->
<!-- ---- current issues ----
- users.update only works if all fields are provided new values even though setattr should only apply if there is a key (empty fields checked to make sure no new keys are created)
- when tried uploading image, received werkzeug.exceptions.HTTPException.wrap.<locals>.newcls: 400 Bad Request: KeyError: 'username'
which refers to users/views.py line 49 - however, users.update works on its own, but cause an error in users.upload < is there a reason/correlation to this? does clicking upload also causes a submit for the users.update form?

---- feedback/comments ----
1. You might wanna first fix the logic error in the update first, because right now, it only loops through 1 key, then after that, you save and return, which ends the function, meaning the other keys don't get saved [fixed]
2. This is a problem with the url that you have, both update and upload have the same url, so it went in the first one, ignoring your upload [fixed]
- Try fixing these and see if the first problem persists -->

<!-- 6 July 2021 -->
<!-- ---- features to add ----
- validation for casing in username > only allow lower_case?

---- questions ----
- should header live in "_layout.html"? as more pages are added, the if/else might get bloated over time, or should a new header be rendered in each page according to the page's requirement?

---- feedback/comments ----
1. Good work on using remember=True!
2. You can change the FLASK_ENV to production to test the error 500 page, just cause an error to happen in one of your route and then visit it. But as long as the other error handler works, the 500 one should work as well.
3. Headers can actually stay in layout, because some pages are shown for both logged in and non logged in users, so those pages doesn't need to be in the if else statement
4. For the displaying of error in your sign up form, you're doing a loop for every single category, in this case you might wanna consider changing errors to a dictionary instead of a list.
5. For the user_loader for flask-login, you might wanna change User.get_by_id into get_or_none because the docs specifies that if somehow given id doesn't correspond to a user, it should return None
6. Overall nicely done! Good job on understanding the docs and setting up flask-login! -->
