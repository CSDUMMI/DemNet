module User exposing (User, empty, login, view, decoder, encode)
{-| Data Type and functions to handle users
# Definition
@docs User, empty
# Networking
@docs login
# Displaying
@docs show
# JSON
@docs decoder, encode
-}

import Element exposing (Element)
import Element.Border as B

import Http

import Json.Decode as D
import Json.Encode as E

{-| User is a type with all the necessary data about a user
-}
type alias User = { username : String
                  , first_name : String
                  , last_name : String
                  }

{-| empty is a user, who doesn't exist
-}
empty : User
empty = { username = "", first_name = "", last_name = "" }

{-| Request to login a user with this username or email and password
-}
login : String -> String -> String -> (Result Http.Error User -> msg) -> Cmd msg
login username password email msg =
  Http.post { url = "/login"
            , body = Http.multipartBody [ Http.stringPart "username" username
                                        , Http.stringPart "password" password
                                        , Http.stringPart "email" email
                                        ]
            , expect = Http.expectJson msg decoder
            }
{-| Simple square, to view for example below a post
-}
view : User -> Element msg
view user = Element.row
  [B.rounded 5,B.solid, B.width 5]
  [ Element.column []
    [ Element.text <| (user.first_name) ++ (user.last_name)
    , Element.text user.username
    ]
  ]

{-| Decoder for a User

    D.decodeString decoder """{ "username" : "joris", "first_name" : "Joris", "last_name" : "Gutjahr" }""" == { username = "joris", first_name = "Joris", last_name = "Gutjahr" }
    D.decodeString decoder """{ "username" = "abbashan", "first_name" = "Abbashan", "last_name" = "Karasahin" }""" == { username = "abbashan", first_name = "Abbashan", last_name = "Karasahin" }

-}
decoder : D.Decoder User
decoder = D.map3 User
  (D.field "username" D.string)
  (D.field "first_name" D.string)
  (D.field "last_name" D.string)

{-| Encode a User as E.Value

    E.encode 0 <| encode { username = "joris", first_name = "Joris",last_name = "Gutjahr" } == """{ "username" : "joris", "first_name" : "Joris", "last_name" : "Gutjahr"}"""
    E.encode 0 <| encode { username = "abbashan", first_name = "Abbashan", last_name = "Karasahin" } == """{ "username" = "abbashan", "first_name" = "Abbashan", "last_name" = "Karasahin" }"""

-}
encode : User -> E.Value
encode user =
  E.object
    [ ("username", E.string user.username)
    , ("first_name", E.string user.first_name)
    , ("last_name", E.string user.last_name)
    ]
