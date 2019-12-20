module Post exposing     ( Post
                         , empty
                         , welcome
                         , view_one
                         , view_many
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
@docs Post, welcome_post
# Views
@docs view_one, view_many
# Networking functions
@docs save, publish, upload, fetch
# Conversion
@docs new, decoder, encode
-}

import Http
import Json.Decode as D
import Json.Encode as E
import Element exposing ( Element )
import Element.Events as Events

import User exposing ( User )

-- DEFINITION

{-| Utility type for all response messages (for when packets arive)
-}
type alias Expect_Msg result msg = ( Result Http.Error result -> msg )

{-| Post, a simple data type to store a single Post.
content is special in that it is actually parsed as markdown.
-}
type alias Post = { saved : Bool
                  , title : String
                  , content : String
                  , author : User
                  }

{-| An empty post, especially useful for starting to write a new one.
The only thing left to apply is an author
-}
empty : User -> Post
empty = Post True "" ""

{-| An example post, that also functions as test and welcome message.
-}
welcome : Post
welcome =           { saved = True
                    , title = "Welcome to DemNet"
                    , content = """This is a democratic social network.
We designed it to be as direct and democratic as possible.
For every change there is an election where more than 50 % of the users
approve of the change.
If it affects the Election logic this number is raised to 80 %.
We use an Alternative Vote System.
- If you want an easy explaination of the concept [watch this](https://invidio.us/watch?v=3Y3jE3B8HsE)
- I'll write a long explaination specifically about DemNet's elections soon.
"""
                    , author = { username = "joris", first_name = "Joris", last_name = "Gutjahr" }
                    }
-- VIEWS
{-| Create an Element msg, showing a single post
-}
view_one : Element msg -> Element msg -> (String -> Element msg) -> (String -> Element msg) -> Post -> Element msg
view_one header footer fromTitle fromContent post
  = Element.textColumn []
    [ header
    , fromTitle post.title
    , fromContent post.content
    , User.view post.author
    ]

{-| Create a list of Posts, wich send a message, if clicked upon.
This is most useful in the Feed.
-}
view_many : (Post -> msg) -> Element msg -> Element msg -> List Post -> Element msg
view_many on_click header footer posts =
  [ header ]
  ++ List.foldr (\p acc -> (Element.el [Events.onClick (on_click p)] <| Element.text p.title)::acc) [] posts
  ++ [ footer ]
  |> Element.column []


-- NETWORKING

{-| Save a Post on the server, but don't publish it.
If you want to publish a Post use [`publish`](#publish)
-}
save : Expect_Msg String msg -> Post -> Cmd msg
save = upload "save"

{-| Publish a Post on the network.
After this the Post is immutably on the network.
If you just want to save your post for later and not yet publish,
use [`save`](#save)
-}
publish : Expect_Msg String msg -> Post -> Cmd msg
publish = upload "publish"

{-| The function behing both [`save`](#save) and [`upload`](#upload).
The only difference between the two is that they speck to different
routes. The Request is the same.
**This function isn't exposed.**
-}
upload : String -> Expect_Msg String msg ->  Post -> Cmd msg
upload url expect p
  = Http.post { url = "/content/" ++ url
              , body = Http.jsonBody <| encode p
              , expect = Http.expectString expect
              }

{-|  Fetch a few Posts.
You should use this command in combination
with [`new`](#new), which has the type: `String -> List Post`
-}
fetch : Expect_Msg (List Post) msg  -> Cmd msg
fetch expect
  = Http.post { url = "/feed"
              , body = Http.emptyBody
              , expect = Http.expectJson expect new
              }

-- CONVERSION

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
    (D.field "author" User.decoder)

{-| Encode a Post into a E.Value to transmit to the server.
Used in the [`save`](#save) and [`publish`](#publish) functions
underlying [`upload`](#upload) function.

    Post { saved = False, title = "Welcome", content = "To demnet", author = { username = "joris", first_name = "Joris", last_name = "Gutjahr" } }
    |> encode 0
    |> Http.jsonBody

-}
encode : Post -> E.Value
encode post =
  E.object
    [ ("title", E.string post.title)
    , ("content", E.string post.content)
    , ("author", User.encode post.author)
    ]
