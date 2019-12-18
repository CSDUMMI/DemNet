module Views exposing ( reading
                      , writing
                      , feed
                      , Post_Element (..)
                      , Upload_Type (..)
                      )


import Element exposing ( Element )
import Element.Background as Background
import Element.Input as Input
import Element.Events as Events
import Markdown

import Post exposing ( Post )

-- Attribute Lists, that are used often:
post_attr = []

title_attr = []

reading_content_attr = []

edit_title_attr = [ Input.focusedOnLoad, Element.minimum 200 Element.fill |> Element.width, Element.minimum 50 Element.fill |> Element.height]

edit_content_attr = [ Element.minimum 750 Element.fill |> Element.width, Element.minimum 750 Element.fill |> Element.height]

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
    , Element.text post.author
    , footer
    ]

view_posts : (Post -> msg) -> Element msg -> Element msg -> List Post -> Element msg
view_posts on_click header footer posts =
  Element.column list_attr
    [ header
    , Element.paragraph [] <| List.foldl (\p acc -> (Element.el [Events.onClick (on_click p)] <| Element.text p.title)::acc) [] posts
    , footer
    ]

reading : Post -> Element msg
reading
  = view_post
      Element.none
      Element.none
      (Element.el title_attr << Element.text)
      (Element.paragraph reading_content_attr << List.singleton << Element.html << Markdown.toHtml [])

writing : (Post_Element -> String -> msg) -> (Upload_Type -> Post -> msg) -> Post -> Element msg
writing change_msg upload post
  = let header = (Element.text <| case post.saved of
            True -> "Saved"
            False -> "Not Saved"
            )
        footer = (Element.row [Element.spacing 5]
            [ Element.el [Events.onClick <| upload Save post] <| Element.text "Save"
            , Element.el [Events.onClick <| upload Publish post] <| Element.text "Publish"
            ]
          )
        fromTitle = (\t -> Input.text edit_title_attr { onChange = change_msg Title
                                          , text = t
                                          , placeholder = Nothing
                                          , label = Input.labelAbove [Element.moveRight 350] (Element.text "Title")
                                          })
        fromContent = (\c -> Input.multiline edit_content_attr { onChange = change_msg Content
                                                 , text = c
                                                 , placeholder = Nothing
                                                 , spellcheck = True
                                                 , label = Input.labelAbove [Element.moveRight 345] (Element.text "Content")
                                                 })
    in view_post header footer fromTitle fromContent post


feed : (Post -> msg) -> List Post -> Element msg
feed on_click posts = posts
            |> view_posts on_click Element.none Element.none
