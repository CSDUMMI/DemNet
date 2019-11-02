module Requests exposing  ( save_post
                          , publish_post
                          )

import Http
import Url

import Post

save_post : msg -> Post -> Cmd msg
save_post msg post = Http.post { url = Url.toString <| Url.absolute ["save_post"]
                           , body = stringBody "plain/text" (Post.toString post)
                           , expect = Http.expectString msg
}
