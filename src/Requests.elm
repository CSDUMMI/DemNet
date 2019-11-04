module Requests exposing ( save_post
                         , publish_post
                         )

import Http

save_post : msg -> post -> Cmd msg
save_post = upload "/save"

publish_post : msg -> post -> Cmd msg
publish_post = upload "/publish"

upload : String -> msg ->  post -> Cmd msg
upload url expect { title, content }
  = Http.post { url = url
              , body = Http.stringBody "plain/text" ( "# " ++ title ++ "\n" ++ content)
              , expect = Http.expectString expect
              }
