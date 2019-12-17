module Post exposing ( Post
                         , save
                         , publish
                         , fetch
                         , new
                         , decoder
                         , encode
                         )
{-| This module is part of demnet.
It provides all utility functions for handeling
the Post type.

# Definition
@docs Post
# Networking functions
@docs save, publish, upload, fetch
# Conversion
@docs new, decoder, encode
-}

import Http
import Json.Decode as D
import Json.Encode as E

{-| Utility type for all response messages (for when packets arive)
-}
type alias Expect_Msg msg = ( Result Http.Error String -> msg )

{-| Post, a simple data type to store a single Post.
content is special in that it is actually parsed as markdown.
-}
type alias Post = { saved : Bool
                  , title : String
                  , content : String
                  , author : String
                  }
{-| Save a Post on the server, but don't publish it.
If you want to publish a Post use [`publish`](#publish)
-}
save : Expect_Msg msg -> Post -> Cmd msg
save = upload "save"

{-| Publish a Post on the network.
After this the Post is immutably on the network.
If you just want to save your post for later and not yet publish,
use [`save`](#save)
-}
publish : Expect_Msg msg -> Post -> Cmd msg
publish = upload "publish"

{-| The function behing both [`save`](#save) and [`upload`](#upload).
The only difference between the two is that they speck to different
routes. The Request is the same.
**This function isn't exposed.**
-}
upload : String -> Expect_Msg msg ->  Post -> Cmd msg
upload url expect p
  = Http.post { url = "/content/" ++ url
              , body = Http.jsonBody <| encode p
              , expect = Http.expectString expect
              }

{-|  Fetch a few Posts.
You should use this command in combination
with [`new`](#new), which has the type: `String -> List Post`
-}
fetch : Expect_Msg msg  -> Cmd msg
fetch expect
  = Http.post { url = "/feed"
              , body = Http.emptyBody
              , expect = Http.expectJson expect new
              }

{-| Decoder to turn a string into a List of Posts
-}
new : D.Decoder (List Post)
new = D.list decoder

{-| Decoder for a single Post

    D.decodeString decoder """
    { "title" : "Welcome", "content" : "To demnet", "author" : "Joris Gujahr" }
    """ === Post { title = "Welcome", content = "To demnet", "author" = "Joris Gutjahr", saved = True }

Be aware, that any Post, that has been decoded, has set `saved = True`
-}
decoder : D.Decoder Post
decoder =
  D.map3 (Post True)
    (D.field "title" D.string)
    (D.field "content" D.string)
    (D.field "author" D.string)

{-| Encode a Post into a E.Value to transmit to the server.
Used in the [`save`](#save) and [`publish`](#publish) functions
underlying [`upload`](#upload) function.

    Post { saved = False, title = "Welcome", content = "To demnet", author = "Joris Gutjahr" }
    |> encode
    |> Http.jsonBody

-}
encode : Post -> E.Value
encode post =
  E.object
    [ ("title", E.string post.title)
    , ("content", E.string post.content)
    , ("author", E.string post.author)
    ]
