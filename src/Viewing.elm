module Viewing exposing (..)
import Element exposing (Element, text, link)
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font

viewHeader : Element a
viewHeader = Element.wrappedRow
    [ Element.spacingXY 100 2
    , Border.color (Element.rgb 255 255 255)
    , Element.width Element.fill
    ]
    [ viewLink "/" (text "Home")
    , viewLink "/login" (text "Login")
    , viewLink "/register" (text "Register")
    , viewLink "/news" (text "News")
    ]

viewLink : String -> Element msg -> Element msg
viewLink url label = link [ Element.width Element.fill ]
                        { url = url
                        , label = label
                        }

type Content = Text String | Image String String | Content (List Content)
type Posting = Posting { title : String
                       , content : Content
                       }

viewPosts : List Posting -> Element msg
viewPosts posts = Element.paragraph [] (List.map viewPost posts)

viewPost : Posting -> Element msg
viewPost (Posting { title, content }) = Element.row
                    [ Element.spacing 120 ]
                    ([ text title ] ++ [viewContent content])

viewContent : Content -> Element msg
viewContent posting =
  case posting of
    Text txt -> text txt
    Image url description  -> (Element.image [] { src = url, description = description })
    Content posts -> Element.textColumn [] (List.foldl (\x acc -> acc ++ [viewContent x]) [] posts)
