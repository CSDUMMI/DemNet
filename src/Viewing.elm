module Viewing exposing (..)
import Html

viewNavigation : Html msg
viewNavigation = Html.nav [] [ viewLink "/" "Home"
                             , viewLink "/login" "Login"
                             , viewLink "/register" "Register"
                             , viewLink "/news" "News" ]

viewLink : String -> String -> Html msg
viewLink url description = Html.a [ Html.href url ] []
