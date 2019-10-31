module Viewing exposing ( Post
                        , text_bg_color
                        , background_color
                        , link_color
                        , text_attr
                        , Nav_Items (..)
                        , viewNavigation
                        , viewPost
                        , viewPosts
                        , pairToPost
                        , Main_Page (..)
                        , Actions (..)
                        , viewNavBar
                        , viewUser
                        , viewMainPage
                        , viewActions
                        )

import Element exposing ( link
                        , row
                        , text
                        , textColumn
                        , spacing
                        , padding
                        )

import Element.Region as Region
import Element.Background as Background
import Element.Font as Font
import Element.Border as Border

import Markdown exposing  ( toHtmlWith
                          , Options
                          )

-- General Attributes, which are used often.
text_bg_color = Element.rgb255 255 255 255
background_color  = Element.rgb255 96 96 96
link_color = Element.rgb255 153 153 255

text_attr = [ Background.color text_bg_color
            , Border.rounded 20 ]

-- NAVIGATION
type Nav_Items =
    Home Nav_Items
  | Login Nav_Items
  | Register Nav_Items
  | None

reduceNavs : List (Element.Element msg)-> Nav_Items -> List (Element.Element msg)
reduceNavs navs nav_items =
    case nav_items of
      Home ns -> reduceNavs ((viewLink "/" "Home") :: navs) ns
      Login ns -> reduceNavs ((viewLink "/login" "Login") :: navs)ns
      Register ns -> reduceNavs ((viewLink "/register" "Register") :: navs) ns
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


-- POSTS

type Post msg = Post  { title : String
                        , content : Element.Element msg }

viewPosts : List (Post msg) -> Element.Element msg
viewPosts posts = textColumn [ spacing 10, padding 10 ] (List.map (\post -> viewPost post) posts)

viewPost : Post msg -> Element.Element msg
viewPost (Post post) =
  let title = Element.el [spacing 10, padding 10, Region.heading 1] (text post.title)
      content = Element.paragraph [spacing 10, padding 10] [post.content]
  in textColumn text_attr
                [ title, content ]

opts =  { githubFlavored = Just { tables = True, breaks = True }
            , defaultHighlighting = Just "elm"
            , sanitize = True
            , smartypants = True
            }

pairToPost : ( String, String ) -> Post msg
pairToPost (title, content) =
  let content_element = (Element.html << (toHtmlWith opts [])) content
  in Post { title = title, content = content_element }

-- Interpret the first #1 Heading as the title, and use anything else as content
stringToPost : String -> Post msg
stringToPost str_post =
  let post_lines = String.lines  str_post
      title_ = List.head (List.filter (\t -> String.startsWith "# " t) post_lines)
      title =
        case title_ of
          Just t -> t
          Nothing -> ""

      content_lines = List.filter ((/=) title) post_lines
      content = (Element.html << (toHtmlWith opts []) << (String.join "\n")) content_lines
  in  Post { title = title, content = content }


-- PAGE VIEWS
type User = User  { username : String
                  , firstName : String
                  , lastName : String
                  , img_logo : String -- SRC of the User's Image
                  }
type Main_Page
  = Feed
  | Editing
  | Reading
  | Login
  | Register

type Actions
  = Create_Post Actions
  | Publish_Post Actions
  | No_Action Actions

viewNavBar : Nav_Items -> Element.Element msg
viewNavBar navs =

viewUser : Maybe User -> Element.Element msg

viewMainPage : Main_Page -> Element.Element msg

viewActions : Actions -> Element.Element msg
