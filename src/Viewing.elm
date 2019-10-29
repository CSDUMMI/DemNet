module Viewing exposing (..)
import Element exposing (Element, text, link)
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font

viewHeader : Element a
viewHeader = Element.row []
    [ viewLink "/" (text "Home")
    , viewLink "/login" (text "Login")
    , viewLink "/register" (text "Register")
    , viewLink "/news" (text "News")
    ]

viewLink : String -> Element msg -> Element msg
viewLink url label = link []
                        { url = url
                        , label = label
                        }
