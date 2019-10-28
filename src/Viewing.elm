module Viewing exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)

viewHeader : Html Msg
viewHeader =
  div [ class "header_v" ]
    [ viewLink "/home" "Home"
    , viewLink "/login" "Login"
    , viewLink "/register" "Register"
    ]

viewLink : String -> List (Html Msg) -> Html Msg
viewLink reference content = a [ href reference ] content
