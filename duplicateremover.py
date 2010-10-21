from pyoperalink.auth import OAuth
from pyoperalink.client import LinkClient
from pyoperalink.datatypes import Bookmark, BookmarkFolder, SpeedDial

auth = OAuth('wpsa7q7BnsYMtnBMiyjzLKGK9oM3ugRP',
             'dowwds2Istr96e7zl9TmqkM46WrKBLwO')

# Get the access token (load from file or get from the server)
try:
    with open('access_token.txt', 'r') as token_file:
        a_t = token_file.readline().rstrip()
        a_t_s = token_file.readline().rstrip()
        auth.set_access_token(a_t, a_t_s)
except IOError:
    url = auth.get_authorization_url()
    print "Now go to:\n\n%s\n\nand type here the verifier code you get:" \
        % (url)
    verifier = raw_input()
    if verifier == "":
        print "You need to write the verifier code. Please try again."
        sys.exit(1)
    token = auth.get_access_token(verifier)
    with open('access_token.txt', 'w') as token_file:
        token_file.write("%s\n%s\n" % (token.key, token.secret))

client = LinkClient(auth)
speeddials = client.get_speeddials()
speeddial_urls = [sd.uri for sd in speeddials]
print "The list of Speed Dial URLs is:", speeddial_urls

bookmarks = client.get_bookmarks() # Only top-level bookmarks
for bookmark in bookmarks:
    if isinstance(bookmark, Bookmark) and bookmark.uri in speeddial_urls:
        print "Moving bookmark '%s' to Trash" % (bookmark.title,)
        client.trash_bookmark(bookmark.id)
