module Views exposing ( reading, writing, feed,vote, elections )


import Element exposing ( Element )
import Element.Background as Background
import Requests exposing ( Post )

view_post : Element -> Element -> (String -> Element) -> (String -> Element) -> Post -> Element
view_post header footer fromTitle fromContent post =
  Element.textColumn post_attr
    [ header
    , fromTitle post.title
    , fromContent post.content
    , footer
    ]

reading : Post -> 
