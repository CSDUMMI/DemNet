module Viewing exposing ( Post
                        , text_bg_color
                        , background_color
                        , link_color
                        , text_attr
                        , User (..)
                        , Nav_Items (..)
                        , viewNavigation
                        , viewPost
                        , viewPosts
                        , pairToPost
                        , stringToPost
                        , Main_Page (..)
                        , Actions (..)
                        , viewHeadBar
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
import Element.Input as Input

import Markdown exposing  ( toHtmlWith
                          , Options
                          )

-- General Attributes, which are used often.
text_bg_color = Element.rgb255 255 255 255
bar_bg_color = Element.rgb255 17 69 240
background_color  = Element.rgb255 96 96 96
link_color = Element.rgb255 153 153 255

text_attr = [ Background.color text_bg_color
            , Border.rounded 20 ]

bar_attr = [ Background.color bar_bg_color
           , Border.solid ]
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
                  , img_logo : Maybe String -- SRC of the User's Image
                  }



viewHeadBar : Nav_Items -> Maybe User -> Element.Element msg
viewHeadBar nav_items user =
  let nav_bar = viewNavBar nav_items
      user_elem =   case user of
                      Just u -> viewUser u
                      Nothing -> [Element.text "Not Logged in"]
  in Element.row bar_attr (nav_bar::user_elem)


viewNavBar : Nav_Items -> Element.Element msg
viewNavBar = viewNavigation

-- SRC of default user image
defaultSrc = "/static/img/defaultUser.jpg"

viewUser : User -> List (Element.Element msg)
viewUser (User user) =
    let img_src = case user.img_logo of
                    Just src -> src
                    Nothing -> defaultSrc
        firstName = Element.text user.firstName
        lastName = Element.text user.lastName
        name = Element.column [] [ firstName, lastName ]
    in  [ Element.image [ Border.rounded 45 ] { src = img_src, description = "User's Image" }
        , name
        ]

type alias Editing_Post = { title : String
                          , content : String
                          }

type Main_Page msg
  = Feed (List (Post msg))
  | Editing (Editing_Post) (String -> msg) -- Function to call onChange
  | Reading (Post msg)
  | Login_Page (String -> msg) (String -> msg) msg


viewMainPage : Main_Page msg -> Element.Element msg
viewMainPage page =
  let attr = [ Region.mainContent,  Element.width Element.fill, Element.height Element.fill ]
  in
    case page of

      Feed messages -> viewPosts messages

      Editing post on_change ->
        Element.textColumn attr
        [ Input.text [] { onChange = on_change
                        , text = post.title
                        , placeholder = Nothing
                        , label = Input.labelAbove [] (Element.text "Title")
                        }
        , Input.multiline []  { onChange = on_change
                              , text = post.content
                              , placeholder = Nothing
                              , label = Input.labelAbove [] (Element.text "Content")
                              , spellcheck = True
                              }
        ]

      Reading (Post post) ->
        Element.textColumn attr
          [ Element.paragraph [ Region.heading 2 ] [ Element.text post.title ]
          , Element.el [] post.content
          ]

      Login_Page username_changed password_changed submit_pressed ->
        Element.textColumn attr
        [ Input.text [] { onChange = username_changed
                        , text = ""
                        , placeholder = Just <| Input.placeholder [] (Element.text "joris")
                        , label = Input.labelAbove [] (Element.text "Username")
                        }
        , Input.text [] { onChange = password_changed
                        , text = ""
                        , placeholder = Just <| Input.placeholder [] (Element.text "password")
                        , label = Input.labelAbove [] (Element.text "Password")
                        }
        , Input.button [] { onPress = Just submit_pressed
                          , label = Element.text "Login"
                          }
        ]


type Actions msg
  = Create_Post (Actions msg)
  | Publish_Post (Actions msg)
  | No_Action

viewActions : Actions msg -> Element.Element msg
viewActions actions =
  let action_field = [ Border.rounded 50 ]
      actions_list = reduceActions action_field actions

  in Element.column [] actions_list

reduceActions : List (Element.Attribute msg) -> Actions msg -> List (Element.Element msg)
reduceActions attr actions =
  case actions of
    Create_Post others -> (Element.el attr (Element.text "Write"))::(reduceActions attr others)
    Publish_Post others -> (Element.el attr (Element.text "Publish"))::(reduceActions attr others)
    No_Action -> []
