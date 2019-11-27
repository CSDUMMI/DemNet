module Views exposing ( reading, writing, feed,vote, elections )


import Element exposing ( Element )
import Element.Background as Background
import Requests exposing ( Post )

view_post : Post -> (String -> Element) -> (String -> Element) -> Element
view_post post fromTitle fromContent =
  Element.textColumn post_attr
    [ fromTitle post.title
    , fromContent post.content
    , additional_fields
    ]
