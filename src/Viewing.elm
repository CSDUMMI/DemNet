module Viewing exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)

viewHeader : Html a
viewHeader =
  div [ class "header_v" ]
    [ viewLink "/home" [text "Home"]
    , viewLink "/login" [text "Login"]
    , viewLink "/register" [text "Register"]
    ]

viewLink : String -> List (Html a) -> Html a
viewLink reference content = a [ href reference ] content
