# New Release Procedure
  1. Change __version__ in __init__.py
  2. Add changelog to README.md
  3. Make a comit with the form pydicts-$NEWVERSION$
  4. git push
  5. Create a new release setting $NEWVERSION$
  6. poetry publish --username --password

