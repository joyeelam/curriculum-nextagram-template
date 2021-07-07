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

<!-- 7 July 2021 -->
---- current issues ----
- users.update only works if all fields are provided new values even though setattr should only apply if there is a key (empty fields checked to make sure no new keys are created)
- when tried uploading image, received werkzeug.exceptions.HTTPException.wrap.<locals>.newcls: 400 Bad Request: KeyError: 'username'
which refers to users/views.py line 49 - however, users.update works on its own, but cause an error in users.upload < is there a reason/correlation to this? does clicking upload also causes a submit for the users.update form?
