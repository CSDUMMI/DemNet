module Viewing exposing (..)

import Element exposing (link, row, text, textColumn, spacing, padding)
import Element.Region as Region
import Element.Background as Background
import Element.Font as Font
import Element.Border as Border

type Posting msg = Posting  { title : String
                            , content : Element.Element msg }

text_bg_color = Element.rgb255 255 255 255
background_color  = Element.rgb255 96 96 96
link_color = Element.rgb255 153 153 255

text_attr = [ Background.color text_bg_color
            , Border.rounded 20 ]

type Nav_Items =
    Home Nav_Items
  | Login Nav_Items
  | Register Nav_Items
  | News Nav_Items
  | Feed Nav_Items
  | None

reduceNavs : List (Element.Element msg)-> Nav_Items -> List (Element.Element msg)
reduceNavs navs nav_items =
    case nav_items of
      Home ns -> reduceNavs ((viewLink "/" "Home") :: navs) ns
      Login ns -> reduceNavs ((viewLink "/login" "Login") :: navs)ns
      Register ns -> reduceNavs ((viewLink "/register" "Register") :: navs) ns
      News ns -> reduceNavs ((viewLink "/news" "News") :: navs) ns
      Feed ns -> reduceNavs ((viewLink "/feed" "Feed") :: navs) ns
      None -> navs

viewNavigation : Nav_Items -> Element.Element msg
viewNavigation nav_items =
  let navs = reduceNavs [] nav_items
  in Element.wrappedRow

                 (text_attr ++ [ spacing 10
                               , padding 10
                               , Font.color link_color ])
                               navs



viewLink : String -> String -> Element.Element msg
viewLink url description = link [] { url = url, label = text description }

viewPosts : List (Posting msg) -> Element.Element msg
viewPosts posts = textColumn [ spacing 10, padding 10 ] (List.map (\post -> viewPost post) posts)

viewPost : Posting msg -> Element.Element msg
viewPost (Posting post) =
  let title = Element.el [spacing 10, padding 10, Region.heading 1] (text post.title)
      content = Element.paragraph [spacing 10, padding 10] [post.content]
  in textColumn text_attr
                [ title, content ]
