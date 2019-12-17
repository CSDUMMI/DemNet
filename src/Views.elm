module Views exposing ( reading
                      , writing
                      , feed
                      , Post_Element (..)
                      , Upload_Type (..)
                      )


import Element exposing ( Element )
import Element.Background as Background
import Element.Input as Input
import Post exposing ( Post )

-- Attribute Lists, that are used often:
post_attr = []

title_attr = []

reading_content_attr = []

edit_title_attr = [ Input.focusedOnLoad ]

edit_content_attr = []

list_attr = []
-- Datatypes for distinction:
type Post_Element = Title | Content

type Upload_Type = Publish | Save

view_post : Element msg -> Element msg -> (String -> Element msg) -> (String -> Element msg) -> Post -> Element msg
view_post header footer fromTitle fromContent post =
  Element.textColumn post_attr
    [ header
    , fromTitle post.title
    , fromContent post.content
    , footer
    ]

view_posts : Element msg -> Element msg -> List Post -> Element msg
view_posts header footer posts =
  Element.column list_attr
    [ header
    , Element.paragraph [] <| List.foldl (\p acc -> (Element.text p.title)::acc) [] posts
    , footer
    ]

reading : Post -> Element msg
reading
  = view_post
      Element.none
      Element.none
      (Element.el title_attr << Element.text)
      (Element.paragraph reading_content_attr << List.singleton << Element.text)

writing : (Post_Element -> String -> msg) -> Post -> Element msg
writing change_msg
  = view_post
      Element.none
      Element.none
      (\t -> Input.text edit_title_attr { onChange = change_msg Title
                                        , text = t
                                        , placeholder = Nothing
                                        , label = Input.labelLeft [] (Element.text "Title")
                                        })
      (\c -> Input.multiline edit_content_attr { onChange = change_msg Content
                                               , text = c
                                               , placeholder = Nothing
                                               , spellcheck = True
                                               , label = Input.labelAbove [] (Element.text "Content")
                                               })
feed : List Post -> Element msg
feed posts = posts
            |> view_posts Element.none Element.none []
