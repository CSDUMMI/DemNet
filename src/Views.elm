module Views exposing ( reading, writing, feed,vote, elections )


import Element exposing ( Element )
import Element.Background as Background
import Requests exposing ( Post )

view_post : Post -> Element -> Element -> (String -> Element) -> (String -> Element) -> Element
view_post post header footer fromTitle fromContent =
  Element.textColumn post_attr
    [ header
    , fromTitle post.title
    , fromContent post.content
    , footer
    ]
