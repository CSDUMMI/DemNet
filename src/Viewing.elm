module Viewing exposing (..)

import Element exposing (link, row, text, textColumn, spacing, padding)
import Element.Region as Region
import Element.Background as Background
import Element.Font as Font

type Posting msg = Posting  { title : String
                        , content : Element.Element msg }

white = Element.rgb255 255 255 255
grey  = Element.rgb255 96 96 96
link_color = Element.rgb255 153 153 255

viewNavigation : Element.Element msg
viewNavigation = Element.wrappedRow [spacing 10, padding 10, Background.color white, Font.color link_color ]
                             [ viewLink "/" "Home"
                             , viewLink "/login" "Login"
                             , viewLink "/register" "Register"
                             , viewLink "/news" "News" ]

viewLink : String -> String -> Element.Element msg
viewLink url description = link [] { url = url, label = text description }

viewNews : List (Posting msg) -> Element.Element msg
viewNews posts = textColumn [ spacing 10, padding 10] (List.map (\post -> viewPost post) posts)

viewPost : Posting msg -> Element.Element msg
viewPost (Posting post) =
  let title = Element.el [spacing 10, padding 10, Region.heading 1] (text post.title)
      content = Element.paragraph [spacing 10, padding 10] [post.content]
  in textColumn [ Background.color white ] [ title, content ]
