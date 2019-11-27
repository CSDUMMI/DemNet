module Views exposing ( reading, writing, feed,vote, elections )


import Element exposing ( Element )
import Element.Background as Background
import Requests exposing ( Post )

view_post : Post -> (String -> Element) Element
view_post post toElement = 
