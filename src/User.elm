module User exposing (User, show, decoder, encode)
{-| Data Type and functions to handle users
# Definition
@docs User, empty
# Displaying
@docs show
# JSON
@docs decoder, encode
-}

import Element exposing (Element)
import Element.Border as B

{-| User is a type with all the necessary data about a user
-}
type alias User = { username : String
                  , first_name : String
                  , last_name : String
                  , key : String
                  , img_uri : String
                  }

{-| empty is a user, who doesn't exist
-}
empty : User
empty = { username = "", first_name = "", last_name = "", key = "", img_uri = "" }

{-| Simple square, to show for example below a post
-}
show : User -> Element msg
show user = Element.row
  [B.rounded 5,B.solid, B.width 5]
  [ Element.image [B.rounded 20,B.solid,B.width 5] { src = user.img_uri, description = user.username }
  , Element.column []
    [ Element.text <| (user.first_name) ++ (user.last_name)
    , Element.text user.username
    ]
  ]
